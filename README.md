# Airbnb analysis — SIO Pràctica 1

Eight substantive studies of the supplied Airbnb snapshots, with a focused Barcelona–Madrid extension. Notebook 01 is the data audit; notebooks 02–09 contain the eight studies. Assignment requirements come from the PDFs in `docs/`.

The English report is [`report/report.pdf`](report/report.pdf), with editable source in [`report/report.tex`](report/report.tex). The submission archive is generated at `deliverables/airbnb_submission.zip`. **The team must fill in the author details on the title page and recompile before submitting.**

## Reproduce

Use Python 3.11+ (verified with Python 3.13). From the project root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-lock.txt
.venv/bin/python scripts/run_all.py
.venv/bin/python scripts/build_report.py
tectonic --keep-logs report/report.tex
.venv/bin/python scripts/verify_delivery.py
.venv/bin/python scripts/package_delivery.py
```

On Windows, use `.venv\Scripts\python.exe`. `requirements-lock.txt` records exact versions from the verified environment; `requirements.txt` lists the direct requirements. JupyterLab is not required. The runner executes each notebook in a fresh Python kernel, from the `notebooks/` directory, and stops on an error. To rerun one notebook, supply its filename, e.g. `scripts/run_all.py 08_price_regression.ipynb`.

Install [Tectonic](https://tectonic-typesetting.github.io/) separately (on macOS, `brew install tectonic`); the first compilation downloads standard TeX packages. Alternatively, run `pdflatex report.tex` twice from `report/`. All analysis inputs are already in the archive. The archived PDF and static plots work offline. HTML maps require internet for external basemaps and, for Folium maps, JavaScript libraries. Plotly JavaScript is embedded in its HTML exports.

## Layout

| Path | Contents |
|---|---|
| `data/<city>/` | Original compressed listings and neighbourhood GeoJSON files |
| `src/` | Original loader/registry APIs, integrated Folium map helpers and one study utility module |
| `notebooks/01_*.ipynb` | Data audit and missingness |
| `notebooks/02–05` | Existing host, price, room-type and rental-model studies |
| `notebooks/06–09` | New short-stay geography, monthly quotations, regression and activity studies |
| `tables/` | CSV results, filter audits and notebook execution records |
| `figures/` | Reproducibly generated figures used in the report |
| `maps/` | Interactive HTML maps and retained original supplementary images |
| `report/` | LaTeX source, generated tables/macros, PDF and verification report |
| `scripts/` | Execution, report generation, validation and ZIP packaging |
| `STUDIES.md` | Study index and interpretation limits |

## Definitions and limitations

- All new calculations use only repository data. Official housing publications provide brief report context; no external rent or income data is merged.
- Study 05 groups minimum stays as 1–6, 7–29 and 30+ nights. Studies 06/09 use entire homes with minimums of 1–29 nights. Minimum stay is an advertised rule, not actual booked duration.
- Study 06 maps **neighbourhoods**, not the larger districts. Its denominator is all Airbnb listings, including missing prices. Fewer than 20 listings means grey fill. The two new maps share a 0–100% scale.
- Study 07 uses successful EUR quotes of 28–35 nights and computes `total / nights * 30`. Outliers remain in the summaries. Fee/tax coverage and dates limit comparisons; these are not ordinary monthly rents.
- Study 08 is one complete-case log-price OLS model with HC3 intervals. It excludes exact location and quote dates, and does not establish causation.
- Study 09 treats annual reviews as activity, not occupancy or revenue, and repeats only for listings with a first review at least one calendar year before their scrape date.
- Existing USD/JPY/MXN conversions are explicitly labelled illustrative assumptions, not verified historical exchange rates. All Spain prices are native EUR.

The rental-model additions were imported from the locally available `origin/study/04-rental-model` branch and numbered 05 without replacing the room-type study from `main`. Existing studies received execution, export and interpretation corrections. No commits or remote changes were made as part of report preparation.
