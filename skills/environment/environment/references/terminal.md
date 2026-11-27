# Terminal, Token Proxies, Audit & Processes

Load this reference for OS/shell selection, CLI output compression, multi-agent observability, credential-free log proxies, and detached processes.

## 1. OS & Shell Gate: Avoid Windows for Coding

```text
IF coding, building, testing, or running agent loops:
   1st choice -> Linux (private VM, container, or WSL2)
   2nd choice -> macOS (POSIX shell)
   Avoid      -> Native Windows (PowerShell / Windows Terminal)
```

- **Why:** Agents fail disproportionately on Windows shells (`;` vs `&&`, quote stripping, CRLF, UTF-8/BOM, `C:/` vs `/c/` paths, console-window flashes).
- **Windows host rule:** If the local laptop runs Windows, keep the coding workspace inside **WSL2, a Linux VM, or Docker** and reserve PowerShell strictly for thin host-side launching/tunnels.

## 2. Token-Saving CLI Output Proxies (`rtk` Pattern)

Verbose `git`, test, lint, and build logs drain context fast during error-fix loops:

- **Wire a failure-preserving CLI compressor:** Use **[RTK (`rtk-ai/rtk`)](https://github.com/rtk-ai/rtk)** (`rtk init -g`; `rtk gain` to measure savings) or content-aware alternatives (`token-saver`, `tamp`) between the agent's shell hook and bash to trim passing noise by **60–90%**.
- **Non-negotiable error rule:** Never use a dumb truncator that strips stack traces, failing test names, assertions, or `file:line` locations — agents will loop blindly. Keep a raw recall command (e.g., `rtk recall`) for full output on demand.
- **Limits:** Shell hooks only compress bash tool calls (not native file-read tools); check license terms (`rtk` uses `Apache-2.0 + BUSL-1.1`) before commercial redistribution.

## 3. Multi-Agent Observability & Credential-Free Debug Proxies

- **Non-intrusive `tmux` panels:** Run each agent role in its own `tmux` session so humans observe read-only (`panel`) without hijacking stdin.
- **Structured bus (`0700` + HMAC):** Use per-role mailboxes with a root-owned router and signed envelopes instead of scraping terminals.
- **Credential-free cross-env log/debug proxies:** Expose narrow read-only proxy tools (`logs tail/query`, `service status/trace`, `metrics/errors`) holding short-lived upstream tokens so agents debug `dev` / `staging` / `prod` in real time **without** raw `gcloud`/`aws`/`kubectl`/APM keys.
  - Require scoped filters (`env`, `service`, `severity`, `trace_id`, bounded time/line cap) so one query never floods context.
  - **Redact inside the proxy** (strip `Authorization` headers, tokens, cookies, credentialed URLs, PII) before output reaches the LLM, and tag external log payloads as `untrusted` data.

## 4. Tamper-Resistant Audit Trail

- Capture execution at kernel level (`auditd` `execve` + `snoopy` `ld.so.preload` outside container write scope) → `rsyslog` → daily append-only JSONL (`chattr +a`, unreadable by agents) shipped off-box with retention.
- Expose team-readable logs only through a redacted view with `untrusted: true` provenance tags.

## 5. Detached Daemons & Process Verification

- **Never trust session-scoped background tools for persistent services:** Detach real daemons (`systemd` with lingering on Linux; Task Scheduler / detached launcher on Windows).
- **Match by `PID` + full `CommandLine`, never binary name:** (`ps -ef` / `pgrep -af` on POSIX; `Win32_Process` / `psutil` on Windows). Pair with log timestamps or heartbeat `mtime` (`presence != progress`), and capture stacks (`py-spy dump --pid <pid>`) before killing.
- **Windows-only daemon fallbacks (if forced onto Windows):**
  - `pythonw.exe` leaves `stdout`/`stderr` as `None` → wire a file logger with `.isatty() -> False`.
  - Venv `pythonw.exe` spawns stub + real interpreter with identical cmdline → group by creation time (~5s window) before deduplicating.
  - Headless subprocesses calling console binaries **must** pass `creationflags=0x08000000` (`CREATE_NO_WINDOW`) and `stdin=subprocess.DEVNULL`.

## 6. Emergency Fallback Table (If Forced onto PowerShell 5.1)

| Operation | PowerShell 5.1 | POSIX Bash |
| :--- | :--- | :--- |
| Chaining | `;` + check `$LASTEXITCODE` (`&&` errors) | `&&` (dependent), `;` (independent) |
| Multi-line / quotes | Write a `.py`/`.ps1` file (double quotes expand `$` and eat `\"`) | `<<'EOF'` heredoc |
| Paths | `C:/path/...` or `C:\path\...` (never `/c/...` for `powershell.exe`) | `/path/...` |
| Encoding | Force UTF-8 output; save accented `.ps1` with UTF-8 BOM | UTF-8 default |
