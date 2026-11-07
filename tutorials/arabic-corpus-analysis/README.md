# Arabic Corpus Analysis: Frequencies, Keyness and KWIC

**A new, synthetic-data teaching demonstration · Dr Eva Ferron's Digital Research Methods portfolio**

**Privacy:** Every sentence in the supplied CSV files was created specifically for this tutorial. **No Twitter/X data, account names, posts, archival extracts, or research participant identifiers have been copied from the doctoral research.** The private Colab notebooks informed a *methodological review* only; their protected datasets, outputs and source file paths have **not** been published.

**Status:** A tested, AI-assisted draft for independent scholarly and teaching review. Not a previously delivered EFI/CDCS workshop, peer-reviewed method, or reproduction of the doctoral results.

## Learning outcomes

1. Read small UTF-8 Arabic document corpora and calculate raw and normalised word frequencies.
2. Explain and apply a consistent surface-word tokenisation and Arabic normalisation policy.
3. Compare target (**focus**) and **reference** corpus frequencies using a 2×2 log-likelihood (G²) statistic.
4. Distinguish a statistical comparison from an **effect size**: adjusted log₂ rate ratio.
5. Recognise the limitations of approximate p-values, multiple testing and small/unrepresentative datasets.
6. Explore exact word forms in a **keyword-in-context (KWIC)** concordance.

## Why this example is safe

The two datasets contain **12 invented sentences each**: one set discusses digital research workshops; the other discusses historical archives and reading. These are examples of *different genres* chosen to make the mechanics easy to see, not empirical samples of the world. Do not present apparent keyword differences as scientifically established findings.

| Dataset | Invented documents | Word tokens with default settings |
| --- | ---: | ---: |
| `data/focus.csv` | 12 | 108 |
| `data/reference.csv` | 12 | 97 |

No internet connection, API credentials, or external packages are required for the Python script.

## Run locally

Use Python **3.10 or later**. Download or clone this repository, open a terminal **in this tutorial folder**, then run:

```bash
python analysis.py
python -m unittest discover -s tests -v
```

You should see **158 compared word types** and **7 KWIC occurrences** for the example search `البيانات`, with **five passing tests**. The script writes four CSV files to an ignored `outputs/` directory:

- `focus_frequencies.csv`, `reference_frequencies.csv`: counts and rates per 10,000 word tokens;
- `keyness.csv`: frequencies, G², approximate p-values, exploratory Benjamini–Hochberg q-values, adjusted log₂ rate ratios, and which corpus has a higher raw rate;
- `kwic.csv`: one line for each exact matching occurrence, with a document identifier and four words of left/right context.

To search another **single surface word**, use `python analysis.py --query "الوثائق"`. To alter the context width, add `--window 6`. Use `--fold-alef` **only if your research protocol justifies merging** `آ / أ / إ / ٱ` with `ا`.

### Optional Google Colab

