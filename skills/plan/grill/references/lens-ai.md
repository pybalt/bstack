# Domain Lens: AI, LLMs & Agents

Load this lens when grilling LLM features, RAG pipelines, agent workflows, prompt systems, classifiers, or AI-assisted automation.

## 1. Gate #0 (Mandatory): Does This Actually Need AI?

Before choosing a model, framework, or agent loop, challenge AI overkill:
```text
IF rules, regex, SQL, deterministic parsing, or a classical model solves >= 95% of cases cleanly:
   -> Baseline Simple = Deterministic code (or deterministic core + narrow LLM fallback).
   -> Only introduce an LLM where unstructured ambiguity genuinely requires semantic judgment.
```
Also challenge **multi-agent orchestration**: start with a single well-prompted call → structured workflow → agent loop only when dynamic branching is proven necessary.

## 2. High-Leverage Decision Branches

1. **Quality & Evals (Measurable, Never "Vibes"):**
   - Define the **golden dataset / eval suite** and target metric (precision, recall, schema validity, rubric score) *before* tuning prompts.
   - Identify failure tolerance: what happens when the model hallucinates or returns invalid output?
2. **Cost, Latency & Model Tiering:**
   - Estimate tokens/call × expected volume = monthly cost and p95 latency.
   - Route simple/high-volume tasks to fast/cheap models and reserve frontier models for hard reasoning; check caching/batching.
3. **Privacy & Data Classification (`environment` Privacy Gate):**
   - Classify inputs (public / internal / PII / regulated). Verify ZDR / VPC / no-training guarantees before sending real data; enforce redaction at the proxy boundary.
4. **Containment, Determinism & Fallbacks:**
   - Structured output validation (strict schemas), bounded retries, tool allowlists (read-only by default), human approval gates for irreversible actions, and deterministic fallback behavior on model failure or timeout.

## 3. AI Observability & Security Baseline

- **Logs & Traces:** Log every run with `trace_id`, model/version, prompt/template version, latency, input/output token counts, estimated cost, tool calls, and validation pass/fail (redact PII/secrets before storing).
- **Metrics:** Eval pass rate, schema/parse failure rate, fallback rate, p95 latency, cost per successful task, and user acceptance/override rate.
- **Security:** Treat all retrieved docs, tickets, web pages, and user inputs as **untrusted** (prompt-injection defense); enforce permissions in code/proxies outside the LLM; cap max steps, tokens, and spend per run.

## 4. Recommended Frameworks
`4 Value Levers` · `Pugh Matrix` · `Pre-Mortem` · `Lightweight STRIDE` · `evolve` (for empirical prompt/eval optimization).
