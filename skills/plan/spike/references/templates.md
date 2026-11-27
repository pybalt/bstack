# Spike Templates & Frontier Mode

Load this reference when decomposing multiple spikes, documenting verdicts, comparing variants head-to-head, or deciding what to spike next.

## 1. Risk-Ordered Decomposition Table

| # | Spike | Validates (Given / When / Then) | Risk | Timebox |
| :--- | :--- | :--- | :---: | :---: |
| `001` | `ws-streaming` | Given an active WS connection, when tokens stream, then client renders chunks in < 100ms under backpressure | High | 30 min |
| `002a` | `parser-lib-a` | Given a 50-page sample doc, when parsed with Lib A, then tables extract with > 95% accuracy | Medium | 20 min |
| `002b` | `parser-lib-b` | Given the same 50-page doc, when parsed with Lib B, then tables extract with > 95% accuracy | Medium | 20 min |

- **Standard spike (`001`):** one approach answering one question.
- **Comparison spike (`002a` / `002b`):** same question, competing approaches.

## 2. Spike Verdict (`spikes/NNN-slug/README.md`)

```markdown
# NNN: <slug>
- **Question (Given/When/Then):** ...
- **Timebox:** ... | **Approach:** ...

## Verdict: VALIDATED | PARTIAL | INVALIDATED

### Evidence (Commands & Observed Output)
- ...

### What Worked / What Didn't
- Worked: ...
- Didn't (including edge cases tested): ...

### Surprises & Constraints
- ...

### Recommendation for the Real Build
- ... (Keep/drop approach, or promote to `evolve` if hybridizing)
```

## 3. Head-to-Head Comparison Table

```markdown
## Head-to-Head: Option A (002a) vs Option B (002b)

| Dimension | Option A (`002a`) | Option B (`002b`) |
| :--- | :--- | :--- |
| Primary quality / accuracy | ... | ... |
| Edge-case resilience | ... | ... |
| Setup & dependency friction | ... | ... |
| Measured latency / resource cost | ... | ... |

**Winner:** <Option> for the measured problem profile. *Breakpoint:* switch to <Alternative> if <condition>.
```

## 4. Frontier Mode ("What Should We Spike Next?")

When `spikes/` already exists and the user asks what to validate next, scan existing verdicts for:
1. **Integration risks:** two `VALIDATED` spikes touching the same resource/API that were never tested together.
2. **Unproven handoffs:** output format of Spike A assumed compatible with input of Spike B.
3. **Assumed capabilities:** critical parts of the plan still backed only by guesses.
4. **Alternative angles:** new paradigms for `PARTIAL` or `INVALIDATED` spikes.

Propose **2–4 risk-ordered candidates** in Given/When/Then format and let the user choose.
