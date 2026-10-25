"""Small shared helpers for reproducible tables and the four Spain studies."""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import Normalize
from matplotlib.patches import Patch, PathPatch
from matplotlib.path import Path as MplPath

from src.cities import CITIES
from src.load import load_all, load_neighbourhoods

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
TABLES = ROOT / "tables"
SPAIN = ["barcelona", "madrid"]


def export_table(data, name, index=False):
    TABLES.mkdir(exist_ok=True)
    data.to_csv(TABLES / f"{name}.csv", index=index)
    return data


def save_figure(fig, name):
    FIGURES.mkdir(exist_ok=True)
    fig.savefig(FIGURES / f"{name}.png", dpi=180, bbox_inches="tight")


def load_spain():
    columns = ["id", "last_scraped", "room_type", "price", "accommodates", "bedrooms",
               "minimum_nights", "neighbourhood_cleansed", "neighbourhood_group_cleansed",
               "first_review", "number_of_reviews_ltm", "price_quote_checkin_date",
               "price_quote_checkout_date", "price_quote_total_price", "price_quote_raw"]
    data = load_all(SPAIN, usecols=columns)
    assert not data.duplicated(["city", "id"]).any(), "Duplicate listing IDs within a city"
    data["city_name"] = data.city.map({k: c.name for k, c in CITIES.items()})
    for col in ["last_scraped", "first_review", "price_quote_checkin_date", "price_quote_checkout_date"]:
        data[col] = pd.to_datetime(data[col], errors="coerce")
    data["quote_nights"] = (data.price_quote_checkout_date - data.price_quote_checkin_date).dt.days
    data["quote_total"] = pd.to_numeric(data.price_quote_total_price, errors="coerce")
    data["short_entire"] = data.room_type.eq("Entire home/apt") & data.minimum_nights.between(1, 29)
    return data


def quote_metadata(raw):
    """Read availability/currency; invalid JSON is an invalid quotation, not a crash."""
    try:
        quote = json.loads(raw).get("quote", {})
        return quote.get("currency"), quote.get("is_available")
    except (TypeError, ValueError, AttributeError):
        return None, None


def neighbourhood_map(city, table, value, title, filename, vmin=0, vmax=100):
    """Static GeoJSON choropleth, including holes, without a GIS client or web tiles.

    table: indexed by neighbourhood; requires listings and the value column.
    Same 0--100 scale for comparable percentage maps. Small samples stay grey.
    """
    geo = load_neighbourhoods(city)
    names = {f["properties"]["neighbourhood"] for f in geo["features"]}
    assert set(table.index).issubset(names), f"Unmatched neighbourhoods in {city}"
    fig, ax = plt.subplots(figsize=(7.5, 6.5))
    norm, cmap = Normalize(vmin, vmax), plt.get_cmap("YlOrRd")
    for feature in geo["features"]:
        name = feature["properties"]["neighbourhood"]
        n = int(table.loc[name, "listings"]) if name in table.index else 0
        val = table.loc[name, value] if name in table.index else np.nan
        color = cmap(norm(val)) if n >= 20 and np.isfinite(val) else "#dddddd"
        geom = feature["geometry"]
        assert geom["type"] in ("Polygon", "MultiPolygon")
        polygons = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
        for polygon in polygons:
            paths = []
            for i, ring in enumerate(polygon):
                xy = np.asarray(ring, dtype=float)
                # Exterior counterclockwise, holes clockwise for nonzero winding fill.
                signed = np.sum(xy[:-1, 0]*xy[1:, 1] - xy[1:, 0]*xy[:-1, 1])
                if (signed > 0) != (i == 0):
                    xy = xy[::-1]
                codes = [MplPath.MOVETO] + [MplPath.LINETO]*(len(xy)-2) + [MplPath.CLOSEPOLY]
                paths.append(MplPath(xy, codes))
            ax.add_patch(PathPatch(MplPath.make_compound_path(*paths), facecolor=color,
                                   edgecolor="white", linewidth=0.6))
    ax.autoscale_view()
    mid_lat = np.mean(ax.get_ylim())
    ax.set_aspect(1 / np.cos(np.deg2rad(mid_lat)))
    ax.set_xlabel("Longitude (degrees)")
    ax.set_ylabel("Latitude (degrees)")
    ax.set_title(f"{CITIES[city].name}: {title}")
    ax.tick_params(labelsize=8)
    ax.annotate("N ↑", xy=(0.95, 0.94), xycoords="axes fraction", ha="center")
    ax.legend(handles=[Patch(facecolor="#dddddd", label="Fewer than 20 listings / no data")],
              loc="lower left", fontsize=8)
    fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, shrink=0.75,
                 label="Share of all Airbnb listings in neighbourhood (%)")
    fig.tight_layout()
    save_figure(fig, filename)
    return fig
