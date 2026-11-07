"""Automated sanity checks for the synthetic Arabic teaching example."""
import csv
from pathlib import Path
import tempfile
import unittest

from analysis import (bh_adjust, count_tokens, keyness_rows, kwic_rows,
                      likelihood_ratio, normalize_arabic, read_documents, run, tokenize)

HERE = Path(__file__).resolve().parents[1]

class ArabicCorpusTests(unittest.TestCase):
    def test_arabic_normalisation_is_explicit(self):
        self.assertEqual(normalize_arabic("الْبَيَانَاتــ"), "البيانات")
        self.assertEqual(tokenize("أثر، اثر؛ وإثر!"), ["أثر", "اثر", "وإثر"])
        self.assertEqual(tokenize("أثر، اثر؛ وإثر!", fold_alef=True), ["اثر", "اثر", "واثر"])
        self.assertEqual(tokenize("المكتبة مكتبة"), ["المكتبة", "مكتبة"])

    def test_log_likelihood_against_known_value(self):
        # Independently checked using scipy.stats.chi2_contingency(..., correction=False).
        self.assertAlmostEqual(likelihood_ratio(7, 100, 3, 100), 1.7298743181, places=5)
        self.assertEqual(likelihood_ratio(2, 10, 2, 10), 0.0)
        self.assertGreater(likelihood_ratio(10, 10, 0, 10), 0)
        with self.assertRaises(ValueError):
            likelihood_ratio(11, 10, 1, 10)

    def test_keyness_and_bh(self):
        rows = keyness_rows(count_tokens(read_documents(HERE / "data" / "focus.csv")),
                            count_tokens(read_documents(HERE / "data" / "reference.csv")))
        self.assertGreater(len(rows), 20)
        assert all(0 <= row["bh_q_exploratory"] <= 1 for row in rows)
        self.assertEqual(bh_adjust([0.01, 0.04, 0.03]), [0.03, 0.04, 0.04])
        focus_key = next(x for x in rows if x["word"] == "البيانات")
        self.assertEqual(focus_key["direction"], "focus")
        self.assertGreater(focus_key["focus_count"], focus_key["reference_count"])

    def test_kwic_never_crosses_document_boundaries(self):
        docs = [{"doc_id": "A", "text": "أقرأ البيانات بعناية"},
                {"doc_id": "B", "text": "الوثائق في الأرشيف"}]
        lines = kwic_rows(docs, "البيانات", corpus_label="focus", window=8)
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0]["left"], "أقرأ")
        self.assertEqual(lines[0]["right"], "بعناية")
        self.assertNotIn("الوثائق", lines[0]["right"])
        with self.assertRaises(ValueError):
            kwic_rows(docs, "البيانات والوثائق", corpus_label="focus")

    def test_reproducible_csv_exports(self):
        with tempfile.TemporaryDirectory() as tmp:
            summary = run(HERE / "data" / "focus.csv", HERE / "data" / "reference.csv",
                          Path(tmp), query="البيانات")
            self.assertEqual(summary["focus_documents"], 12)
            self.assertEqual(summary["reference_documents"], 12)
            self.assertEqual(summary["focus_tokens"], 108)
            self.assertEqual(summary["reference_tokens"], 97)
            self.assertEqual(summary["tested_word_types"], 158)
            self.assertEqual(summary["kwic_hits"], 7)
            for name in ("focus_frequencies.csv", "reference_frequencies.csv", "keyness.csv", "kwic.csv"):
                self.assertTrue((Path(tmp) / name).exists())
            with (Path(tmp) / "kwic.csv").open(encoding="utf-8-sig", newline="") as fh:
                self.assertEqual(sum(1 for _ in csv.DictReader(fh)), summary["kwic_hits"])

if __name__ == "__main__":
    unittest.main()
