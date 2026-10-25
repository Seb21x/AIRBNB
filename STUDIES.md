# Studies

Notebook 01 supplies methodology. The eight substantive studies are 02–09. Pair 1 is Barcelona–Los Angeles, pair 2 Madrid–New York, pair 3 Tokyo–Mexico City; the four new studies compare Barcelona and Madrid directly. The pairs organize comparisons, not causal identification.

| # | Notebook | Question and scope | Main interpretation |
|---|---|---|---|
| 01 | `01_first_look.ipynb` | Dimensions, dates, IDs and missingness (six cities) | Audit supports the methodology; not a separate study |
| 02 | `02_host_economy.ipynb` | Account-size concentration, room mix and ratings (six cities) | Concentrated listing accounts do not identify companies or ownership |
| 03 | `03_price_distribution.ipynb` | Price shape, spread and same-currency comparison (six cities) | All cities are right-skewed; Barcelona median EUR 177.67 vs Madrid EUR 125 |
| 04 | `04_room_type_price.ipynb` | Room-type medians and tests (six cities) | Private-room medians are lower everywhere; unadjusted group differences |
| 05 | `05_rental_model.ipynb` | Minimum stays, review/calendar checks and geography (six cities) | Monthly+ share varies from 1.2% to 81.7%; actual stays and policy effects are unobserved |
| 06 | `06_short_stay_geography.ipynb` | Neighbourhood shares of entire homes with 1–29-night minimums (Spain) | Share of Airbnb listings, not housing stock; counts and join audit exported |
| 07 | `07_monthly_stay_cost.ipynb` | Valid 28–35-night EUR quotes normalized to 30 nights (Spain) | Date coverage and sample selection limit comparisons; not ordinary rents |
| 08 | `08_price_regression.ipynb` | One complete-case log-price OLS model with HC3 intervals (Spain) | Conditional price associations, with full-rank and finite-result checks |
| 09 | `09_price_guest_activity.ipynb` | Price–annual-review Spearman correlations and one age check (Spain) | Reviews are an activity proxy; not occupancy or realized revenue |

Execution status and sample counts are generated in `tables/execution.json` and study-specific CSVs. The report's numerical macros and tables are built from these exports; they are not hand-entered. `report/verification.json` records delivery checks. Regenerate these files after changing code or data.
