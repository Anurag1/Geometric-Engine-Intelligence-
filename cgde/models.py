"""
Canonical data model for the Contradiction-Driven Geometric Discovery Engine (CGDE).

Phase 0 Foundation — completed.
This model enforces explicit assumptions, provenance, unexplored edges,
falsifiability scores, and clear separation between candidate and validated knowledge.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class ClaimType(Enum):
    FACTUAL = "factual"
    THEORETICAL = "theoretical"
    METHODOLOGICAL = "methodological"
    EMPIRICAL = "empirical"
    ASSUMPTION = "assumption"


class RelationType(Enum):
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    DEPENDS_ON = "depends_on"
    GENERALIZES = "generalizes"
    SPECIALIZES = "specializes"
    ANALOGOUS_TO = "analogous_to"
    UNEXPLORED = "unexplored"          # candidate edge in E*
    CAUSAL = "causal"
    CORRELATIONAL = "correlational"


@dataclass
class Provenance:
    source_id: str
    source_type: str                    # paper, book, experiment, model output, human
    location: Optional[str] = None      # page, section, DOI, arXiv id
    extracted_by: str = "human"         # or model version identifier
    confidence: float = 1.0
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Claim:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    text: str = ""
    claim_type: ClaimType = ClaimType.FACTUAL
    entities: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)   # explicit list of assumptions
    evidence: List[Provenance] = field(default_factory=list)
    confidence: float = 0.5
    domain: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Edge:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source_claim_id: str = ""
    target_claim_id: str = ""
    relation: RelationType = RelationType.UNEXPLORED
    strength: float = 0.0               # for known edges
    novelty_score: float = 0.0          # for unexplored candidates
    falsifiability_score: float = 0.0
    cross_domain_score: float = 0.0
    contradiction_score: float = 0.0
    supporting_evidence: List[Provenance] = field(default_factory=list)
    proposed_test: Optional[str] = None
    status: str = "candidate"           # candidate | validated | refuted | known


@dataclass
class Hypothesis:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    text: str = ""
    source_edge_id: str = ""
    assumptions: List[str] = field(default_factory=list)
    predicted_observation: str = ""
    discriminating_test: str = ""
    expected_outcome_if_true: str = ""
    expected_outcome_if_false: str = ""
    novelty_score: float = 0.0
    testability_score: float = 0.0
    risk_of_triviality: float = 0.0
    status: str = "proposed"            # proposed | under_test | supported | refuted


@dataclass
class KnowledgeGraph:
    claims: Dict[str, Claim] = field(default_factory=dict)
    edges: Dict[str, Edge] = field(default_factory=dict)
    hypotheses: Dict[str, Hypothesis] = field(default_factory=dict)

    def add_claim(self, claim: Claim) -> None:
        self.claims[claim.id] = claim

    def add_edge(self, edge: Edge) -> None:
        self.edges[edge.id] = edge

    def add_hypothesis(self, hypothesis: Hypothesis) -> None:
        self.hypotheses[hypothesis.id] = hypothesis

    def unexplored_edges(self) -> List[Edge]:
        return [e for e in self.edges.values() if e.relation == RelationType.UNEXPLORED]

    def contradictions(self) -> List[Edge]:
        return [e for e in self.edges.values() if e.relation == RelationType.CONTRADICTS]

    def known_edges(self) -> List[Edge]:
        return [e for e in self.edges.values() if e.relation != RelationType.UNEXPLORED and e.status == "known"]

    def candidate_hypotheses(self) -> List[Hypothesis]:
        return [h for h in self.hypotheses.values() if h.status == "proposed"]

    def summary(self) -> Dict[str, int]:
        return {
            "claims": len(self.claims),
            "total_edges": len(self.edges),
            "known_edges": len(self.known_edges()),
            "unexplored_edges": len(self.unexplored_edges()),
            "contradictions": len(self.contradictions()),
            "hypotheses": len(self.hypotheses),
            "candidate_hypotheses": len(self.candidate_hypotheses()),
        }
