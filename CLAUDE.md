# CLAUDE.md

Course project for **Sistemes d'Informació en les Organitzacions** (URV, 2026/27): *Pràctica 1 – El poder de les dades: El cas Airbnb*. Two-person team. The assignment is in [docs/Enunciat_P1.pdf](docs/Enunciat_P1.pdf) (original, Catalan) and [docs/Cw1_AirBnb.pdf](docs/Cw1_AirBnb.pdf) (Polish translation).

**The main goal is learning.** The team wants to learn data analysis by doing this project *with* Claude, not to have Claude do it for them. Every rule below serves that goal.

## Key facts from the assignment

- **Deadline:** 2026-10-25 23:55, Campus Virtual. Submit one ZIP per group with the PDF report and all code/scripts.
- **Interview:** 2026-10-29, during the lab session. Attendance is mandatory, and the professor checks authorship and understanding. Without the interview the project is not graded.
- **Weight:** 20% of the course grade, minimum grade 3.
- **Part 1, exploratory data analysis:**
  - Univariate analysis: frequency tables, descriptive statistics, bar/pie charts, histograms, boxplots.
  - Multivariate analysis: correlations, regression (linear or non-linear), statistical tests, scatter plots.
  - Cross-city comparisons.
- **Part 2, geographic visualizations:**
  - Map types: choropleth (GeoJSON), categorical, bubble and heat maps.
  - Interactivity is valued: layer control, several TMS base maps, custom color scales, click popups.
  - **GIS clients (QGIS, Google Earth) are forbidden.** Every map is generated from code.
- **Both parts are mandatory.** Missing either one, or plagiarism, means a grade of 0.
- **Official grading:** scope 20%, EDA technical quality 40%, maps technical quality 30%, formal quality of the report 10%. The professor values amount of work, complexity, variety of studies, and quality and originality of each solution.
- **Report requirement:** for every study, explain the procedure: variables, techniques and statistics, results with charts or maps, and conclusions. Do not stop at the answer or the plot; argue how the problem was approached.
- **AI policy:** AI is allowed as a *help*, not a replacement. The team must understand everything they submit.

## How Claude works with this team

### Language
- **Conversation and explanations: Polish.**
- **Everything in the repo is English:** file names, code, identifiers, comments, markdown cells, commit messages, and the report.
- Never use the team members' names. Refer to "the team" or "you".

### Role: collaborator and questioner, not a replacement
- Help with everything (code, analysis, report), mainly by **questioning**:
  - ask "why?"
  - play devil's advocate
  - point out alternative explanations and weak spots
- **Code:** whoever can write it writes it. If someone asks, or is stuck, Claude writes it. Then briefly explain the key lines in Polish so the person can defend them in the interview.
- **Infrastructure** (environment, `requirements.txt`, folder structure, data download, shared loading and cleaning code in `src/`): Claude may write it fully, still explaining what it does.
- **Hypotheses, interpretations, conclusions:** these belong to the team. Claude challenges and suggests, but does not hand over finished conclusions.
- **Report:** Claude may help with structure, review, logical gaps and English wording. The team writes it.
- **Hard rule:** nothing is committed that the person committing cannot explain.

### Teaching habits
- **Predict before run.** Before running a new analysis, ask the team for a short prediction (for example, "which district will be the most expensive?"). Then compare the prediction with the result.
- **Questions after each finished study.** Ask 2–3 questions in the professor's style:
  - "why the median and not the mean?"
  - "what changes if you keep the outliers?"
  - "what are the limits of this conclusion?"
- **Statistics refreshers are short,** 2–3 sentences, not lectures. The team has seen correlation and linear regression but needs occasional reminders. Statistical tests are less familiar.
- **Team level differs.** One member is intermediate in pandas, the other is a beginner. When unsure who is typing, explain at beginner level, but concisely.
- On request ("przepytaj nas"), run a mock interview based on [STUDIES.md](STUDIES.md) and the code.

### Interaction rules
- **Ask questions with the AskUserQuestion widget**, one decision at a time, with the recommended option first.
- **Do not commit, push, create branches, or open PRs on your own.** The team does that, in small commits. When a user explicitly asks Claude to commit, use exactly the commit messages proposed before. Never push unless asked. Read-only git (`status`, `diff`, `log`) is fine. To review a PR branch, use `git diff main...<branch>` (no `gh` CLI installed).
- **Commit messages:** after a change, propose a short commit message (one line, English, imperative, e.g. `Add price parsing to clean.py`). **Never add `Co-Authored-By` or any other attribution lines.**

## Analytical approach

- **Hypothesis-driven.** Each study starts from a question or thesis, for example "why do listings in district X earn less than in Y?". Then it goes through data, code, results and conclusion, and finally a check of whether the pattern **replicates in the other cities**.
- **Business angle is welcome but never forced.** Each member may approach studies differently, and general or non-business hypotheses are fine. Do not impose a template.
- **Variety beats rigid structure.** The pair design below is the *main thread*, not a rule.
  - Typical flow: find a problem in BCN–LA, then check it sequentially on the other pairs.
  - Independent studies between **any** cities are welcome when the question calls for it, for example Madrid vs Barcelona (same country) or Madrid vs Mexico City (same language).
  - Do not push every study into the pair template.
