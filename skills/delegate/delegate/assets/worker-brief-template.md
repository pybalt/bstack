# Worker Assignment: <short-title>

- **Role:** Explorer | Implementer | Adversarial Reviewer | Spike Runner | Evolve Island
- **Model Family Target:** `<e.g., different family from author if reviewing or running evolve>` (Privacy Tier verified: `Tier A | Tier B`)
- **Workspace Mode:** Read-Only | Isolated Worktree (`<branch/path>`) | Disjoint Owned Files
- **Goal (observable outcome):** `<1–2 concrete sentences>`
- **Owned Files (allowed to edit):** `<exact paths or READ-ONLY>`
- **Do-Not-Touch Boundaries:** `<files, schemas, immutable evaluators, lockfiles off-limits>`
- **Context & Contracts:** `<minimal slice of Decision Brief / ODD tracker / repo rules>`
- **Required Verification Command(s):** `<exact command(s)>`
- **Retry Cap:** Max 2 bounded self-correction attempts; stop and report root blocker if still failing.

## Required Return Format
1. Changed files + concise summary of changes and why.
2. Exact commands executed + observed output (strictly separate **Verified** vs **Not Run**).
3. Risks, open edge cases, or blockers discovered.
