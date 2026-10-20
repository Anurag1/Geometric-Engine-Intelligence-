# CoDEx-S adapter test report

**Status:** Unit-test checks passed on a small synthetic fixture; the real CoDEx-S dataset evaluation has not yet been run.

## Checks performed

Six unit tests were executed for the frequency-baseline adapter's core behavior:

- expected MRR, Hits@1, and Hits@10 on a hand-calculated fixture;
- reporting a test triple whose relation has no training examples;
- deterministic sampling for a fixed seed;
- enforcing the requested sample limit;
- parsing a valid tab-separated triple;
- rejecting malformed and empty input files.

Observed result: **6 tests passed**.

These checks validate input handling and basic metric calculations only. They do **not** constitute a CoDEx-S benchmark result, do not reproduce the official CoDEx evaluation protocol, and do not show GEI outperforming any baseline. No real-data performance numbers are reported here.

## Next required scientific step

Run the adapter on the official CoDEx-S train/test files, then implement or use an evaluation aligned with the official filtered all-entity protocol before making comparisons with published models. CoDEx's published benchmark reports MRR and Hits@10 for several knowledge-graph embedding models; those results must not be compared directly with this adapter's current sampled-candidate diagnostic.

Dataset source: https://github.com/tsafavi/codex  
Benchmark paper: https://aclanthology.org/2020.emnlp-main.669/
