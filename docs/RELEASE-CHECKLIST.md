# Release and DOI checklist

Use this checklist **after** the tutorials have been taught or otherwise evaluated and are ready for a stable public version. It does **not** claim that a version 1.0 release, classroom evaluation or DOI already exists.

## 1. Before a stable GitHub release

- [ ] Review the scope of the tutorials and confirm intended learning outcomes.
- [ ] Complete at least one teaching or learner evaluation and record non-identifying improvements in [Teaching evaluation](TEACHING-EVALUATION.md), or explicitly state if the first release is based on another evaluation method.
- [ ] Resolve feedback and ensure teaching instructions match the current code.
- [ ] Run every tutorial from a fresh environment: dependencies, example data, outputs and automated tests.
- [ ] Validate the Arabic normalisation choices, LL keyness results, interpretation of p-values and KWIC behaviour.
- [ ] Check usability and accessibility of instructions, exercises and Colab links.
- [ ] Review all files **and relevant Git history** for protected or identifying material. Do not publish any restricted social-media data.
- [ ] Confirm any third-party assets, excerpts and software dependencies are licensed appropriately.
- [ ] Recheck the [MIT code licence](../LICENSE) and [CC BY 4.0 teaching-material licence](../LICENSE-CONTENT.md) against the final content.
- [ ] Confirm [CITATION.cff](../CITATION.cff) contains the correct title, author, ORCID and eventual version metadata.
- [ ] Write accurate change notes in [CHANGELOG.md](../CHANGELOG.md).

## 2. Publish a stable version only when ready

1. In GitHub, open **Releases → Draft a new release**.
2. Select the reviewed commit on `main`, create an appropriate tag (for example, `v1.0.0`), and include the release notes. Do not tag an unreviewed state.
3. Check the release's source archive contains only intended public assets, then publish it.
4. Update `CITATION.cff` to reflect the *actual* tagged version and release date; if doing this after creating the tag, record the citation metadata on the next commit or make it part of the tag preparation.

GitHub guidance: https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository

## 3. Archive the release and obtain a DOI

1. Sign in to **Zenodo** and link the intended GitHub account.
2. Open Zenodo's GitHub integration, synchronise the repositories and enable `s1112124/digital-research-methods`.
3. Release a new tagged version **after** Zenodo integration is enabled (or use Zenodo's manual deposition route if a release already predates activation).
4. Verify that Zenodo archived the **correct public version**, including title, author, ORCID, licence information, description and DOI.
5. Add the verified DOI to `CITATION.cff` and the GitHub README. If Zenodo supplies both a version-specific DOI and an all-versions DOI, use the appropriate one for the intended citation.
6. Record the Zenodo URL and DOI in the changelog. Never invent a DOI or link to an unconfirmed deposit.

Zenodo guide: https://help.zenodo.org/docs/github/enable-repository/

## 4. Subsequent versions

Repeat validation and publish a new tag for materially revised materials. Keep existing DOI citations tied to the versions they identify; use the all-versions DOI for the evolving project when appropriate.