[Open the companion notebook](colab_walkthrough.ipynb) or use the [Open in Colab link](https://colab.research.google.com/github/s1112124/digital-research-methods/blob/main/tutorials/arabic-corpus-analysis/colab_walkthrough.ipynb). It downloads **this public repository only**, runs the synthetic script and displays example output tables. The notebook does not mount Google Drive or request access to private research files.

## Tokenisation decisions

This is deliberately a **transparent surface-word baseline**, not a complete Arabic morphological parser.

- Normalises Unicode compatibility forms (NFKC), removes Arabic **diacritics** and **tatweel** (`ـ`).
- Keeps **hamza/alef variants**, `ة` and `ى` distinct by default. Optional `--fold-alef` merges four alef spellings.
- Extracts sequences of Arabic letters; does **not** segment `و`-, `ب`-, `ل`- prefixes or separate attached definite articles, stem words, remove stopwords or resolve spelling variants automatically.
- Does not implement platform-specific cleaning of hashtags, mixed-script content or links. **It is not a plug-and-play pipeline for real Twitter/X datasets.**
- KWIC searches **one exact normalised token** and shows context in token units. It never crosses document boundaries and is **not** a substitute for AntConc's richer concordancer or a discourse analysis.

Normalisation is an analytical choice that can erase meaningful distinctions; compare alternatives before applying the method to historical or theological Arabic.

## What keyness measures — and what it does not

For each word, the script constructs a **2×2 table** of word/non-word occurrences in the focus and reference corpora and calculates **G² = 2 Σ O ln(O/E)**, treating zero-observed cells as contributing zero. It also reports an adjusted log₂ rate ratio for the **magnitude and direction** of relative usage (with a 0.5 count correction), plus normalised frequency per 10,000 tokens.

- **Log-likelihood** is a test statistic: a high score does not automatically mean a substantively important difference.
- **Adjusted log₂ rate ratio** is an effect size: with rare words it can be unstable.
- **Approximate p-values** use a chi-square(1) approximation; sparse cells, repeated words within documents and these tiny illustrative corpora undermine the usual inference assumptions.
- **Benjamini–Hochberg q-values** are calculated over *all 158 tested word types*, but they do not resolve dependence, sampling bias, genre mismatch or sparse data. Do not treat them as proof of significance.
- **Reference-corpus selection** and genre/register differences can dominate keyness results. Here the contrasts are purposefully designed, so **none of the numbers is evidence about real language populations**.

The original research notebook included an earlier LL routine and different Arabic cleaning decisions. This tutorial reimplements the comparison with **one consistent counting pathway** and documents choices explicitly. It does not reproduce, validate or publish the original doctoral findings.

## Guided workshop activity

1. **Inspect:** Compare `F01` and `R01` in the CSV files. Which aspects of their invented topics might predict different frequencies?
2. **Count:** Find `البيانات` in `focus_frequencies.csv`; check how raw frequency differs from relative frequency.
3. **Compare:** Open `keyness.csv`. Contrast G² ranking and adjusted log₂ rate ratio. Which word types are high on one measure but not the other, and why?
4. **Investigate:** Read the seven example KWIC lines for `البيانات`. What questions do they prompt that frequency alone cannot answer?
5. **Experiment:** Run with and without `--fold-alef`. Observe changes in counts and explain possible analytic costs.
6. **Critique:** Explain why the apparent statistical differences do not establish general claims. Consider document clustering, size, metadata, representativeness and multiple comparisons.
7. **Extend:** Add a third **invented** document to the focus corpus, rerun tests and inspect which outputs change. For a more advanced exercise, replace the tokenizer with a documented Arabic morphological segmenter and evaluate its impact.

## Reference methods

- UCREL (Lancaster University), [Log-likelihood and effect-size calculator](https://ucrel.lancaster.ac.uk/llwizard.html).
- Lancaster University's [Corpus Linguistics: Method, Theory and Practice — Statistical Comparisons](https://corpora.lancs.ac.uk/clmtp/2-stat.php).
- The `corpora` R package [keyness documentation](https://search.r-project.org/CRAN/refmans/corpora/html/keyness.html) describes G² and corrected log-ratio methods.
- Laurence Anthony, [AntConc Concordance documentation](https://antconc-manual.readthedocs.io/en/latest/concordance.html).

These resources informed the teaching explanation. The code and synthetic example are newly produced; this is **not** an implementation of AntConc itself.

## Ethics, attribution and current limitations

The original Saudi Twitter/X data and research notebooks remain private under the project's ethics constraints. **Do not copy protected records into this repository** or replace invented example text with real tweets. Any adapted future release would require separate permission and a documented disclosure review.

This tutorial was drafted with AI assistance for Dr Eva Ferron's research-methods portfolio. Its underlying statistical calculation has been independently cross-checked against SciPy on known test tables; automated checks cover normalisation, token matching, output generation and adjusted values. It has **not** been field-tested with learners or externally peer reviewed.

[Back to the main portfolio](../../README.md).
