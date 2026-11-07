"""Demonstration: synthetic social-media-style data to Gephi edge table.

No live API, scraped material, or real social-media users are involved.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"
OUT.mkdir(exist_ok=True)

posts = pd.read_csv(HERE / "data" / "synthetic_posts.csv", parse_dates=["created_at"])
required = {"post_id", "author", "mentioned_account", "created_at", "likes", "reposts"}
missing = required - set(posts.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")
if posts["post_id"].duplicated().any():
    raise ValueError("post_id must be unique")
if posts["created_at"].isna().any():
    raise ValueError("created_at contains missing or invalid timestamps")
for field in ("likes", "reposts"):
    if posts[field].isna().any() or (posts[field] < 0).any():
        raise ValueError(f"{field} must be non-missing and non-negative")

posts["date"] = posts["created_at"].dt.date
posts["engagement"] = posts["likes"] + posts["reposts"]

activity = posts.groupby("date").size().reset_index(name="post_count")
engagement = (
    posts.groupby("author", as_index=False)
    .agg(posts=("post_id", "count"), total_engagement=("engagement", "sum"))
    .sort_values(["total_engagement", "author"], ascending=[False, True])
)

mentions = posts.dropna(subset=["author", "mentioned_account"]).copy()
mentions = mentions.loc[
    mentions["author"].str.strip().ne("")
    & mentions["mentioned_account"].str.strip().ne("")
]
edges = (
    mentions.groupby(["author", "mentioned_account"], as_index=False)
    .size()
    .rename(columns={"author": "Source", "mentioned_account": "Target", "size": "Weight"})
)
activity.to_csv(OUT / "activity_by_day.csv", index=False)
engagement.to_csv(OUT / "engagement_by_author.csv", index=False)
edges.to_csv(OUT / "gephi_edges.csv", index=False)

ax = activity.plot(x="date", y="post_count", kind="bar", legend=False, figsize=(7, 4))
ax.set_xlabel("Date")
ax.set_ylabel("Number of posts")
ax.set_title("Synthetic activity by day")
plt.tight_layout()
plt.savefig(OUT / "activity_by_day.png", dpi=160)
plt.close()

print(f"Processed {len(posts)} fictional posts; produced {len(edges)} unique directed edges.")
