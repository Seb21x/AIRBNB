"""Loading Inside Airbnb data for one or many cities."""
import json

import pandas as pd

from src.cities import CITIES
from src.clean import parse_price


def load_listings(city: str, usecols: list[str] | None = None) -> pd.DataFrame:
    """Load listings of one city, with `price` parsed to float and a `city` column added."""
    df = pd.read_csv(CITIES[city].path / "listings.csv.gz", usecols=usecols, low_memory=False)
    if "price" in df.columns:
        df["price"] = parse_price(df["price"])
    df.insert(0, "city", city)
    return df


def load_all(cities: list[str] | None = None, usecols: list[str] | None = None) -> pd.DataFrame:
    """Load several cities (default: all) into one DataFrame, one row per listing."""
    cities = cities or list(CITIES)
    return pd.concat([load_listings(c, usecols) for c in cities], ignore_index=True)


def load_neighbourhoods(city: str) -> dict:
    """Load the neighbourhood polygons of one city as a GeoJSON dict (folium accepts it directly)."""
    with open(CITIES[city].path / "neighbourhoods.geojson", encoding="utf-8") as f:
        return json.load(f)
