# CoDEx-S filtered frequency evaluation

This script adds a stronger, transparent baseline than the earlier sampled-candidate diagnostic.

## Run

Download and extract the official CoDEx-S archive from the [Zenodo dataset record](https://zenodo.org/records/4281094) or the [official CoDEx repository](https://github.com/tsafavi/codex). Then run:

```bash
python benchmarks/run_codex_s_filtered_frequency.py \
  --train /path/to/codex-s/train.txt \
  --valid /path/to/codex-s/valid.txt \
  --test /path/to/codex-s/test.txt \
  --output results/codex_s_filtered_frequency.json
```

The expected format is one `head<TAB>relation<TAB>tail` triple per line.

## Protocol

- Tail prediction: rank the gold tail against all entities observed in the provided splits.
- Baseline score: count of each candidate tail in the training set for the query relation.
- Filtering: remove other known true tails for the same (head, relation) query, retaining the gold answer.
- Ties: use average rank for equal scores.
- Metrics: MRR, Hits@1, Hits@3, Hits@10.
- Data splits: training frequencies are computed from train only; validation and test triples are used only to construct the entity universe and filter known answers.

## Interpretation limits

This is a reproducible, interpretable frequency baseline, not a trained embedding model. It evaluates tail prediction only. It is **not** a direct reproduction of the official CoDEx leaderboard protocol, and results must not be compared as if identical to published results unless evaluation details are aligned. It does not test GEI's current untyped claim-pair heuristic and does not establish scientific discovery or GEI superiority.

## Current execution status

The implementation and hand-constructed fixture logic have been checked for filtering, tie handling, and metric arithmetic. The official CoDEx-S archive was not available in the execution environment during this run, so **no real-data scores are reported**. Do not populate a results table with invented or estimated values. The next gate is to run this command on the official files and review the output before making claims.
