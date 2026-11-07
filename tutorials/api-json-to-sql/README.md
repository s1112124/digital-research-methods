# Supplementary tutorial: From API-style JSON to validated research data

**Status:** New, separately authored teaching example developed following an audit of completed 2023 Python coursework. It is **not** an original submission, marked exercise, delivered workshop or demonstration of current live API access. All data are invented.

## Why this exercise?

The earlier coursework demonstrates data retrieval, manipulation, statistical summaries and visualisation. This new exercise adds more explicit **data-quality reporting, validation, SQL integration and tests**, which make a research workflow easier for another researcher to inspect and reproduce.

## Learning outcomes

1. Understand the common structure of JSON returned by an API.
2. Validate expected fields and explicitly handle duplicate IDs, missing dates, absent authors and invalid engagement values.
3. Use **pandas** to clean and transform records while preserving evidence about missingness.
4. Create an in-memory **SQLite** table and write a SQL aggregation query.
5. Save outputs and a machine-readable quality report.
6. Test expected results using Python's built-in `unittest` framework.

## Run the exercise

From this directory, using Python 3.10+:

```bash
python -m pip install -r requirements.txt
python analysis.py
python -m unittest discover -s tests -v
```

The script creates `outputs/cleaned_posts.csv`, `outputs/author_summary.csv` and `outputs/data_quality_report.json`. The test runner should report **three passing tests**. With the supplied synthetic dataset, 10 initial records become 7 cleaned records: one duplicated ID is discarded and two records are excluded for a bad date or missing author. Two retained records have unavailable engagement; these are **not imputed as zero**.

## Research exercises

- Explain why `keep="last"` is a contestable decision when handling duplicate IDs. What would make a different policy defensible?
- Inspect the missing engagement counts. How would totals be biased if missing values were silently treated as zero?
- Change the input schema and observe the error. What kinds of upstream API changes could produce this failure?
- Examine the SQL query. What does `COUNT(engagement)` exclude that `COUNT(*)` includes?
- Extend the code to validate non-numeric post identifiers, or design a test for an empty input dataset.
- Outline how a *real* platform API would introduce authentication, pagination, rate limits, changing terms and research ethics considerations. This exercise makes **no live request**.

## Responsible reuse

**All accounts, IDs and records are fictional.** No real research participants, Twitter/X timelines, API credentials or restricted data are included.

The example is self-contained and was locally tested using the supplied fixture. It was drafted with AI assistance for Dr Eva Ferron's review and adaptation, and has not undergone peer review or live classroom testing. It should not be represented as evidence of past independent teaching or original coursework completion.

[Return to the Digital Research Methods portfolio](../../README.md).
