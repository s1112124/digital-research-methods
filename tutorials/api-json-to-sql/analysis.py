"""Offline example: synthetic API-style JSON, pandas cleaning and SQLite."""
from pathlib import Path
import argparse
import json
import sqlite3

import pandas as pd

REQUIRED = {"id", "author", "created_at", "likes", "reposts"}

def load_and_clean(path: Path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = payload.get("data")
    if not isinstance(records, list):
        raise ValueError("Expected a JSON object containing a 'data' list")
    raw = pd.DataFrame.from_records(records)
    missing = REQUIRED - set(raw.columns)
    if missing:
        raise ValueError(f"Required fields missing: {sorted(missing)}")

    dedup = raw.drop_duplicates(subset="id", keep="last").copy()
    duplicate_records = len(raw) - len(dedup)
    dedup["created_at"] = pd.to_datetime(dedup["created_at"], errors="coerce", utc=True)
    dedup["author"] = dedup["author"].astype("string").str.strip()
    bad_date = dedup["created_at"].isna()
    bad_author = dedup["author"].isna() | dedup["author"].eq("")
    invalid_rows = bad_date | bad_author
    clean = dedup.loc[~invalid_rows].copy()

    for col in ("likes", "reposts"):
        clean[col] = pd.to_numeric(clean[col], errors="coerce")
        clean[col] = clean[col].where(clean[col] >= 0)
    # Do not treat missing or invalid engagement as zero.
    clean["engagement"] = clean["likes"] + clean["reposts"]
    clean["created_at"] = clean["created_at"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    report = {
        "input_rows": int(len(raw)),
        "duplicate_ids_discarded": int(duplicate_records),
        "rows_missing_valid_timestamp_or_author": int(invalid_rows.sum()),
        "cleaned_rows": int(len(clean)),
        "engagement_unavailable_rows": int(clean["engagement"].isna().sum()),
        "policy": "keep last duplicate ID; drop records lacking author/date; mark invalid likes/reposts as missing, not zero"
    }
    return clean, report

def summarise_with_sql(clean: pd.DataFrame) -> pd.DataFrame:
    with sqlite3.connect(":memory:") as con:
        clean.to_sql("posts", con, index=False, if_exists="replace")
        return pd.read_sql_query(
            """SELECT author, COUNT(*) AS posts,
                      COUNT(engagement) AS posts_with_observed_engagement,
                      SUM(engagement) AS observed_engagement_total,
                      SUM(CASE WHEN engagement IS NULL THEN 1 ELSE 0 END)
                          AS posts_missing_engagement
               FROM posts
               GROUP BY author
               ORDER BY posts DESC, author ASC""", con)

def run(input_file: Path, output_dir: Path) -> dict:
    clean, report = load_and_clean(input_file)
    summary = summarise_with_sql(clean)
    output_dir.mkdir(parents=True, exist_ok=True)
    clean.to_csv(output_dir / "cleaned_posts.csv", index=False)
    summary.to_csv(output_dir / "author_summary.csv", index=False)
    (output_dir / "data_quality_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Offline JSON to pandas to SQLite")
    here = Path(__file__).resolve().parent
    parser.add_argument("--input", type=Path, default=here / "data" / "sample_api_response.json")
    parser.add_argument("--output", type=Path, default=here / "outputs")
    args = parser.parse_args()
    print(json.dumps(run(args.input, args.output), indent=2))
