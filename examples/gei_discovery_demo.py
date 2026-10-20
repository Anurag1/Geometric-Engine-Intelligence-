#!/usr/bin/env python3
"""Small, deterministic GEI discovery-loop demo (stdlib only).

This ranks candidate connections in a user-supplied claim graph. It does not
establish that a connection is true or scientifically novel.
"""
from __future__ import annotations

import argparse
import itertools
import json
import re
from pathlib import Path
from typing import Any

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "in", "into", "is", "it", "of", "on", "or", "that", "the", "to",
    "with", "can", "may", "this", "when", "which", "using", "via",
}


def tokens(text: str) -> set[str]:
    """Return a simple, transparent token set; intentionally not an embedding."""
    return {
        word for word in re.findall(r"[a-z0-9]+", text.lower())
        if len(word) > 2 and word not in STOPWORDS
    }


def validate_dataset(data: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], set[tuple[str, str]]]:
    claims = data.get("claims")
    edges = data.get("known_edges", [])
    if not isinstance(claims, list) or not claims:
        raise ValueError("'claims' must be a non-empty list")

    by_id: dict[str, dict[str, Any]] = {}
    for claim in claims:
        if not isinstance(claim, dict):
            raise ValueError("Each claim must be an object")
        for field in ("id", "title", "domain"):
            if not isinstance(claim.get(field), str) or not claim[field].strip():
                raise ValueError(f"Each claim needs a non-empty string '{field}'")
        if claim["id"] in by_id:
            raise ValueError(f"Duplicate claim id: {claim['id']}")
        by_id[claim["id"]] = claim

    known: set[tuple[str, str]] = set()
    for edge in edges:
        if not isinstance(edge, list) or len(edge) != 2:
            raise ValueError("Each known edge must be a two-item list")
        left, right = edge
        if left not in by_id or right not in by_id:
            raise ValueError(f"Unknown claim id in edge: {edge}")
        if left == right:
            raise ValueError("Self-edges are not allowed")
        known.add(tuple(sorted((left, right))))
    return by_id, known


def rank_candidates(data: dict[str, Any], top_k: int = 10) -> list[dict[str, Any]]:
    """Rank unconnected pairs with interpretable heuristic features."""
    if top_k < 1:
        raise ValueError("top_k must be at least 1")
    claims, known = validate_dataset(data)
    terms = {
        claim_id: tokens(f"{claim['title']} {claim.get('description', '')}")
        for claim_id, claim in claims.items()
    }
    degree = {claim_id: 0 for claim_id in claims}
    for left, right in known:
        degree[left] += 1
        degree[right] += 1
    max_degree = max(degree.values(), default=0) or 1

    results = []
    for (left_id, left), (right_id, right) in itertools.combinations(sorted(claims.items()), 2):
        pair = tuple(sorted((left_id, right_id)))
        if pair in known:
            continue
        left_terms, right_terms = terms[left_id], terms[right_id]
        union = left_terms | right_terms
        overlap = len(left_terms & right_terms) / len(union) if union else 0.0
        cross_domain = float(left["domain"].strip().casefold() != right["domain"].strip().casefold())
        isolation = 1.0 - ((degree[left_id] + degree[right_id]) / (2 * max_degree))
        score = round(0.50 * overlap + 0.35 * cross_domain + 0.15 * isolation, 4)
        shared = sorted(left_terms & right_terms)
        reasons = []
        if cross_domain:
            reasons.append("cross-domain connection")
        if shared:
            reasons.append("shared terms: " + ", ".join(shared))
        if isolation > 0:
            reasons.append("at least one endpoint has room for more graph connections")
        if not reasons:
            reasons.append("unexplored pair selected by the transparent baseline")
        results.append({
            "left_id": left_id,
            "left_title": left["title"],
            "right_id": right_id,
            "right_title": right["title"],
            "score": score,
            "features": {
                "lexical_jaccard": round(overlap, 4),
                "cross_domain": bool(cross_domain),
                "isolation": round(isolation, 4),
            },
            "why_ranked": reasons,
            "validation_status": "UNTESTED — candidate connection, not a factual claim",
            "suggested_next_step": (
                "Find independent evidence for a specific causal or mechanistic link; "
                "write a test that could disconfirm it."
            ),
        })
    results.sort(key=lambda item: (-item["score"], item["left_id"], item["right_id"]))
    return results[:top_k]


def load_data(path: str | None) -> dict[str, Any]:
    if path is None:
        return {
            "claims": [
                {"id": "c1", "title": "Caffeine can delay sleep onset", "domain": "sleep",
                 "description": "Caffeine timing is associated with sleep latency."},
                {"id": "c2", "title": "Light exposure influences circadian timing", "domain": "chronobiology",
                 "description": "Evening light can shift the circadian rhythm."},
                {"id": "c3", "title": "Shift work changes meal timing", "domain": "nutrition",
                 "description": "Work schedules affect when people eat."},
                {"id": "c4", "title": "Sleep restriction affects attention", "domain": "cognition",
                 "description": "Reduced sleep can impair sustained attention."},
                {"id": "c5", "title": "Exercise timing relates to sleep quality", "domain": "exercise",
                 "description": "Physical activity timing may correlate with sleep measures."}
            ],
            "known_edges": [["c1", "c4"], ["c2", "c1"]]
        }
    with Path(path).open("r", encoding="utf-8") as handle:
        loaded = json.load(handle)
    if not isinstance(loaded, dict):
        raise ValueError("Input JSON must be an object with 'claims' and optional 'known_edges'")
    return loaded


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", help="JSON file containing claims and known_edges")
    parser.add_argument("--top-k", type=int, default=5, help="Number of candidates to print (default: 5)")
    parser.add_argument("--output", help="Optional path to write the JSON result")
    args = parser.parse_args()
    try:
        result = {
            "method": "GEI transparent lexical/domain heuristic v0",
            "limitations": [
                "This baseline does not understand meaning or verify evidence.",
                "A high score is not proof of novelty, causality, or scientific discovery.",
                "Use source review and a disconfirming test before accepting a hypothesis."
            ],
            "candidates": rank_candidates(load_data(args.input), args.top_k),
        }
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
