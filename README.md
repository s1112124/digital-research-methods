# Digital Research Methods

**Dr Eva Ferron** · Digital politics · Computational social science · Research methods education

A collection of practical, reproducible tutorials for applying computational methods in the humanities and social sciences. Each tutorial connects a research question to data preparation, analysis and interpretation, with executable code and synthetic teaching datasets.

## Tutorials

### [1. From Synthetic Platform Data to Social Network Analysis](tutorials/social-media-to-network/README.md)

Use **Python, pandas and matplotlib** to clean structured records, analyse activity and engagement, and generate a weighted directed edge list for **Gephi**. The example begins with a prepared synthetic CSV dataset.

### [2. From API-style JSON to Validated Research Data](tutorials/api-json-to-sql/README.md)

Validate structured JSON, document data-quality decisions, process records with **pandas**, query them with **SQLite**, and test the resulting workflow. The exercise works offline using a fictional API-style response.

### [3. Arabic Corpus Analysis: Frequencies, Keyness and KWIC](tutorials/arabic-corpus-analysis/README.md)

Compare two invented Arabic-language corpora using a transparent tokenizer, relative frequencies, **log-likelihood (G²) keyness**, adjusted effect sizes and **keyword-in-context (KWIC)** concordances. Includes a [runnable Google Colab notebook](https://colab.research.google.com/github/s1112124/digital-research-methods/blob/main/tutorials/arabic-corpus-analysis/colab_walkthrough.ipynb).

## How to cite

If you use or adapt these resources in teaching or research, please cite:

> Ferron, Eva. 2026. *Digital Research Methods: Reproducible Synthetic-Data Tutorials*. GitHub. https://github.com/s1112124/digital-research-methods.

Use GitHub's **Cite this repository** option, powered by [`CITATION.cff`](CITATION.cff), for machine-readable citation details. Where possible, include the tutorial name and Git commit or tagged release so readers can identify the version you used. A version-specific DOI will be added following a reviewed release.

**ORCID:** [0000-0002-2269-7991](https://orcid.org/0000-0002-2269-7991)

## Licence and data

- **Software code and executable notebook cells:** [MIT Licence](LICENSE).
- **Original teaching text, notebook explanations and synthetic example datasets:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE-CONTENT.md).
- All supplied teaching datasets are **synthetic**. The tutorials do not include original research participant data.

You are welcome to use and adapt the materials under the relevant licence; please acknowledge the source and indicate changes.

## Development and evaluation

The tutorials are maintained as reusable teaching resources. Feedback from teaching and independent use can inform improvements; see the [teaching evaluation template](docs/TEACHING-EVALUATION.md), [changelog](CHANGELOG.md) and [release and DOI checklist](docs/RELEASE-CHECKLIST.md).

A stable, archived release and DOI are planned **after the resources have been evaluated and reviewed**.

## Research background

My research combines social network analysis with computational text analysis, including frequencies, keyness, collocations and concordances, to investigate digital platforms, political communication and authority.
