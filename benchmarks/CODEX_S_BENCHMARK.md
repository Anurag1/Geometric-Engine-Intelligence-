# CoDEx-S benchmark adapter

This adapter starts a real-data benchmark path using CoDEx-S, a public knowledge-graph completion dataset derived from Wikidata/Wikipedia. The dataset provides typed triples (head, relation, tail), so it is **not directly interchangeable** with GEI's current untyped claim-pair candidate task. See the dataset's official documentation and cite its authors when reporting results:

- Dataset and format: https://github.com/tsafavi/codex
- Benchmark paper: https://aclanthology.org/2020.emnlp-main.669/

## Run the lightweight diagnostic

After obtaining the official CoDEx-S files, run:

```bash
python benchmarks/run_codex_s_frequency_baseline.py \
  --train /path/to/codex-s/train.txt \
  --test /path/to/codex-s/test.txt \
  --limit 500 \
  --seed 42 \
  --output results/codex_s_frequency_baseline.json
```

Each input line must be a tab-separated `head<TAB>relation<TAB>tail` triple. The runner reports a simple relation-tail-frequency diagnostic using MRR, Hits@1, and Hits@10 over a deterministic test sample.

## Important limitations

- This is **not** the official CoDEx leaderboard protocol or a filtered all-entity evaluation.
- The runner is a simple baseline diagnostic, not a GEI-vs-state-of-the-art comparison.
- It ranks observed tails for each relation; unseen relations in training are skipped and reported.
- The current GEI heuristic scores untyped claim pairs. A fair comparison requires a task-aligned, relation-aware GEI variant and suitable graph baselines.
- Do not claim scientific superiority from this diagnostic. Treat it as an integration milestone only until it has been executed, audited, and compared under the official evaluation protocol.

## Research next steps

1. Run this script locally or in CI against the official CoDEx-S files.
2. Add graph baselines such as common neighbors / Adamic–Adar only where their task assumptions are valid.
3. Implement a relation-aware model for the same typed triple-completion task.
4. Use filtered ranking metrics and the official split semantics for the principal comparison.
5. Report reproducible configuration, dataset version, exact sample size, seed, and limitations.