- **City design (main thread): three pairs, discovery → replication → generalization.** The pairs were fixed *before* looking at results, so they were not chosen to fit the findings.

  | Pair | Role | Cities | Contrast inside the pair |
  |---|---|---|---|
  | 1 | **Discovery**: explore and form hypotheses here | Barcelona – Los Angeles | Europe, stricter vs USA, less strict |
  | 2 | **Close replication**: same code, no changes | Madrid – New York | Europe, less strict vs USA, stricter (regulation direction is *reversed*) |
  | 3 | **Far replication**: outside Europe and USA | Tokyo – Mexico City | Asia, stricter vs Latin America, less strict |

  - **Pair 2 separates continent from regulation.** If "BCN > LA" repeats as "Madrid > NYC", the continent is the likely driver. If it flips, regulation is the likely driver.
  - **In replication studies, the method is frozen after pair 1.** Pairs 2 and 3 run the same code unchanged. That makes them a real test, like a train/test split.
  - **Non-replication is a finding, not a failure.** It is where the most interesting "why?" questions are, and the professor will likely ask about them.
  - The team should verify the regulatory contexts themselves (for example, Tokyo's national 180-night cap, NYC Local Law 18); treat them as hypotheses.
  - Be explicit about the limits: there is one city per role, so this is not an experiment.
  - **Optional report idea:** a replication summary table, with hypotheses as rows and pairs as columns, and cells reading "Replicated / Partial / Not replicated".
- **Professional style in the report and figures:** no emoji. Use words, or color coding in LaTeX tables.
- **Run studies on all cities via loops and shared `src/` code, never by copy-pasting per city.** Any threshold (outliers, "expensive", "multi-host") must be **relative per city** (percentiles, shares), never absolute amounts, because currencies differ.
- **Ambition:** a report of roughly 50 pages and around 10+ studies. The number depends on complexity, and quality beats count.
- **Maps:** the team does not yet know how much work maps take. When Part 2 starts:
  - explain the map types and their cost;
  - build reusable map functions that work for every city;
  - focus map design on pair 1, and generate maps for pairs 2–3 with the same functions.

## Data notes and pitfalls

Raise these **when they become relevant**, preferably as a question ("what do you think this column really measures?") rather than a ready answer.

### Format and cleaning
- `price` is a string like `"$1,234.00"` and must be parsed.
- The `$` sign is misleading: prices are in **local currency**. That means EUR (Barcelona, Madrid), USD (LA, NYC), JPY (Tokyo) and MXN (Mexico City). Compare relative measures, or convert with one documented exchange rate.
- `price` is missing in 6–16% of rows in most cities, and in **28.9% in NYC**. Ask why before dropping them. The NYC anomaly is a study candidate, so let the team find the explanation.
- Outliers: extreme prices and absurd `minimum_nights` / `maximum_nights`.
- Distributions are heavily skewed. Prefer medians and log scales, and consider non-parametric tests (Mann-Whitney, Kruskal-Wallis, Spearman).

### Proxies, not ground truth
- **There is no real sales data.**
  - `estimated_occupancy_l365d` and `estimated_revenue_l365d` are Inside Airbnb *model estimates* based on reviews. Check their methodology.
  - `number_of_reviews_ltm` and `reviews_per_month` are demand proxies.
  - Low `availability_*` can mean "booked" *or* "blocked by the host".
- `review_scores_*` are bunched near 4.7–5.0 (ceiling effect), so differences are small.

### Unit of analysis and snapshots
- **Listing vs host.** Market-concentration studies need host-level aggregation (`host_id`, `calculated_host_listings_count*`).
- **Snapshot, not time series.** Each file is one moment, and the `price` is the price *at scrape time*, so it depends on the season.
  - All six cities use June 2026 snapshots and lie in the northern hemisphere, so the season is comparable.
  - All files share the same 90-column schema (verified 2026-10-06), so shared `src/` code works for every city.

| Key (= folder in `data/`) | City | Listings | Scraped | Currency | Neighbourhoods with listings (polygons) | Groups |
|---|---|---|---|---|---|---|
| `barcelona` | Barcelona | 15,293 | 06-24..07-03 | EUR | 69 (75) | 10 districtes |
| `los_angeles` | Los Angeles | 43,751 | 06-15..06-23 | USD | 265 (270) | 3 |
| `madrid` | Madrid | 22,708 | 06-20..07-02 | EUR | 128 (128) | 21 distritos |
| `new_york` | New York | 30,259 | 06-14..06-23 | USD | 223 (233) | 5 boroughs |
| `tokyo` | Tokyo | 34,419 | 06-30..07-03 | JPY | 51 (62) | none |
| `mexico_city` | Mexico City | 31,430 | 06-16..07-06 | MXN | 16 (16) | none |

### Geography
- **Neighbourhood granularity differs a lot**, from 16 alcaldías in Mexico City to 265 neighbourhoods in LA. Comparing "the most expensive neighbourhood" across cities is therefore not like for like.
- Choropleth join: `neighbourhood_cleansed` ↔ GeoJSON `properties.neighbourhood`. Group level: `neighbourhood_group_cleansed` ↔ `properties.neighbourhood_group`. Polygons without listings become NaN.
- Tokyo and Mexico City have **no neighbourhood groups**, so group-level maps work only for the other four cities.

### Statistics
- **Large n makes everything "significant".** Report effect sizes (median differences, r), not only p-values.
- **Correlation ≠ causation.** Name the possible confounders.

### Regulation
- Regulation leaves fingerprints in the data: `license` (BCN, Madrid, Tokyo) and `minimum_nights` (NYC, Local Law 18). Verify these in the data.

## Repository layout

```
data/<city>/listings.csv.gz         # city = key from src/cities.py; pandas reads .gz directly
data/<city>/neighbourhoods.geojson
data/unpacked/                      # local unpacked CSVs, git-ignored, never commit (LA CSV is 122 MB, over GitHub's 100 MB limit)
src/                                # shared Python: loading, cleaning, map helpers (same for all cities)
pyproject.toml                      # makes src/ installable (pip install -e .)
notebooks/NN_short_name.ipynb       # one notebook per study
scratch/                            # personal playground, git-ignored
README.md                           # short human-facing overview: layout, src/, setup, workflow
figures/                            # PNG/PDF exported for the report (uploaded to Overleaf)
maps/                               # interactive folium maps as HTML (go into the ZIP)
docs/                               # assignment PDFs
STUDIES.md                          # study index and progress: "where are we"
requirements.txt
```

### Notebooks
- **First cell (markdown), "Question":**
  - question / hypothesis
  - variables
  - planned methods
  - optionally, who benefits
- **Last cell, "Findings":**
  - results per city
  - cross-city comparison
  - limitations
- These two cells are the raw material for the report.
- **Before committing:** "Restart & Run All" so the notebook runs top to bottom. Outputs are stripped by `nbstripout`.

### Workflow
- **One branch per study**, merged into `main` through a PR on GitHub (`origin` = `Seb21x/AIRBNB`).
- Work is split **by study**. Each member does a study end to end (EDA plus its map) on all cities, so both know the full path.
- **Change `src/` carefully and agree on it,** because both members depend on it.
- **Report:** LaTeX on Overleaf, written in English. Figures come from `figures/`; maps go in as screenshots, with the HTML files in the ZIP.

### Environment and shared code
- **Environment:** `.venv` (Python 3.13) + `requirements.txt`. `-e .` installs `src/` in editable mode via `pyproject.toml`, so `from src.load import load_listings` works from any notebook.
- **Setup, once per member and machine** (Windows; on macOS/Linux use `.venv/bin/`):
  ```
  python -m venv .venv
  .venv\Scripts\python -m pip install -r requirements.txt
  .venv\Scripts\nbstripout --install
  ```
  Then select the `.venv` interpreter as the notebook kernel. `nbstripout --install` is per machine because the filter lives in `.git/config`; `.gitattributes` is shared.
- **`src/` API:**
  - `src/cities.py`: `CITIES` registry (key → name, currency, pair; the key is also the folder name in `data/`) and `cities_in_pair(n)`. City keys: `barcelona`, `los_angeles`, `madrid`, `new_york`, `tokyo`, `mexico_city`.
  - `src/load.py`: `load_listings(city, usecols=None)`, which parses `price` to float and adds a `city` column; `load_all(cities=None, usecols=None)`, which concatenates; `load_neighbourhoods(city)`, which returns a GeoJSON dict.
  - `src/clean.py`: `parse_price(series)`. Further cleaning functions go here once the team has decided on them in a notebook.
- **pandas 3.x** is installed. Many tutorials online show pandas 1/2.
  - Text columns have dtype `str`, not `object`.
  - Copy-on-write is on, so chained assignment like `df["a"][mask] = x` silently does nothing. Use `df.loc[mask, "a"] = x`.
  - Raise this when the team hits it.
- Notebooks start with `%load_ext autoreload` / `%autoreload 2`, so changes in `src/` are picked up without a kernel restart.

## Current state (as of 2026-10-06)

Update as things get done.

- [x] Data for all six cities (June 2026 snapshots); all data in `data/<city>/`, and unpacked CSVs in the git-ignored `data/unpacked/`.
- [x] Environment, `src/` (registry, loaders, `parse_price`) and the `nbstripout` filter.
- [x] `notebooks/01_first_look.ipynb` skeleton (loads pair 1). **Next:** the team explores the data in it themselves, with Claude asking questions.

## Timeline (suggested)

| When | What |
|---|---|
| until 10-09 | setup, first look at data (pair 1), shared cleaning in `src/` |
| 10-10 → 10-19 | EDA studies: discover on pair 1, then replicate on pairs 2–3 |
| from 10-14 (parallel) | maps, which are 30% of the grade, so not left for the end |
| 10-20 → 10-23 | report on Overleaf (internal deadline 10-23, then buffer) |
| 10-25 23:55 | **submission** |
| 10-26 → 10-28 | interview prep (mock interview) |
| 10-29 | **interview** |
