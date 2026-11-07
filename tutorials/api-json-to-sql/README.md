# From API-style JSON to Validated Research Data

**Example data:** A wholly synthetic JSON response, supplied with the tutorial. The analysis runs offline.

## Why this exercise?

Reliable data analysis requires explicit decisions about duplicate records, invalid values and missing information. This exercise demonstrates **data-quality reporting, validation, SQL integration and automated tests** to make a research workflow easier to inspect and reproduce.

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

## Scope and reuse

This exercise uses invented records to demonstrate processing of an API-style response; it does not contact an external service. If adapting the workflow to a real API, review its documentation, usage conditions and data protection requirements.

Please cite the [Digital Research Methods repository](../../README.md#how-to-cite) when using or adapting this tutorial. Code is licensed under [MIT](../../LICENSE), and the explanatory material and synthetic dataset under [CC BY 4.0](../../LICENSE-CONTENT.md).

[Return to the Digital Research Methods portfolio](../../README.md).
