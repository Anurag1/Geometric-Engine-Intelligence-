# GEI Reproducible Discovery MVP

This branch adds a small, dependency-free discovery loop to make the GEI concept executable and testable.

## Run the demo

Requires Python 3.10+ and only the standard library.

```bash
python examples/gei_discovery_demo.py
python examples/gei_discovery_demo.py --top-k 3 --output results.json
python examples/gei_discovery_demo.py --input benchmarks/sample_claims.json --top-k 4
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Run the baseline comparison

```bash
python benchmarks/evaluate_synthetic_baseline.py --k 3 --trials 1000
```

The harness compares the heuristic's precision@k against the mean precision@k of seeded random rankings over the same candidate set. It also validates that held-out positive edges are not leaked into the known training edges. The bundled eight-claim holdout is **synthetic and illustrative**. Its results are only a harness smoke test; they are not evidence of generalization, scientific discovery, causality, or performance on real research data.

## Input format

A JSON object with a non-empty `claims` array. Each claim needs a unique `id`, `title`, and `domain`; `description` is optional. `known_edges` is an optional array of two-ID arrays.

## What it does

1. Validates claim and edge IDs.
2. Enumerates pairs that are not already connected.
3. Computes an interpretable score from lexical Jaccard overlap, cross-domain status, and graph isolation.
4. Returns reasons, feature values, and a suggested falsification step.

## Important limitations

This is a transparent heuristic baseline—not an embedding model, evidence retriever, scientific validator, or proof of novelty. Its score means only “prioritize for review.” The demo does not access the internet or verify sources. Do not present a generated pair as a discovery until evidence review and an independent, disconfirming test have been completed.

## Next research-grade validation milestone

Replace or supplement the synthetic holdout with a curated, expert-labelled dataset, freeze the split before tuning, and evaluate across multiple domains. Compare against random ranking and simple graph heuristics; report precision@k, redundancy, uncertainty across seeds, and evidence coverage. Keep benchmark data, split definitions, and scoring changes versioned to prevent leakage.
