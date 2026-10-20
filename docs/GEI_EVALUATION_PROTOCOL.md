# GEI Evaluation Protocol — Research-Grade Validation Plan

**Status:** protocol proposal; not yet an executed real-world benchmark.

## Objective

Test whether GEI's candidate ranking helps identify held-out, documented relationships more effectively than simple baselines. This evaluation does not test whether GEI discovers novel scientific facts unless the dataset and review process explicitly support that claim.

## Current evidence boundary

The bundled benchmark is synthetic and useful for exercising code paths and metrics only. It cannot establish generalization, practical usefulness, or superiority to conventional research workflows. Do not use its scores as real-world performance claims.

## Dataset requirements

For the first real benchmark, select one narrow domain and a public dataset with documented provenance and a clear definition of a positive relationship.

Record:
- dataset name, version, license, source URL, retrieval date, and checksum;
- entity/claim schema and relationship semantics;
- how positive and negative examples were established;
- known missingness and sampling biases;
- permitted use and any privacy constraints.

Do not combine incompatible edge types into one positive label. Where labels are uncertain, preserve an explicit unknown category instead of silently treating unknown pairs as negatives.

## Leakage-safe split

1. Define the task and candidate universe before tuning scores.
2. Split positive edges into train, validation, and test sets with a fixed, documented seed.
3. Remove validation/test positives from the graph used for ranking.
4. Check reverse edges, duplicates, aliases, and derived features for leakage.
5. If entities or time can leak information, add entity-disjoint or temporal evaluation as appropriate.
6. Freeze the test set until the method and hyperparameters are finalized.
7. Keep a manifest of IDs per split and a script that verifies disjointness.

A random edge split alone may be insufficient when near-duplicate entities, repeated sources, or temporal dependencies exist.

## Required baselines

Compare on the **same candidate set and split**:
1. Seeded random ranking (sanity baseline).
2. Lexical Jaccard similarity.
3. Graph common-neighbors score.
4. Adamic–Adar or resource-allocation score when graph structure supports it.
5. Preferential-attachment score.
6. GEI's combined heuristic.
7. A credible domain-specific baseline, selected with input from a domain expert.

Avoid presenting a baseline as applicable when the dataset lacks the information it requires. State each method's inputs and parameter settings.

## Metrics and reporting

Report at minimum:
- Precision@k at predeclared k values;
- Recall@k where the positive-label universe makes it meaningful;
- average precision or mean reciprocal rank when appropriate;
- candidate coverage and the number of positives in the eligible candidate set;
- bootstrap confidence intervals or another justified uncertainty estimate;
- runtime and memory use for comparable environments;
- qualitative false-positive and false-negative analysis.

Report raw counts alongside rates. A high Precision@k on a tiny test set can be unstable; include the denominator and uncertainty.

## Human review

For a small blinded sample, ask independent domain reviewers to assess relevance and evidence quality without seeing which method proposed each candidate. Record inter-rater agreement and disagreements. Ranking a known relationship is not the same as discovering a novel one.

## Ablations

Evaluate the GEI score with each component removed in turn:
- lexical overlap;
- cross-domain indicator;
- endpoint isolation.

This tests whether each component contributes beyond the others. Tune weights only on training/validation data, never on the frozen test set.

## Release checklist

- [ ] Dataset provenance and license documented
- [ ] Split manifest generated and disjointness checked
- [ ] Leakage audit documented
- [ ] Baselines evaluated on identical candidates
- [ ] Metrics and uncertainty reported
- [ ] Ablations run
- [ ] Errors and limitations analyzed
- [ ] Exact commands, environment, and seeds recorded
- [ ] Claims in README and social posts match evidence

## Decision rule

Only claim an improvement if the held-out results support it, uncertainty is reported, and the comparison is methodologically fair. If results are mixed or inconclusive, publish that outcome. A failed or neutral result is useful evidence.

## Project links

- [GEI repository](https://github.com/Anurag1/Geometric-Engine-Intelligence-)
- [Workflow diagram](./GEI_WORKFLOW_DIAGRAM.md)
- [Conventional workflow vs. GEI](./TRADITIONAL_VS_GEI_WORKFLOW.md)
- [Live prototype](https://blind-multicolored-cubase--anuragdongare1.replit.app)
