"""Live A/B benchmark: plain LLM prompting vs GEI-style structured discovery.

Requires OPENAI_API_KEY in the execution environment.
The script never prints the key.
"""
import json, os, re, statistics, time
from pathlib import Path
from openai import OpenAI

ROOT = Path(__file__).resolve().parent
CASES = json.loads((ROOT / "discovery_cases.json").read_text())
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6")
RUNS = int(os.getenv("BENCHMARK_RUNS", "1"))

BASELINE = """You are a strong general-purpose AI assistant. Answer the research question carefully. Do not invent historical facts. Distinguish established knowledge from hypotheses. Give one useful, testable answer."""

GEI = """You are a research discovery engine. Treat the supplied entities as nodes in a knowledge graph.

For every task:
1. Identify the relevant known relationships.
2. Search for an unexplored or weakly explored edge.
3. State the assumptions that make the proposed connection plausible.
4. Look explicitly for contradictions or reasons the connection could fail.
5. Produce a falsifiable hypothesis.
6. Propose a discriminating test that could prove the hypothesis wrong.
7. Never present a generated connection as a historical fact unless supported by the supplied context.

Return JSON with exactly these fields:
{
  "candidate_edge": "A-B",
  "hypothesis": "...",
  "assumptions": ["..."],
  "contradictions": ["..."],
  "test": "...",
  "confidence": 0.0
}
"""

def call(client, system, case):
    prompt = f"QUESTION: {case['question']}\nTASK: {case['task']}\nNODES: {case['nodes']}\nKNOWN EDGES: {case['known_edges']}"
    response = client.responses.create(model=MODEL, input=[{"role":"system","content":system},{"role":"user","content":prompt}])
    return response.output_text

def parse_json(text):
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.S)
        return json.loads(match.group(0)) if match else None

def score(raw, mode):
    data = parse_json(raw) if mode == "gei" else None
    if mode == "gei" and data:
        fields = ["candidate_edge","hypothesis","assumptions","contradictions","test","confidence"]
        completeness = sum(1 for f in fields if f in data and data[f] not in (None, "", [])) / len(fields)
        falsifiability = 1.0 if isinstance(data.get("test"), str) and len(data["test"].split()) >= 8 else 0.0
        contradiction = 1.0 if isinstance(data.get("contradictions"), list) and len(data["contradictions"]) > 0 else 0.0
        edge = 1.0 if isinstance(data.get("candidate_edge"), str) and "-" in data["candidate_edge"] else 0.0
        return round((completeness + falsifiability + contradiction + edge) / 4, 3)
    # Baseline gets a structural score without requiring JSON.
    text = raw.lower()
    signals = ["hypothesis", "assumption", "test", "evidence", "contradiction", "uncertain"]
    return round(sum(s in text for s in signals) / len(signals), 3)

def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is not available in the execution environment.")
    client = OpenAI()
    rows=[]
    for case in CASES:
        for run in range(RUNS):
            for mode, system in (("baseline", BASELINE), ("gei", GEI)):
                start=time.perf_counter()
                raw=call(client, system, case)
                elapsed=round(time.perf_counter()-start, 2)
                rows.append({"case":case["id"],"run":run+1,"mode":mode,"model":MODEL,"score":score(raw,mode),"latency_s":elapsed,"output":raw})
    out=ROOT/"results.json"
    out.write_text(json.dumps(rows, indent=2, ensure_ascii=False))
    for mode in ("baseline","gei"):
        subset=[r for r in rows if r["mode"]==mode]
        print(f"{mode:8} score={statistics.mean(r['score'] for r in subset):.3f} latency={statistics.mean(r['latency_s'] for r in subset):.2f}s")
    print(f"Saved {len(rows)} responses to {out}")

if __name__ == "__main__":
    main()
