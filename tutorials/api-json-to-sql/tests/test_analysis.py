"""Tests for the synthetic, offline JSON → pandas → SQLite exercise."""
from pathlib import Path
import json
import tempfile
import unittest

from analysis import load_and_clean, summarise_with_sql, run

HERE = Path(__file__).resolve().parents[1]

class OfflinePipelineTests(unittest.TestCase):
    def test_cleaning_policy_and_sql(self):
        clean, report = load_and_clean(HERE / "data" / "sample_api_response.json")
        self.assertEqual(report["input_rows"], 10)
        self.assertEqual(report["duplicate_ids_discarded"], 1)
        self.assertEqual(report["rows_missing_valid_timestamp_or_author"], 2)
        self.assertEqual(report["cleaned_rows"], 7)
        self.assertEqual(report["engagement_unavailable_rows"], 2)
        self.assertEqual(len(clean["id"].unique()), 7)
        summary = summarise_with_sql(clean)
        self.assertEqual(int(summary["posts"].sum()), 7)
        self.assertEqual(int(summary["posts_missing_engagement"].sum()), 2)
        self.assertEqual(int(summary.loc[summary["author"] == "archive_a", "posts"].iloc[0]), 3)

    def test_reproducible_outputs(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            report = run(HERE / "data" / "sample_api_response.json", folder)
            self.assertEqual(report["cleaned_rows"], 7)
            for name in ("cleaned_posts.csv", "author_summary.csv", "data_quality_report.json"):
                self.assertTrue((folder / name).is_file())
            self.assertEqual(json.loads((folder / "data_quality_report.json").read_text())["input_rows"], 10)

    def test_bad_schema_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            bad_file = Path(temp) / "bad.json"
            bad_file.write_text('{"not_data": []}')
            with self.assertRaises(ValueError):
                load_and_clean(bad_file)

if __name__ == "__main__":
    unittest.main()
