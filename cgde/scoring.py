"""
Scoring functions for unexplored edges (E*) and hypotheses.

Phase 0 foundation. These scores are designed to be measurable and ablatable.
"""

from __future__ import annotations

from typing import Dict, Optional
from .models import Edge, Hypothesis, KnowledgeGraph, RelationType


def novelty_score(edge: Edge, graph: KnowledgeGraph, reference_corpus_size: int = 1000) -> float:
    """
    Higher when the edge is rare relative to known structure.
    Placeholder heuristic for Phase 0; replace with embedding / graph distance metrics.
    """
    if edge.relation != RelationType.UNEXPLORED:
        return 0.0
    # Simple inverse frequency style placeholder
    return min(1.0, 1.0 / (1.0 + edge.strength))


def falsifiability_score(edge: Edge, hypothesis: Optional[Hypothesis] = None) -> float:
    """
    Higher when a clear discriminating test exists.
    """
    if hypothesis and hypothesis.discriminating_test:
        base = 0.7
        if hypothesis.expected_outcome_if_true and hypothesis.expected_outcome_if_false:
            base += 0.3
        return min(1.0, base)
    if edge.proposed_test:
        return 0.5
    return 0.1


def cross_domain_score(edge: Edge, graph: KnowledgeGraph) -> float:
    """
    Higher when source and target claims belong to different domains.
    """
    src = graph.claims.get(edge.source_claim_id)
    tgt = graph.claims.get(edge.target_claim_id)
    if not src or not tgt:
        return 0.0
    if src.domain and tgt.domain and src.domain != tgt.domain:
        return 0.9
    return 0.2


def contradiction_score(edge: Edge) -> float:
    """
    Higher when the relation is explicitly contradictory or assumptions conflict.
    """
    if edge.relation == RelationType.CONTRADICTS:
        return 1.0
    return edge.contradiction_score


def composite_edge_score(
    edge: Edge,
    graph: KnowledgeGraph,
    weights: Optional[Dict[str, float]] = None,
) -> float:
    """
    Weighted combination used for ranking E*.
    Default weights emphasize novelty and falsifiability.
    """
    if weights is None:
        weights = {
            "novelty": 0.35,
            "falsifiability": 0.30,
            "cross_domain": 0.20,
            "contradiction": 0.15,
        }

    n = novelty_score(edge, graph)
    f = falsifiability_score(edge)
    c = cross_domain_score(edge, graph)
    k = contradiction_score(edge)

    score = (
        weights["novelty"] * n
        + weights["falsifiability"] * f
        + weights["cross_domain"] * c
        + weights["contradiction"] * k
    )
    return round(score, 4)


def rank_unexplored_edges(graph: KnowledgeGraph, top_k: int = 20) -> list:
    """Return top-k unexplored edges sorted by composite score."""
    candidates = graph.unexplored_edges()
    scored = [(composite_edge_score(e, graph), e) for e in candidates]
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]
