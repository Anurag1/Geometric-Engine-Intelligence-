# CoDEx-S benchmark execution status

**Status: blocked before benchmark execution; no GEI experimental result is claimed.**

## What was attempted

A GitHub Actions workflow was added to:
1. run the repository's Python unit tests;
2. download the official CoDEx-S train/validation/test triples;
3. execute the filtered all-entity relation-tail-frequency baseline;
4. validate metric ranges and upload the JSON result as an artifact.

The workflow run associated with the current pull-request head completed with failure. GitHub's run metadata returned a completed failed job but no step list, and fetching its job log returned a 404 because no log artifact was available. Two subsequent failed-job retries (CoDEx-S run 39380845367 and GEI MVP run 39380845378) also completed with `steps: null` and no job log URL. Therefore, the available evidence does not establish whether the failure is runner provisioning, repository Actions configuration, or another pre-step service failure. Crucially, there is no evidence that the dataset download or benchmark code executed. An administrator should inspect the repository's Actions settings and GitHub Actions service/runner availability before another benchmark attempt.

## Published literature reference (not our run)

The original CoDEx repository reports these CoDEx-S link-prediction metrics for its trained models:

| Model | MRR | Hits@1 | Hits@3 | Hits@10 |
|---|---:|---:|---:|---:|
| RESCAL | 0.404 | 0.293 | 0.4494 | 0.623 |
| TransE | 0.354 | 0.219 | 0.4218 | 0.634 |
| ComplEx | 0.465 | 0.372 | 0.5038 | 0.646 |
| ConvE | 0.444 | 0.343 | 0.4926 | 0.635 |
| TuckER | 0.444 | 0.339 | 0.4975 | 0.638 |

Source: https://github.com/tsafavi/codex (CoDEx authors' published repository). These are reported literature results, **not** measurements produced by GEI, and they must not be treated as a direct comparison with the current frequency baseline because the exact evaluation protocol and candidate ranking may differ.

## Latest local validation (2026-10-20)

The four focused fixture tests for the filtered frequency evaluator were executed in an isolated local Python test workspace after correcting the fixture's expected average tie rank. Result: **4 tests passed**. The fixture verifies filtered known answers, average-rank tie handling, input validation, and deterministic output. This is a local unit-test result for the evaluator logic; it is not a run on the official CoDEx-S dataset and does not validate dataset download, full-repository test suite, or GitHub Actions.

## Current conclusion

- The filtered frequency baseline implementation, fixture tests, and CI workflow are committed.
- The official-dataset evaluation remains unexecuted in this run.
- No claim that GEI beats these baselines is supported.
- Do not merge this pull request until required checks can run and pass. Do not bypass repository protections.
