# Geometric Engine Intelligence (GEI)

**Contradiction-Driven Geometric Discovery Engine (CGDE)**

> Can AI move from generating plausible answers toward discovering missing relationships, producing falsifiable hypotheses, and learning from verification?

This repository implements a research system that treats **unexplored edges** and **contradictions** as first-class objects of discovery.

---

## Status: Phase 0 Foundation Complete (Breakthrough Path Active)

**Phase 0 Deliverables (Completed)**
- Canonical data model for claims, assumptions, evidence, provenance, edges, and hypotheses
- Explicit separation of known edges vs unexplored edges (`E*`)
- Research claim ladder (Level 1 → Level 2 → Level 3)
- Core mathematical framing and discovery loop formalized
- Package skeleton and evaluation harness foundation

**Current Research Claim Level**: Level 1 (algorithmic novelty) ready for rigorous testing. Level 2 and Level 3 remain the target.

---

## Core Idea

Most AI systems generate answers.  
GEI/CGDE is designed to generate **missing questions and testable hypotheses**.

### Mathematical Object

\[
G = (V, E, X)
\]

- `V`: entities / claims
- `E`: known relationships
- `X`: evidence, attributes, uncertainty, time, assumptions

The primary search space is the complement of the known edge set:

\[
E^* = \{(u,v) : u,v \in V,\ u \neq v,\ (u,v) \notin E\}
\]

Candidates in `E*` are ranked by measurable properties:
- Novelty
- Cross-domain connectivity
- Falsifiability / testability
- Contradiction potential
- Redundancy penalty

---

## Research Claim Ladder (Non-Negotiable)

| Level | Claim | Requirement |
|-------|-------|-------------|
| **1** | Algorithmic novelty | System produces different / higher-quality candidate edges than baselines |
| **2** | Knowledge novelty | Candidates survive deduplication + provenance checks against a reference corpus |
| **3** | Scientific discovery | Candidates produce previously unknown, reproducible empirical results |

Level 1 is **not** treated as proof of Level 3.

---

## Discovery Loop

```
Reality / Existing Knowledge
        ↓
Knowledge Graph (Claims + Evidence + Assumptions)
        ↓
Known Edges  ↔  Unexplored Edges (E*)
        ↓
Candidate Ranking (novelty × falsifiability × cross-domain)
        ↓
Contradiction Test + Novelty Test
        ↓
Falsifiable Hypothesis + Discriminating Test
        ↓
Experiment / Simulation / Independent Evaluation
        ↓
Validation or Refutation → Graph Update
```

---

## Package Structure

```
cgde/
├── models.py          # Canonical data model (Claim, Edge, Hypothesis, Provenance, KnowledgeGraph)
├── scoring.py         # Novelty, falsifiability, cross-domain, contradiction scoring
├── extractors/        # Claim + assumption extraction interfaces
├── graph/             # Graph construction and operations
├── evaluation/        # Benchmark harness and claim-level metrics
├── demos/             # Interactive and historical demos
benchmarks/
├── discovery_cases.json
├── benchmark.py
docs/
├── research-map.md
├── VISUAL_RESEARCH_MAP.md
```

---

## Quick Start (Phase 0)

```bash
# Clone
git clone https://github.com/Anurag1/Geometric-Engine-Intelligence-.git
cd Geometric-Engine-Intelligence-

# Interactive historical demo (original prototype)
open index.html

# Core data model and scoring (Python)
python -c "from cgde.models import KnowledgeGraph, Claim, Edge; print('CGDE models loaded')"
```

---

## How to Contribute (High-Value Work Only)

Contributions are most valuable when they **test** an idea rather than merely endorse it.

Preferred contributions:
- Independent replications
- Stronger baselines
- Ablation studies
- Mathematical formalization
- Counterexamples and falsification tests
- Benchmark datasets with ground-truth novelty labels
- Provenance and evidence improvements
- Reproducibility fixes

A negative result is valuable when it is reproducible.

---

## Scientific Standard

Claims must be separated into:
1. Algorithmic novelty
2. Knowledge novelty
3. Scientific discovery

The goal is to make the third claim difficult to earn — and therefore meaningful when achieved.

---

## Roadmap Status

| Phase | Goal | Status |
|-------|------|--------|
| **0** | Canonical data model + foundation | **Complete** |
| **1** | Working discovery loop + scoring | In progress |
| **2** | Scientific validation on real corpora | Planned |
| **3** | Productization + self-improvement loops | Planned |

---

## License

Apache-2.0 (see LICENSE)

---

**Maintainer**: Anurag Bimbisar Dongare ([@Anurag1](https://github.com/Anurag1))

This project exists to make discovery-oriented AI measurable, falsifiable, and reproducible.
