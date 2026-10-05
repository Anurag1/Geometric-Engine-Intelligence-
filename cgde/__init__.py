"""
Contradiction-Driven Geometric Discovery Engine (CGDE)
Geometric Engine Intelligence core package.
"""

from .models import (
    ClaimType,
    RelationType,
    Provenance,
    Claim,
    Edge,
    Hypothesis,
    KnowledgeGraph,
)

__version__ = "0.1.0-phase0"
__all__ = [
    "ClaimType",
    "RelationType",
    "Provenance",
    "Claim",
    "Edge",
    "Hypothesis",
    "KnowledgeGraph",
]
