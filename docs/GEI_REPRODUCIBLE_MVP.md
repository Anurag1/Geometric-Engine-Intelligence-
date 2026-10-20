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
python -m unittest discover -s tests -p 'test_gei_discovery_demo.py' -v
```

## Input format

A JSON object with a non-empty `claims` array. Each claim needs a unique `id`, `title`, and `domain`; `description` is optional. `known_edges` is an optional array of two-ID arrays.

## What it does

1. Validates claim and edge IDs.
2. Enumerates pairs that are not already connected.
3. Computes an interpretable score from lexical Jaccard overlap, cross-domain status, and graph isolation.
4. Returns reasons, feature values, and a suggested falsification step.

## Important limitations

This is a transparent heuristic baseline—not an embedding model, evidence retriever, scientific validator, or proof of novelty. Its score means only “prioritize for review.” The demo does not access the internet or verify sources. Do not present a generated pair as a discovery until evidence review and an independent, disconfirming test have been completed.

## Next validation milestone

Evaluate on a curated dataset with held-out known relationships and expert-judged candidate quality. Compare against random ranking and simple graph heuristics; report precision@k, redundancy, and evidence coverage. Keep benchmark data and splits versioned to prevent leakage.
