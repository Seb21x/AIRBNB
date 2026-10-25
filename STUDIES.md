# Studies

Index of all studies: "where are we". One row per study. Details live in each notebook's *Question* and *Findings* cells.

Status: `idea` → `wip` → `review` (PR open) → `done`

Pair columns: pair 1 = BCN–LA (discovery), pair 2 = Madrid–NYC, pair 3 = Tokyo–Mexico City. Values for pairs 2–3: `Replicated` / `Partial` / `Not replicated` / `–` (not run yet). For independent studies outside the pair design (for example Madrid vs Barcelona), use `n/a` in the pair columns and name the cities in the question.

| # | Notebook | Question / hypothesis | Part | Status | Pair 1 | Pair 2 | Pair 3 | Key finding |
|---|----------|-----------------------|------|--------|--------|--------|--------|-------------|
| 04 | `04_rental_model.ipynb` | Is Airbnb still a short-stay product, or has part of it become monthly rental (30+ nights)? | EDA + maps | wip | BCN 37%, LA 47% monthly+ | Partial | Partial | The monthly peak sits on each city's legal line (31–32 nights BCN, 30 nights LA/NYC); share follows regulation, not continent (LA: 74% inside the city boundary, 9–22% outside) |
| 05 | `05_demand_geography.ipynb` | Is Airbnb supply located where the demand (reviews in the last 12 months) is? | EDA + maps | wip | Demand follows supply (ρ 0.97, 0.90), Gini 0.61 | Replicated | Partial | Demand is concentrated everywhere (top 10% of listings get 33–42% of reviews); Barcelona's old town and central Manhattan get less demand per listing; airport neighbourhoods more |

## Ideas backlog

Questions not started yet. Anyone can add.

- 06: Who is the city for? Solo travellers and couples vs families and groups (`accommodates`, `bedrooms`, `room_type`); map: median `accommodates` per neighbourhood.
- 07: Market maturity: is the market growing, when did hosts join, is there a COVID dip (`host_since`, `first_review`); map: share of new listings per neighbourhood.
