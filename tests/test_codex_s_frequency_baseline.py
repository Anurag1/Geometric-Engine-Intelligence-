import tempfile
import unittest
from pathlib import Path

from benchmarks.run_codex_s_frequency_baseline import evaluate, read_triples


class CoDExFrequencyBaselineTests(unittest.TestCase):
    def setUp(self):
        self.train = [
            ("a", "r", "x"),
            ("b", "r", "x"),
            ("c", "r", "y"),
        ]
        self.test = [
            ("q", "r", "x"),
            ("q", "r", "z"),
            ("q", "unseen_relation", "x"),
        ]

    def test_metrics_and_unseen_relation_skip_are_reported(self):
        result = evaluate(self.train, self.test, limit=10, seed=42)
        self.assertEqual(result["sampled_test_triples"], 3)
        self.assertEqual(result["evaluated_triples"], 2)
        self.assertEqual(result["skipped_no_relation_training_examples"], 1)
        self.assertEqual(result["MRR"], 0.666667)
        self.assertEqual(result["Hits@1"], 0.5)
        self.assertEqual(result["Hits@10"], 1.0)

    def test_seed_makes_sampling_deterministic(self):
        first = evaluate(self.train, self.test, limit=2, seed=7)
        second = evaluate(self.train, self.test, limit=2, seed=7)
        self.assertEqual(first, second)

    def test_limit_is_respected(self):
        result = evaluate(self.train, self.test, limit=1, seed=42)
        self.assertEqual(result["sampled_test_triples"], 1)

    def test_reader_accepts_tab_separated_triples(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "triples.txt"
            path.write_text("head\trelation\ttail\n", encoding="utf-8")
            self.assertEqual(read_triples(path), [("head", "relation", "tail")])

    def test_reader_rejects_malformed_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.txt"
            path.write_text("head\trelation\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_triples(path)

    def test_reader_rejects_empty_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "empty.txt"
            path.write_text("\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_triples(path)


if __name__ == "__main__":
    unittest.main()
