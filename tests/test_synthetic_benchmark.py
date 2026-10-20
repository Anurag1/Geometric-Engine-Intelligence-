import json
import unittest
from pathlib import Path

from benchmarks.evaluate_synthetic_baseline import evaluate

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "benchmarks" / "synthetic_holdout.json").read_text(encoding="utf-8"))


class SyntheticBaselineTests(unittest.TestCase):
    def test_returns_precision_and_random_baseline(self):
        result = evaluate(DATA, k=3, trials=100)
        self.assertEqual(result["candidate_count"], 26)
        self.assertEqual(result["held_out_positive_count"], 3)
        self.assertEqual(result["heuristic_precision_at_k"], 0.6667)
        self.assertIn("random_baseline_mean_precision_at_k", result)
        self.assertEqual(len(result["top_k_pairs"]), 3)

    def test_is_deterministic(self):
        self.assertEqual(evaluate(DATA, k=3, trials=100), evaluate(DATA, k=3, trials=100))

    def test_rejects_heldout_edge_already_known(self):
        invalid = dict(DATA)
        invalid["held_out_positive_edges"] = [DATA["known_edges"][0]]
        with self.assertRaises(ValueError):
            evaluate(invalid)

    def test_rejects_zero_trials(self):
        with self.assertRaises(ValueError):
            evaluate(DATA, trials=0)


if __name__ == "__main__":
    unittest.main()
