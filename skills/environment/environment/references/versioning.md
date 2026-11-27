# Versioning (Git Proxies, Worktrees & Concurrency Boundaries)

Load this reference for git security boundaries, parallel agent isolation, conflict resolution, and host-agnostic releases.

## 1. Git as a Security Boundary

- **Hide raw git credentials behind a local proxy:** Hold PATs/keys in a root-owned loopback proxy (`127.0.0.1`) that attaches auth only to allowlisted repos/branches and blocks direct pushes or force-pushes to protected branches (`main`, `master`, release branches).
- **Enforce policy in hooks, not prose:** Use `pre-commit`, `commit-msg`, and `pre-receive` hooks to reject secret leaks, forbidden paths, malformed messages, and protected-branch writes automatically.

## 2. Pre-Edit & Parallel Worktree Protocol

Before reporting state, proposing work, or editing any shared repository:

1. **Read truth from disk:** Run `git status -sb` and `git log --oneline -10`. Never report branch state, file contents, or test counts from memory.
2. **Respect foreign WIP:** If `git status` shows changes you did not make, inspect `git diff` immediately. Never run `git add .` in a shared tree — stage explicit file paths or branch into your own worktree.
3. **One agent, one branch, one worktree (on persistent storage):**
   ```bash
   git worktree add -b feat/<topic> /srv/worktrees/<repo>-<topic> main
   ```
   Assign disjoint files per parallel worker; handle shared wiring/imports centrally during integration.
4. **Respect `.gitignore`:** Run `git log -1 -- .gitignore` before `git add -f` on an ignored path so you do not fight an intentional exclusion.

## 3. Integration, Conflicts & Verification Gate

1. **Verify worker output on disk:** Do not trust a subagent's "done" message — inspect `git -C <worktree> log --oneline -1`, verify files exist, and run tests yourself.
2. **Merge by preserving BOTH intents:** When two valid branches touch adjacent lines, read both diffs and combine both behaviors instead of blindly picking `ours`/`theirs`.
3. **Never rewrite pushed history:** Do not `--amend` or force-push shared commits; add a corrective commit instead.
4. **Stay forge-agnostic:** Stick to portable `git` primitives (`status`, `diff`, `worktree`, `merge`, `tag`, `push`), conventional commits, and annotated semver tags (`git tag -a v0.1.0 -m "v0.1.0"`).

## Completion Checklist

- [ ] `grep -rc '<<<<<<<'` returns `0` across merged files.
- [ ] Full test suite passes after merge (count reflects combined additions, not one branch's subset).
- [ ] `git status -sb` confirms clean sync (`## <branch>...origin/<branch>`) and `git log -1` shows the intended commit.
