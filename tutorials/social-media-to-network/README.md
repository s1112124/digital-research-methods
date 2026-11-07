# From Synthetic Platform Data to Social Network Analysis

**Audience:** Humanities and social science researchers who want a practical introduction to transforming structured records into a simple, interpretable network.

**Status:** Draft, standalone teaching example. The synthetic dataset and script have been used to demonstrate the workflow; **Gephi compatibility and learner-facing instructions still require independent classroom testing**. This has not been delivered as an EFI/CDCS course.

## Learning outcomes

By the end of the exercise you should be able to:

1. Read a structured CSV using Python and pandas.
2. Check basic data requirements and summarise activity and engagement.
3. Construct a directed, weighted edge list of account mentions.
4. Import the edge list into Gephi for network visualisation.
5. Distinguish computational measures from substantive claims about influence.

## Requirements

- Python 3.10 or later
- pandas and matplotlib (see `requirements.txt`)
- Gephi (optional for the final network visualisation activity)

## Run the Python exercise

Download this repository, open a terminal and change into this tutorial folder. Then run:

```bash
python -m pip install -r requirements.txt
python activity_to_network.py
```

The script reads `data/synthetic_posts.csv` and generates an `outputs/` folder containing:

| Generated file | Purpose |
| --- | --- |
| `activity_by_day.csv` | Number of posts on each date |
| `engagement_by_author.csv` | Posts and total likes-plus-reposts by fictional author |
| `gephi_edges.csv` | Directed mentions network: Source, Target and Weight |
| `activity_by_day.png` | Plot of posting frequency |

A successful run should report **12 fictional posts** and **10 unique directed edges**. To verify the output structure, run:

```bash
python tests/check_outputs.py
```

## Guided exercise

1. **Inspect the input.** Identify `author`, `mentioned_account`, `created_at`, `likes` and `reposts`. Are these fields sufficient for your own research question?
2. **Run the code.** Find the operations that check for duplicate IDs, extract dates, create an engagement measure and group records.
3. **Inspect the output.** Which account receives the greatest number of recorded mentions? Does this account also have the highest engagement?
4. **Use Gephi.** In the Data Laboratory, import `outputs/gephi_edges.csv` as an **Edges table**, ensuring the graph is **directed** and the numerical `Weight` column is correctly interpreted. Visualise the graph and compare indegree and weighted indegree.
5. **Test an assumption.** Modify a fictional record and regenerate the outputs. Explain what changed and why.
6. **Interpret cautiously.** Does a higher mention count establish political or social influence? What additional evidence might be needed?

## Source and ethics

Every actor and record in this dataset is invented for teaching. It does not depend on live APIs and contains no real social-media user information. The activity is **not** a demonstration of current API-based data acquisition. For real datasets, consider data licensing, platform restrictions, sampling, missingness, privacy and potential participant exposure.

## Technical and educational limitations

The edge list models **mentions**, not friendships, follows or retweets. It uses one edge for each observed author–mentioned-account relationship with `Weight` equal to the number of observations. The small dataset cannot support substantive claims about social or political networks. The exercise has not been independently validated in a formal teaching session.

The material was prepared with AI assistance for Dr Eva Ferron's review and adaptation. It is **not peer reviewed**, and no institutional affiliation or endorsement is implied.

[Back to the research methods portfolio](../../README.md)
