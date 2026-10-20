#!/usr/bin/env python3
"""Filtered all-entity tail prediction for CoDEx-style TSV triples.

This is a transparent frequency baseline, not a trained embedding model.
For each test (head, relation, tail), rank all entities by relation-tail
frequency, filter other known true tails for the same (head, relation), and
use average ranks for ties. Metrics are MRR and Hits@1/3/10.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


Triple = tuple[str, str, str]


def read_triples(path: Path) -> list[Triple]:
    triples: list[Triple] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        fields = line.split("\t")
        if len(fields) != 3 or not all(fields):
            raise ValueError(f"{path}:{line_no}: expected head<TAB>relation<TAB>tail")
        triples.append((fields[0], fields[1], fields[2]))
    if not triples:
        raise ValueError(f"No triples found in {path}")
    return triples


def evaluate(train: list[Triple], valid: list[Triple], test: list[Triple]) -> dict:
    if not train or not test:
        raise ValueError("train and test must both contain at least one triple")
    all_triples = train + valid + test
    entities = sorted({entity for h, _, t in all_triples for entity in (h, t)})
    tails_by_relation: dict[str, Counter[str]] = defaultdict(Counter)
    known_tails: dict[tuple[str, str], set[str]] = defaultdict(set)

    for h, r, t in train:
        tails_by_relation[r][t] += 1
    for h, r, t in all_triples:
        known_tails[(h, r)].add(t)

    reciprocal_ranks: list[float] = []
    hits = {1: 0, 3: 0, 10: 0}
    for h, r, gold in test:
        counts = tails_by_relation.get(r, Counter())
        gold_score = counts[gold]
        # Filter other known answers for this query, but always retain the gold.
        filtered = known_tails[(h, r)] - {gold}
        remaining = [e for e in entities if e not in filtered and e != gold]
        greater = sum(counts[e] > gold_score for e in remaining)
        tied = sum(counts[e] == gold_score for e in remaining)
        rank = 1.0 + greater + tied / 2.0
        reciprocal_ranks.append(1.0 / rank)
        for k in hits:
            hits[k] += rank <= k

    n = len(reciprocal_ranks)
    return {
        "benchmark": "CoDEx-S",
        "task": "tail prediction",
        "method": "relation-tail-frequency baseline",
        "ranking": "all entities observed across train/valid/test; filtered known answers; average tie rank",
        "entities": len(entities),
        "train_triples": len(train),
        "valid_triples": len(valid),
        "test_triples": len(test),
        "evaluated_queries": n,
        "MRR": round(sum(reciprocal_ranks) / n, 6),
        "Hits@1": round(hits[1] / n, 6),
        "Hits@3": round(hits[3] / n, 6),
        "Hits@10": round(hits[10] / n, 6),
        "limitations": [
            "Tail prediction only; does not evaluate head prediction.",
            "Frequency baseline, not a trained knowledge-graph embedding model.",
            "Use the dataset's official entity universe and evaluation implementation for direct leaderboard comparisons.",
            "This measures link prediction, not novel scientific discovery or the current untyped GEI heuristic."
        ]
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train", type=Path, required=True)
    parser.add_argument("--valid", type=Path, required=True)
    parser.add_argument("--test", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = evaluate(read_triples(args.train), read_triples(args.valid), read_triples(args.test))
    rendered = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
