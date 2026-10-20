#!/usr/bin/env python3
"""Small CoDEx-S link-prediction sanity benchmark for GEI's transparent heuristic.

Input files are the official CoDEx-S train/valid/test triple files:
one tab-separated head\trelation\ttail triple per line.
This script is a lightweight baseline comparison, not a reproduction of CoDEx
leaderboard results. It evaluates relation-specific head/tail completion and
compares the GEI lexical/domain-style score only where the candidate task is
defined; relation-aware graph baselines remain necessary for a fair full study.
"""
from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

def read_triples(path: Path) -> list[tuple[str, str, str]]:
    rows = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) != 3 or not all(parts):
            raise ValueError(f"{path}:{line_no}: expected head<TAB>relation<TAB>tail")
        rows.append(tuple(parts))
    if not rows:
        raise ValueError(f"No triples found in {path}")
    return rows

def reciprocal_rank(rank: int) -> float:
    return 1.0 / rank

def evaluate(train: list[tuple[str,str,str]], test: list[tuple[str,str,str]], limit: int = 500, seed: int = 42) -> dict:
    """Evaluate a simple frequency ranking on a deterministic test sample.

    For each test triple, rank the true tail among entities observed in training
    for the same relation. This is intentionally a simple relation-aware baseline.
    It is not a full filtered KGE evaluation; report this limitation explicitly.
    """
    tails_by_relation: dict[str, Counter] = defaultdict(Counter)
    known = set(train)
    entities = sorted({e for h,r,t in train for e in (h,t)})
    for h,r,t in train:
        tails_by_relation[r][t] += 1
    rng = random.Random(seed)
    sample = list(test)
    rng.shuffle(sample)
    sample = sample[:min(limit, len(sample))]
    ranks, reciprocal_ranks, hits1, hits10, skipped = [], [], 0, 0, 0
    for h, r, true_t in sample:
        counts = tails_by_relation.get(r, Counter())
        if not counts:
            skipped += 1
            continue
        # Candidate set consists of observed tails for the relation plus truth.
        candidates = set(counts)
        candidates.add(true_t)
        ordered = sorted(candidates, key=lambda e: (-counts[e], e))
        # Deterministic tie-breaking is lexical ID; this is a simple baseline.
        rank = ordered.index(true_t) + 1
        ranks.append(rank)
        reciprocal_ranks.append(reciprocal_rank(rank))
        hits1 += rank <= 1
        hits10 += rank <= 10
    n = len(ranks)
    return {
        "benchmark": "CoDEx-S",
        "method": "relation-tail-frequency baseline",
        "sampled_test_triples": len(sample),
        "evaluated_triples": n,
        "skipped_no_relation_training_examples": skipped,
        "MRR": round(sum(reciprocal_ranks)/n, 6) if n else None,
        "Hits@1": round(hits1/n, 6) if n else None,
        "Hits@10": round(hits10/n, 6) if n else None,
        "seed": seed,
        "limitations": [
            "Lightweight diagnostic only; not comparable to filtered all-entity KGE leaderboard metrics.",
            "Does not implement GEI's current pairwise heuristic because CoDEx is a typed, directed, multi-relational graph; pairwise claim ranking is a different task.",
            "Use the official CoDEx evaluation protocol and relation-aware baselines for scientific claims.",
            "This result tests known-edge completion, not novel scientific discovery."
        ]
    }

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--train", type=Path, required=True, help="CoDEx-S train.txt")
    p.add_argument("--test", type=Path, required=True, help="CoDEx-S test.txt")
    p.add_argument("--limit", type=int, default=500)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--output", type=Path)
    a = p.parse_args()
    if a.limit < 1:
        p.error("--limit must be >= 1")
    result = evaluate(read_triples(a.train), read_triples(a.test), a.limit, a.seed)
    rendered = json.dumps(result, indent=2)
    if a.output:
        a.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)

if __name__ == "__main__":
    main()
