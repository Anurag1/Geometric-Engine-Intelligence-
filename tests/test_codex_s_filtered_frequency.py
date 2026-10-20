import unittest

from benchmarks.run_codex_s_filtered_frequency import evaluate


class FilteredFrequencyBaselineTests(unittest.TestCase):
    def test_filtered_metrics_and_average_ties(self):
        train = [
            ("a", "r", "x"),
            ("b", "r", "x"),
            ("c", "r", "y"),
        ]
        valid = [("q", "r", "x")]
        test = [("q", "r", "z")]
        result = evaluate(train, valid, test)
        self.assertEqual(result["entities"], 7)
        self.assertEqual(result["train_triples"], 3)
        self.assertEqual(result["valid_triples"], 1)
        self.assertEqual(result["test_triples"], 1)
        # x is filtered as another known answer; y outranks z, while
        # a, b, c, and q tie with z at score zero. Average tie rank is 4.
        self.assertEqual(result["MRR"], 0.25)
        self.assertEqual(result["Hits@1"], 0.0)
        self.assertEqual(result["Hits@3"], 0.0)
        self.assertEqual(result["Hits@10"], 1.0)

    def test_filters_other_known_answers_for_query(self):
        train = [("q", "r", "x"), ("a", "r", "x"), ("b", "r", "y")]
        valid = [("q", "r", "y")]
        test = [("q", "r", "z")]
        result = evaluate(train, valid, test)
        self.assertEqual(result["evaluated_queries"], 1)
        self.assertEqual(result["entities"], 6)

    def test_rejects_empty_train_or_test(self):
        with self.assertRaises(ValueError):
            evaluate([], [], [("h", "r", "t")])
        with self.assertRaises(ValueError):
            evaluate([("h", "r", "t")], [], [])

    def test_results_are_deterministic(self):
        triples = [("a", "r", "x"), ("b", "r", "x"), ("c", "r", "y")]
        query = [("q", "r", "z")]
        self.assertEqual(evaluate(triples, [], query), evaluate(triples, [], query))


if __name__ == "__main__":
    unittest.main()
