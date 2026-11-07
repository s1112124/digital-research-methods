"""Sanity checks for the generated outputs of the synthetic tutorial."""
from pathlib import Path
import csv

OUT = Path(__file__).resolve().parents[1] / "outputs"

def read_rows(name):
    with (OUT / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))

activity = read_rows("activity_by_day.csv")
engagement = read_rows("engagement_by_author.csv")
edges = read_rows("gephi_edges.csv")

assert sum(int(x["post_count"]) for x in activity) == 12, "Unexpected post count"
assert len(edges) == 10, "Unexpected number of unique directed edges"
assert len(engagement) == 4, "Unexpected number of authors"
assert all(int(x["Weight"]) >= 1 for x in edges), "Every recorded edge needs positive weight"
assert sum(int(x["Weight"]) for x in edges) == 12, "Unexpected total mention count"
assert (OUT / "activity_by_day.png").exists(), "Missing plotted output"

print("All synthetic tutorial output checks passed.")
