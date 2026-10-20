# GEI Discovery Lab — Workflow Diagram

> **Status:** conceptual workflow for the research prototype. Candidate scores and examples are illustrative; discoveries require independent validation.

## End-to-end workflow

```mermaid
flowchart TD
    A["1 · Ask a research question"] --> B["2 · Build a knowledge graph"]
    B --> C["3 · Generate candidate connections"]
    C --> D["4 · Explain and inspect each candidate"]
    D --> E["5 · Validate with evidence and tests"]
    E --> F{"Evidence supports the hypothesis?"}
    F -- "No / uncertain" --> G["Record uncertainty; revise hypothesis"]
    G --> C
    F -- "Yes" --> H["6 · Benchmark against baselines"]
    H --> I["7 · Explore and refine results"]
    I --> J["8 · Export, document, and publish"]
    J --> K["9 · Apply validated findings to real problems"]
    K -. "New observations and questions" .-> A
    classDef input fill:#10264a,stroke:#38bdf8,color:#fff
    classDef discovery fill:#152a35,stroke:#34d399,color:#fff
    classDef validation fill:#2a1e40,stroke:#c084fc,color:#fff
    classDef output fill:#17352c,stroke:#34d399,color:#fff
    class A,B input
    class C,D discovery
    class E,F,G,H validation
    class I,J,K output
```

## What each stage does

| Stage | Purpose | Output |
|---|---|---|
| Ask | Define a concrete question | Research question |
| Build | Organize claims and known relationships | Knowledge graph |
| Discover | Rank unconnected candidate pairs | Candidate list with explanations |
| Validate | Check evidence, contradictions, and testability | Testable hypotheses and uncertainty notes |
| Benchmark | Compare with appropriate baselines | Reproducible evaluation report |
| Explore | Inspect and refine candidates | Reviewed findings |
| Publish | Export results and methods | Shareable artifacts |
| Apply | Investigate potential practical use | Follow-up experiments |

## Research integrity

- A high score is a **candidate signal**, not proof of a true relationship.
- Use held-out examples and prevent evaluation leakage.
- Report the dataset, scoring method, baseline, sample size, and limitations.
- Do not present synthetic examples as real-world validation.
- Treat real-world impact as a hypothesis until measured.

## Live prototype

[Open GEI Discovery Lab](https://blind-multicolored-cubase--anuragdongare1.replit.app)

## Source repository

[Geometric-Engine-Intelligence](https://github.com/Anurag1/Geometric-Engine-Intelligence-)
