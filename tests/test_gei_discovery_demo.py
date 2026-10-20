import unittest

from examples.gei_discovery_demo import rank_candidates, validate_dataset


DATA = {
    "claims": [
        {"id": "a", "title": "Sleep timing and attention", "domain": "sleep"},
        {"id": "b", "title": "Attention under sleep restriction", "domain": "cognition"},
        {"id": "c", "title": "Soil moisture and crop growth", "domain": "agriculture"},
    ],
    "known_edges": [["a", "b"]],
}


class DiscoveryDemoTests(unittest.TestCase):
    def test_known_edges_are_excluded(self):
        candidates = rank_candidates(DATA)
        pairs = {(row["left_id"], row["right_id"]) for row in candidates}
        self.assertNotIn(("a", "b"), pairs)

    def test_only_unknown_pairs_are_returned(self):
        self.assertEqual(len(rank_candidates(DATA)), 2)

    def test_order_is_deterministic(self):
        self.assertEqual(rank_candidates(DATA), rank_candidates(DATA))

    def test_top_k_is_respected(self):
        self.assertEqual(len(rank_candidates(DATA, top_k=1)), 1)

    def test_rejects_unknown_edge_endpoint(self):
        invalid = {"claims": DATA["claims"], "known_edges": [["a", "missing"]]}
        with self.assertRaises(ValueError):
            validate_dataset(invalid)

    def test_rejects_duplicate_ids(self):
        invalid = {"claims": [DATA["claims"][0], DATA["claims"][0]], "known_edges": []}
        with self.assertRaises(ValueError):
            validate_dataset(invalid)

    def test_rejects_zero_top_k(self):
        with self.assertRaises(ValueError):
            rank_candidates(DATA, top_k=0)


if __name__ == "__main__":
    unittest.main()
