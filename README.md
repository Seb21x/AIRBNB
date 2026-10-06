# Airbnb data analysis – SIO Pràctica 1

Exploratory and geographic analysis of Inside Airbnb data (June 2026) for six cities. URV, Sistemes d'Informació en les Organitzacions 2026/27.

## Repository

```
data/<city>/      listings.csv.gz + neighbourhoods.geojson (data/unpacked/ is git-ignored)
src/              shared code, the same for every city
notebooks/        one notebook per study: NN_short_name.ipynb
scratch/          your own playground, git-ignored
figures/, maps/   (later) charts for the report, interactive HTML maps
docs/             assignment
STUDIES.md        index of studies and progress
CLAUDE.md         instructions for Claude Code
```

## Cities

| Pair | Role | Cities (keys) |
|---|---|---|
| 1 | discovery | `barcelona`, `los_angeles` |
| 2 | close replication | `madrid`, `new_york` |
| 3 | far replication | `tokyo`, `mexico_city` |

## src/

| File | What it does |
|---|---|
| `cities.py` | `CITIES` registry (name, currency, pair); `cities_in_pair(n)` |
| `load.py` | `load_listings(city)` (price parsed, `city` column added), `load_all()`, `load_neighbourhoods(city)` |
| `clean.py` | `parse_price()`; more cleaning functions go here |

```python
from src.load import load_listings, load_all
bcn = load_listings("barcelona")
```

## Setup (once per machine)

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\nbstripout --install
```

Then select `.venv` as the notebook kernel.

## Workflow

1. `git pull`, then create a branch per study: `git checkout -b study/NN-short-name`.
2. In the notebook, write the **Question** cell, then the analysis (looping over cities), then the **Findings** cell.
3. Run "Restart & Run All" before committing. Keep commits small.
4. Update `STUDIES.md`, open a PR and merge to `main`.
