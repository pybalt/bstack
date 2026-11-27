# Tight Repro Loops, Automated `git bisect` & Anti-Rationalizations

Load this reference when a bug is hard to reproduce, when isolating a regression across commits with `git bisect`, or when resisting shortcuts.

## 1. Automated `git bisect` Protocol (For Regressions)

**Trigger:** *"This worked before (known good commit/tag/date) and is broken now."* Never eyeball 40 commits by hand when binary search finds the exact culprit in ~6 runs.

### Step-by-Step (Non-Interactive & Agent-Safe)
1. **Put the repro script OUTSIDE the tracked repo** (e.g., `/tmp/bisect_check.sh`) so `git checkout` across old commits never deletes or conflicts with it.
2. **Return strict `git bisect` exit codes from the script:**
   - `0` → **good** (bug NOT present)
   - `1–124` or `126–127` → **bad** (bug IS present)
   - **`125` → skip** (critical! return `125` if an intermediate commit fails to build/install for an unrelated reason so bisect does not misclassify it as the bug)
3. **Verify both boundaries BEFORE bisecting:** run the script on `HEAD` (must exit non-zero, not 125) and on `<good-ref>` (must exit `0`).
4. **Execute automated search & always clean up:**
   ```bash
   git bisect start
   git bisect bad HEAD
   git bisect good <known-good-commit-or-tag>
   git bisect run /tmp/bisect_check.sh
   # Inspect the exact offending commit:
   git show --stat <culprit-sha>
   # ALWAYS restore original HEAD when done:
   git bisect reset
   ```

### Template `/tmp/bisect_check.sh`
```bash
#!/usr/bin/env bash
set -u
# Build/setup check — if broken for unrelated reasons, tell git bisect to SKIP (125)
<build_or_deps_check_cmd> >/dev/null 2>&1 || exit 125
# Exact red-capable repro command (0 = good, 1 = bad)
<repro_test_cmd>
```
*(Remember `chmod +x /tmp/bisect_check.sh`. Ensure dirty working tree is stashed or committed first, or run bisect in a dedicated `git worktree` so active edits stay untouched).*

## 2. Ten Ways to Construct a Tight Feedback Loop (Try in Order)

1. **Failing automated test** at the narrowest seam reaching the bug (unit / integration / e2e).
2. **Scripted HTTP call** (`curl`/script) against a local dev server asserting the exact bad response.
3. **CLI invocation** with minimal fixture input diffing stdout/stderr against expected output.
4. **Headless browser check** asserting on DOM state, console error, or failed network request.
5. **Trace replay:** replay a captured HAR, request payload, webhook body, or queue message.
6. **Throwaway harness** booting only the smallest slice of the system to invoke the failing path.
7. **Property / fuzz loop** for intermittent wrong output over a wide input space.
8. **Bisection harness** (`git bisect run` above) when the failure is a regression between two refs.
9. **Differential loop** comparing old vs new version, two configs, or two datasets.
10. **Structured human-in-the-loop script** only as a last resort when manual UI/hardware triggers are unavoidable.

### Tightening & Flake Amplification
- **Faster:** cache setup, narrow test filter, mock unrelated slow boundaries.
- **Sharper:** assert the exact symptom, never generic *"exit 0 / didn't crash"*.
- **Deterministic:** pin clock/timezone, seed RNG, isolate temp dirs. For flaky bugs, amplify reproduction rate first (`for i in $(seq 1 100); do <cmd> || break; done`, add concurrency/stress) — a 50% flake is debuggable; a 1% flake is not.

## 3. Red Flags & Rationalizations (STOP → Return to Phase 1)

| Tempting Excuse | Reality |
| :--- | :--- |
| *"It's simple, just apply a quick fix"* | Simple symptoms often hide upstream state corruption. Phase 1 takes 2 minutes and prevents rework. |
| *"Emergency — no time for process"* | Systematic debugging is faster than blind guess-and-check thrashing. |
| *"Change 3 things at once to save runs"* | You cannot isolate what fixed it and you mask/create new bugs. |
| *"Let's run `evolve` / AI patches until tests pass"* | Reward hacking on an undiagnosed bug masks symptoms instead of fixing root cause. |
| *"Just one more fix attempt" (after 2+ failures)* | **3+ failures = architectural mismatch.** Stop and escalate to the user. |
| *"I'll write the regression test later"* | Untested fixes regress silently; write RED first so GREEN proves the root cause is gone. |
