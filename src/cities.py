"""Registry of the cities analysed in this project."""
from dataclasses import dataclass
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@dataclass(frozen=True)
class City:
    key: str  # short id used in code and as the folder name in data/, e.g. "barcelona"
    name: str  # display name for plots and the report
    currency: str  # currency of `price` (the "$" sign in the raw data is misleading)
    pair: int  # 1 = discovery, 2 = close replication, 3 = far replication

    @property
    def path(self) -> Path:
        return DATA_DIR / self.key


CITIES = {
    c.key: c
    for c in [
        City("barcelona", "Barcelona", "EUR", 1),
        City("los_angeles", "Los Angeles", "USD", 1),
        City("madrid", "Madrid", "EUR", 2),
        City("new_york", "New York", "USD", 2),
        City("tokyo", "Tokyo", "JPY", 3),
        City("mexico_city", "Mexico City", "MXN", 3),
    ]
}


def cities_in_pair(pair: int) -> list[str]:
    """Keys of the two cities in a pair, e.g. cities_in_pair(1) -> ["barcelona", "los_angeles"]."""
    return [key for key, c in CITIES.items() if c.pair == pair]
