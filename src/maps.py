"""Interactive folium maps shared by all studies and cities."""
import copy
from pathlib import Path

import branca.colormap as cm
import folium
import pandas as pd
from folium.plugins import FastMarkerCluster, HeatMap, HeatMapWithTime

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
    colormap: cm.LinearColormap | None = None,
) -> None:
    """Colour the neighbourhood polygons of `city` by `values` (a Series indexed by neighbourhood name).

    `counts` is the number of listings per neighbourhood. Neighbourhoods with fewer than `min_count` listings
    (or none) are drawn grey, because a share computed from a handful of listings is mostly noise.
    Hovering shows a tooltip, and clicking opens a popup with the same details.
    By default the colours run from the lowest to the highest value; pass `colormap` for another scale
    (e.g. a diverging one from `diverging_colormap`).
    """
    reliable = values[counts.reindex(values.index).fillna(0) >= min_count].dropna()
    if colormap is None:
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


def diverging_colormap(max_ratio: float, caption: str) -> cm.LinearColormap:
    """Blue-grey-red scale for a ratio centred on 1: blue below 1, neutral grey at 1, red above 1.

    The scale runs from 1 / max_ratio to max_ratio, so that e.g. 0.5 and 2 are equally far from the centre.
    """
    index = [1 / max_ratio, 1 / max_ratio**0.5, 1, max_ratio**0.5, max_ratio]
    return cm.LinearColormap(
        ["#1c5cab", "#86b6ef", "#f0efec", "#ef9a99", "#c23b3a"], index=index,
        vmin=index[0], vmax=index[-1], caption=caption,
    )


def add_heatmap(m: folium.Map, df: pd.DataFrame, name: str, show: bool = False, weight: str | None = None) -> None:
    """Heat map of the points in `df`, as a layer that can be switched on and off.

    Without `weight` every listing counts once (supply density); with `weight` (a column name) each listing
    counts with that value, e.g. its number of reviews (demand density).
    """
    points = df[["latitude", "longitude"]].round(5)
    if weight:
        # Leaflet treats an intensity of 1 as the maximum, so weights are scaled to 0-1 by the 99th percentile
        points["w"] = (df[weight] / df[weight].quantile(0.99)).clip(upper=1).round(3)
    HeatMap(points.values.tolist(), name=name, show=show, radius=10, blur=12, min_opacity=0.3).add_to(m)


def add_bubbles(
    m: folium.Map,
    data: pd.DataFrame,
    size: str,
    value: str,
    colormap: cm.LinearColormap,
    name: str,
    label: str = "neighbourhood",
    fmt: str = "{:.2f}",
    max_radius: int = 25,
    show: bool = False,
) -> None:
    """Bubble map: one circle per row of `data` (needs `latitude` and `longitude` columns).

    The circle area grows with the `size` column, and the colour shows the `value` column on `colormap`.
    Clicking a circle opens a popup with the label, size and value.
    """
    layer = folium.FeatureGroup(name=name, show=show)
    for _, row in data.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=max_radius * (row[size] / data[size].max()) ** 0.5,  # radius ~ sqrt, so the area ~ size
            color="white", weight=1,
            fill=True, fill_color=colormap(row[value]), fill_opacity=0.85,
            tooltip=f"{row[label]}: {fmt.format(row[value])}",
            popup=folium.Popup(f"<b>{row[label]}</b><br>{size}: {row[size]:,.0f}<br>{value}: {fmt.format(row[value])}", max_width=250),
        ).add_to(layer)
    layer.add_to(m)


def save_map(m: folium.Map, filename: str) -> Path:
    """Add the layer control and save the map as HTML in maps/. Returns the path of the file."""
    folium.LayerControl(collapsed=False).add_to(m)
    MAPS_DIR.mkdir(exist_ok=True)
    path = MAPS_DIR / filename
    m.save(path)
    return path


def _text_color(hex_color: str) -> str:
    """Black or white, whichever is easier to read on `hex_color` (by its relative luminance)."""
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return "black" if 0.2126 * r + 0.7152 * g + 0.0722 * b > 0.5 else "white"


def add_category_points(
    m: folium.Map,
    df: pd.DataFrame,
    category: str,
    colors: dict,
    label: str,
    name_prefix: str = "",
    show: list | None = None,
) -> None:
    """Categorical point map: one layer per category, each listing a small circle in its category's colour.

    `colors` maps each category of the `category` column (in display order) to a colour. Points are grouped
    into clusters that split up when zooming in (FastMarkerCluster draws the points in the browser, so
    maps with tens of thousands of listings stay small and fast); a cluster shows the number of listings
    in it and has the colour of its layer. Hovering a point shows the `label` column. Only the categories
    in `show` are switched on when the map opens.
    """
    show = show or []
    for cat, color in colors.items():
        points = df.loc[df[category] == cat, ["latitude", "longitude", label]]
        points = points.assign(latitude=points["latitude"].round(5), longitude=points["longitude"].round(5),
                               **{label: points[label].astype(str)})
        callback = f"""function (row) {{
            var marker = L.circleMarker(new L.LatLng(row[0], row[1]),
                {{radius: 5, color: "white", weight: 1, fillColor: "{color}", fillOpacity: 0.9}});
            marker.bindTooltip(row[2]);
            return marker;
        }}"""
        icon = f"""function (cluster) {{
            var n = cluster.getChildCount();
            var size = n < 100 ? 28 : (n < 1000 ? 36 : 44);
            return L.divIcon({{
                html: '<div style="background:{color};color:{_text_color(color)};width:' + size + 'px;height:' + size
                      + 'px;box-sizing:border-box;border-radius:50%;border:2px solid white;display:flex;'
                      + 'align-items:center;justify-content:center;font:12px sans-serif;opacity:0.9">' + n + '</div>',
                className: "", iconSize: L.point(size, size)}});
        }}"""
        # FastMarkerCluster always adds itself to its parent, so it sits in a FeatureGroup, which the layer
        # control can switch on and off (and which respects `show`)
        layer = folium.FeatureGroup(name=f"{name_prefix}{cat} ({len(points):,} listings)", show=cat in show)
        FastMarkerCluster(points.values.tolist(), callback=callback, icon_create_function=icon,
                          control=False).add_to(layer)
        layer.add_to(m)


def add_heatmap_over_time(m: folium.Map, df: pd.DataFrame, period: str, name: str, radius: int = 8) -> None:
    """Animated heat map: one frame per value of the `period` column (e.g. entry year), with a time slider.

    Each frame shows only the listings of that period, so the animation shows where new listings appeared
    period by period. The slider and the play button sit in the bottom-left corner.
    """
    periods = sorted(df[period].dropna().unique())
    frames = [df.loc[df[period] == p, ["latitude", "longitude"]].round(5).values.tolist() for p in periods]
    HeatMapWithTime(frames, index=[str(int(p)) for p in periods], name=name, radius=radius,
                    min_opacity=0.2, max_opacity=0.8, auto_play=False).add_to(m)
