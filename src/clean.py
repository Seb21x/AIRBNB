"""Cleaning helpers shared by all cities."""
import pandas as pd


def parse_price(s: pd.Series) -> pd.Series:
    """Convert price strings like "$1,234.00" to floats in local currency. Unparseable values become NaN."""
    if pd.api.types.is_numeric_dtype(s):  # already numeric, e.g. a column that is entirely NaN
        return s.astype(float)
    return pd.to_numeric(s.str.replace(r"[$,]", "", regex=True), errors="coerce")
