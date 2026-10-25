"""Automated verification of project requirements, execution, statistics and PDF."""
import json
from pathlib import Path
import sys

import pandas as pd
import pypdf

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "tables"
FIGURES = ROOT / "figures"
MAPS = ROOT / "maps"
REPORT = ROOT / "report"


def verify_all():
    checks = {}
    all_passed = True

    # 1. Notebook execution
    exec_file = TABLES / "execution.json"
    if not exec_file.exists():
        checks["notebook_execution"] = {"passed": False, "error": "tables/execution.json missing"}
        all_passed = False
    else:
        exec_data = json.loads(exec_file.read_text())
        expected_nbs = [
            "01_first_look.ipynb",
            "02_host_economy.ipynb",
            "03_price_distribution.ipynb",
            "04_room_type_price.ipynb",
            "05_rental_model.ipynb",
            "06_short_stay_geography.ipynb",
            "07_monthly_stay_cost.ipynb",
            "08_price_regression.ipynb",
            "09_price_guest_activity.ipynb",
        ]
        statuses = {item["notebook"]: item["status"] for item in exec_data}
        nb_ok = len(exec_data) == 9 and all(statuses.get(nb) == "passed" for nb in expected_nbs)
        checks["notebook_execution"] = {
            "passed": nb_ok,
            "total_executed": len(exec_data),
            "passed_notebooks": [nb for nb in expected_nbs if statuses.get(nb) == "passed"],
        }
        if not nb_ok:
            all_passed = False

    # 2. Output tables
    required_tables = [
        "data_audit",
        "study02_host_shares",
        "study02_ratings",
        "study02_room_composition",
        "study02_top5",
        "study02_weighting",
        "study03_price_stats",
        "study03_price_test",
        "study03_spain_comparison",
        "study04_discounts",
        "study04_room_stats",
        "study04_tests",
        "study05_districts",
        "study05_licence",
        "study05_missing_calendar",
        "study05_missing_price",
        "study05_reviews_by_model",
        "study05_summary",
        "study06_city_summary",
        "study06_join_audit",
        "study06_neighbourhoods",
        "study06_top_neighbourhoods",
        "study07_filter_audit",
        "study07_monthly_cost",
        "study07_quote_dates",
        "study07_quote_months",
        "study08_coefficients",
        "study08_filter_audit",
        "study08_fit",
        "study09_filter_audit",
        "study09_spearman",
    ]
    missing_tables = [t for t in required_tables if not (TABLES / f"{t}.csv").exists()]
    checks["tables"] = {
        "passed": len(missing_tables) == 0,
        "count_present": len(required_tables) - len(missing_tables),
        "total_required": len(required_tables),
        "missing": missing_tables,
    }
    if missing_tables:
        all_passed = False

    # 3. Figures
    required_figures = [
        "study2_host_concentration.png",
        "study2_ratings_comparison.png",
        "study2_room_type_by_segment.png",
        "study3_price_boxplots_and_outliers.png",
        "study3_price_distribution_histograms.png",
        "study4_privacy_premium_and_discount.png",
        "study4_room_type_boxplots_by_city.png",
        "study05_rental_model_share_all.png",
        "study06_short_entire_barcelona.png",
        "study06_short_entire_madrid.png",
        "study07_monthly_cost.png",
        "study08_coefficients.png",
        "study08_residuals.png",
        "study09_price_activity.png",
    ]
    missing_figs = [f for f in required_figures if not (FIGURES / f).exists()]
    checks["figures"] = {
        "passed": len(missing_figs) == 0,
        "count_present": len(required_figures) - len(missing_figs),
        "total_required": len(required_figures),
        "missing": missing_figs,
    }
    if missing_figs:
        all_passed = False

    # 4. Interactive Maps
    required_maps = [
        "study05_monthly_share_barcelona.html",
        "study05_monthly_share_madrid.html",
        "study05_monthly_share_los_angeles.html",
        "study05_monthly_share_new_york.html",
        "study05_monthly_share_tokyo.html",
        "study05_monthly_share_mexico_city.html",
    ]
    missing_maps = [m for m in required_maps if not (MAPS / m).exists()]
    checks["interactive_maps"] = {
        "passed": len(missing_maps) == 0,
        "count_present": len(required_maps) - len(missing_maps),
        "total_required": len(required_maps),
        "missing": missing_maps,
    }
    if missing_maps:
        all_passed = False

    # 5. Statistical & Model Verifications
    # 5a. Regression (Study 08)
    fit_df = pd.read_csv(TABLES / "study08_fit.csv")
    coef_df = pd.read_csv(TABLES / "study08_coefficients.csv")
    rank_ok = int(fit_df["rank"].iloc[0]) == int(fit_df["columns"].iloc[0]) == 8
    cond_ok = fit_df["condition_number"].iloc[0] < 100
    coef_finite = coef_df[["coefficient", "std_error_HC3", "ci_low", "ci_high"]].notna().all().all()
    checks["study08_regression"] = {
        "passed": bool(rank_ok and cond_ok and coef_finite),
        "rank": int(fit_df["rank"].iloc[0]),
        "columns": int(fit_df["columns"].iloc[0]),
        "condition_number": round(float(fit_df["condition_number"].iloc[0]), 2),
        "r_squared": round(float(fit_df["r_squared"].iloc[0]), 4),
        "n": int(fit_df["n"].iloc[0]),
        "all_coefficients_finite": bool(coef_finite),
    }
    if not (rank_ok and cond_ok and coef_finite):
        all_passed = False

    # 5b. Spearman correlation (Study 09)
    spearman_df = pd.read_csv(TABLES / "study09_spearman.csv")
    spearman_ok = len(spearman_df) == 4 and spearman_df["rho"].notna().all() and spearman_df["p_value"].notna().all()
    checks["study09_spearman"] = {
        "passed": bool(spearman_ok),
        "samples_evaluated": len(spearman_df),
        "correlations": {
            f"{row.city}_{row['sample']}": {"n": int(row.n), "rho": round(float(row.rho), 4)}
            for _, row in spearman_df.iterrows()
        },
    }
    if not spearman_ok:
        all_passed = False

    # 5c. Geographic joins (Study 06)
    joins_df = pd.read_csv(TABLES / "study06_join_audit.csv")
    unmatched_total = int(joins_df["unmatched"].sum())
    joins_ok = unmatched_total == 0
    checks["study06_geographic_joins"] = {
        "passed": bool(joins_ok),
        "unmatched_neighbourhoods": unmatched_total,
        "cities": joins_df["city"].tolist(),
    }
    if not joins_ok:
        all_passed = False

    # 6. Report PDF & LaTeX
    pdf_path = REPORT / "report.pdf"
    if not pdf_path.exists():
        checks["pdf_report"] = {"passed": False, "error": "report/report.pdf missing"}
        all_passed = False
    else:
        reader = pypdf.PdfReader(str(pdf_path))
        num_pages = len(reader.pages)
        pages_with_qmark = []
        for i, page in enumerate(reader.pages):
            txt = page.extract_text() or ""
            if "??" in txt:
                pages_with_qmark.append(i + 1)
        pdf_ok = (15 <= num_pages <= 22) and (len(pages_with_qmark) == 0)
        checks["pdf_report"] = {
            "passed": pdf_ok,
            "page_count": num_pages,
            "page_budget_range": "15-22",
            "file_size_bytes": pdf_path.stat().st_size,
            "unresolved_references": pages_with_qmark,
        }
        if not pdf_ok:
            all_passed = False

    # Write verification report
    verification_summary = {
        "overall_status": "PASSED" if all_passed else "FAILED",
        "checks": checks,
    }
    (REPORT / "verification.json").write_text(json.dumps(verification_summary, indent=2) + "\n")

    print("=" * 60)
    print(f"DELIVERY VERIFICATION: {verification_summary['overall_status']}")
    print("=" * 60)
    for check_name, check_res in checks.items():
        status_str = "PASS" if check_res.get("passed") else "FAIL"
        print(f"[{status_str}] {check_name}: {check_res}")
    print("=" * 60)
    print(f"Saved verification log to {REPORT / 'verification.json'}")

    if not all_passed:
        sys.exit(1)


if __name__ == "__main__":
    verify_all()
