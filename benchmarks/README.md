# Live Modern-AI Benchmark

This benchmark tests the core claim from the GEI discussions:

> Does explicitly representing assumptions, contradictions, missing edges and falsifiable tests improve research-discovery behavior compared with a normal general-purpose prompt?

## Experimental design

The same API model receives the same six research tasks under two conditions:

1. **Baseline** — normal research-assistant instruction.
2. **GEI** — explicit knowledge-graph + unexplored-edge + contradiction + falsification protocol.

The benchmark records output, latency and a transparent structural score. The score is **not a scientific novelty score**; human review is still required to determine whether a proposed connection is genuinely new, useful and correct.

OpenAI's current API quickstart documents the Responses API and `gpt-5.6`; the runner therefore defaults to `OPENAI_MODEL=gpt-5.6` but allows another available model to be selected through the environment. citehttps://platform.openai.com/overview

## Run

```bash
pip install -r benchmarks/requirements.txt
python benchmarks/benchmark.py
```

Optional:

```bash
OPENAI_MODEL=gpt-5.6 BENCHMARK_RUNS=3 python benchmarks/benchmark.py
```

The runner requires an existing `OPENAI_API_KEY` in the execution environment and never prints it. Results are written to `benchmarks/results.json`.

## Interpretation

A useful result is **not** simply "GEI scored higher." A convincing result should show:

- higher-quality candidate edges;
- fewer unsupported historical claims;
- more explicit contradictions;
- more genuinely falsifiable tests;
- comparable or acceptable latency/cost;
- and, most importantly, independent human evaluation of the resulting hypotheses.

The strongest future version should add blinded human ratings, a held-out corpus, provenance checks, semantic-duplicate detection, and execution/simulation of proposed tests.
