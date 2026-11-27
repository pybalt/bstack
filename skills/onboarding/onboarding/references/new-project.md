# New Project & Workspace Onboarding

Load this reference when starting from an empty directory or when the user explicitly invokes `/onboarding`.

## 1. Hard Interaction Rules

- **One question per turn.** Wait for the answer before asking the next dependent question.
- **Max 3 lines of prose before options.** When choices are finite, offer 2–4 crisp options plus one open escape ("Something else"). Never preselect silently.
- **Never repeat answered facts.** If the user's prompt already covers goal, audience, or stack, acknowledge it in one line and jump straight to the first missing decision.
- **No premature scaffolding.** Do not create files, install packages, or run `git init` until the user approves the Project Seed (unless they explicitly asked to scaffold immediately).
- **Never leak skill internals.** Ask in plain natural language without quoting section titles or workflow rules.

## 2. Guided Intake Sequence (Skip Already-Answered Steps)

1. **Goal & User:** What are we building, who uses it, and what concrete problem must v1 solve?
2. **Surface & Stack:** Runtime/surface (CLI, web app, API/worker, mobile, library, script) and any fixed constraints (prefer Linux/macOS execution per `environment/SKILL.md`).
3. **First Useful Slice (v1):** What single end-to-end workflow proves v1 works? Keep scope tight; reject multi-month roadmaps upfront.
4. **Environment Readiness:** Confirm repo/remote posture, package manager, local runtime, and whether external services/secrets or privacy tiers apply (`environment/references/devex.md`).

## 3. Project Seed & Stop Gate (Completion Criterion)

Once all unknowns are resolved, emit **only** this compact Project Seed (≤ 12 lines) and **STOP** for confirmation:

```markdown
### Project Seed — <name>
- **Goal:** <1 concrete sentence>
- **Surface & Stack:** <runtime, language, minimal deps>
- **v1 Milestone:** <single end-to-end slice>
- **Verification:** <exact command/test that proves v1 works>
- **Next step:** Hand off to `plan` (task breakdown) or `spike` (if feasibility is unproven)
```

End with one clear handoff choice: proceed to `plan` / `spike`, adjust a constraint, or scaffold immediately.
