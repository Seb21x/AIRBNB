"""Interactive folium maps shared by all studies and cities."""
import copy
from pathlib import Path

import branca.colormap as cm
import folium
import pandas as pd
from folium.plugins import HeatMap

from src.load import load_neighbourhoods

MAPS_DIR = Path(__file__).resolve().parent.parent / "maps"

# Base maps from different tile providers (TMS); the viewer switches between them in the layer control.
# All of them work without an API key (CartoDB tiles need one since 2025).
BASE_MAPS = {
    "Light grey (Esri World Gray Canvas)": "Esri.WorldGrayCanvas",
    "OpenStreetMap": "OpenStreetMap.Mapnik",
    "Satellite (Esri World Imagery)": "Esri.WorldImagery",
}

# One blue hue from light to dark, for magnitudes such as shares or medians
BLUES = ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]
NO_DATA_COLOR = "#d9d9d9"


def base_map(df: pd.DataFrame) -> folium.Map:
    """Empty map fitted to the listings in `df` (one city), with all base maps added."""
    m = folium.Map(tiles=None, control_scale=True)
    for i, (name, tiles) in enumerate(BASE_MAPS.items()):
        folium.TileLayer(tiles, name=name, show=(i == 0)).add_to(m)  # the first base map is shown on opening
    # Fit to the 1st-99th percentile of coordinates, so a few far-away listings do not zoom the map out
    lat, lon = df["latitude"], df["longitude"]
    m.fit_bounds([[lat.quantile(0.01), lon.quantile(0.01)], [lat.quantile(0.99), lon.quantile(0.99)]])
    return m


def add_choropleth(
    m: folium.Map,
    city: str,
    values: pd.Series,
    counts: pd.Series,
    name: str,
    legend: str,
    fmt: str = "{:.1f}%",
    min_count: int = 20,
    colors: list[str] = BLUES,
) -> None:
    """Colour the neighbourhood polygons of `city` by `values` (a Series indexed by neighbourhood name).

    `counts` is the number of listings per neighbourhood. Neighbourhoods with fewer than `min_count` listings
    (or none) are drawn grey, because a share computed from a handful of listings is mostly noise.
    Hovering shows a tooltip, and clicking opens a popup with the same details.
    """
    reliable = values[counts.reindex(values.index).fillna(0) >= min_count].dropna()
    colormap = cm.LinearColormap(colors, vmin=reliable.min(), vmax=reliable.max(), caption=legend)

    # Copy the GeoJSON and write the value and listing count into each polygon's properties for the tooltip
    geojson = copy.deepcopy(load_neighbourhoods(city))
    for feature in geojson["features"]:
        props = feature["properties"]
        nbhd = props["neighbourhood"]
        props["listings"] = int(counts.get(nbhd, 0))
        props["value"] = reliable.get(nbhd)
        props["value_label"] = fmt.format(props["value"]) if props["value"] is not None else f"fewer than {min_count} listings"

    def style(feature):
        value = feature["properties"]["value"]
        return {
            "fillColor": colormap(value) if value is not None else NO_DATA_COLOR,
            "fillOpacity": 0.75,
            "color": "white",  # thin white borders keep neighbouring polygons apart
            "weight": 1,
        }

    # Tokyo and Mexico City have no neighbourhood groups, so the group is shown only where it exists
    has_groups = any(f["properties"].get("neighbourhood_group") for f in geojson["features"])
    fields = ["neighbourhood"] + (["neighbourhood_group"] if has_groups else []) + ["value_label", "listings"]
    aliases = ["Neighbourhood"] + (["District / group"] if has_groups else []) + [name, "Listings"]

    folium.GeoJson(
        geojson,
        name=name,
        style_function=style,
        highlight_function=lambda _: {"weight": 3, "color": "black"},
        tooltip=folium.GeoJsonTooltip(fields=fields, aliases=aliases, sticky=True),
        popup=folium.GeoJsonPopup(fields=fields, aliases=aliases),
    ).add_to(m)
    colormap.add_to(m)


def add_heatmap(m: folium.Map, df: pd.DataFrame, name: str, show: bool = False) -> None:
    """Heat map of listing density from the coordinates in `df`, as a layer that can be switched on and off."""
    points = df[["latitude", "longitude"]].round(5).values.tolist()
    HeatMap(points, name=name, show=show, radius=10, blur=12, min_opacity=0.3).add_to(m)


def save_map(m: folium.Map, filename: str) -> Path:
    """Add the layer control and save the map as HTML in maps/. Returns the path of the file."""
    folium.LayerControl(collapsed=False).add_to(m)
    MAPS_DIR.mkdir(exist_ok=True)
    path = MAPS_DIR / filename
    m.save(path)
    return path
