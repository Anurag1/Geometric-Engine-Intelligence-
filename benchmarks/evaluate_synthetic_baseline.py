#!/usr/bin/env python3
"""Compare GEI ranking with seeded random ranking on an illustrative synthetic holdout.

This is a benchmark-harness smoke test, not evidence of scientific discovery.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from examples.gei_discovery_demo import rank_candidates, validate_dataset


def canonical(edge: list[str] | tuple[str, str]) -> tuple[str, str]:
    if not isinstance(edge, (list, tuple)) or len(edge) != 2 or not all(isinstance(x, str) for x in edge) or edge[0] == edge[1]:
        raise ValueError(f"Edges must contain two distinct string IDs: {edge}")
    return tuple(sorted(edge))


def precision_at_k(rows: list[dict[str, Any]], positives: set[tuple[str, str]], k: int) -> float:
    if k < 1 or k > len(rows):
        raise ValueError(f"k must be between 1 and candidate count ({len(rows)})")
    hits = sum(canonical((row["left_id"], row["right_id"])) in positives for row in rows[:k])
    return hits / k


def evaluate(data: dict[str, Any], k: int = 3, trials: int = 1000) -> dict[str, Any]:
    if trials < 1:
        raise ValueError("trials must be at least 1")
    claims, known = validate_dataset(data)
    raw_positives = data.get("held_out_positive_edges")
    if not isinstance(raw_positives, list) or not raw_positives:
        raise ValueError("'held_out_positive_edges' must be a non-empty list")
    positives = {canonical(edge) for edge in raw_positives}
    if len(positives) != len(raw_positives):
        raise ValueError("Duplicate held-out positive edge")
    for left, right in positives:
        if left not in claims or right not in claims:
            raise ValueError(f"Unknown claim ID in held-out edge: {(left, right)}")
        if (left, right) in known:
            raise ValueError(f"Held-out positives must not appear in known_edges: {(left, right)}")

    all_pairs = len(claims) * (len(claims) - 1) // 2
    ranked = rank_candidates(data, top_k=all_pairs)
    if k > len(ranked):
        raise ValueError(f"k={k} exceeds eligible candidate count ({len(ranked)})")
    heuristic_p_at_k = precision_at_k(ranked, positives, k)
    random_scores = []
    for seed in range(trials):
        shuffled = list(ranked)
        random.Random(seed).shuffle(shuffled)
        random_scores.append(precision_at_k(shuffled, positives, k))
    random_mean = sum(random_scores) / trials
    return {
        "benchmark": "synthetic_holdout",
        "warning": "Synthetic labels are illustrative only; this does not establish real-world or scientific performance.",
        "candidate_count": len(ranked),
        "held_out_positive_count": len(positives),
        "k": k,
        "random_trials": trials,
        "heuristic_precision_at_k": round(heuristic_p_at_k, 4),
        "random_baseline_mean_precision_at_k": round(random_mean, 4),
        "absolute_difference_vs_random_mean": round(heuristic_p_at_k - random_mean, 4),
        "random_draws_below_heuristic_fraction": round(sum(s < heuristic_p_at_k for s in random_scores) / trials, 4),
        "top_k_pairs": [
            {"left_id": row["left_id"], "right_id": row["right_id"], "score": row["score"],
             "held_out_positive": canonical((row["left_id"], row["right_id"])) in positives}
            for row in ranked[:k]
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="benchmarks/synthetic_holdout.json")
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
        result = evaluate(data, k=args.k, trials=args.trials)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
