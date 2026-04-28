# 🐛 session-bug-hunter

> A Claude Code skill that scans your coding session for bugs and opens GitHub issues automatically — no manual reporting needed.

---

## What it does

Most bugs found during a session never get reported. You fix the urgent ones, note the rest with a "TODO", and forget them by next week. **session-bug-hunter** solves this by scanning everything that happened in your session — the conversation, the errors, the workarounds, the changed files — and turning them into structured GitHub issues before you close the tab.

**It scans two sources:**
- 💬 **Conversation history** — error messages, stack traces, "fix this later" comments, failed attempts, security concerns mentioned in passing
- 📁 **Changed files** — `TODO/FIXME/HACK` comments, empty catch blocks, hardcoded credentials, missing null checks, debug logs left in

**It classifies every issue by:**
- Severity: `critical` / `high` / `medium` / `low`
- Type: `bug` / `tech-debt` / `regression` / `performance`

**Then:**
1. Shows you the full list before doing anything
2. Waits for your approval (`all`, `1,2,3`, `critical only`, etc.)
3. Creates structured GitHub issues with labels, location, reproduction steps, and suggested fix

---

## Demo

```
You: find bugs from this session

🔍 Session Bug Hunter — Found 3 potential issues
═══════════════════════════════════════════════

[CRITICAL] BUG-001 · bug
SQL injection in user search endpoint
📁 src/controllers/user.ts:84
Seen in: code
─────────────────────────────────────
Raw user input is passed directly into the query string without
sanitization. An attacker can manipulate the WHERE clause to
extract or delete arbitrary data.

[HIGH] BUG-002 · tech-debt
JWT secret hardcoded in auth middleware
📁 src/middleware/auth.ts:12
Seen in: conversation + code
─────────────────────────────────────
The JWT secret is hardcoded as a string literal. This was flagged
during the session but not addressed. Should be moved to env vars.

[LOW] BUG-003 · low
console.log statements left in payment flow
📁 src/services/payment.ts:34,67
Seen in: code
─────────────────────────────────────
Two console.log calls that log request payloads were left in
after debugging. These may leak sensitive data in production logs.

───────────────────────────────────────────────────────
Which issues should I open as GitHub issues?
Type: "all", "1,2,3", "critical only", "high and above", or "none"

You: 1,2

✅ Opened 2 GitHub issues in sdfkr22/my-api:
  #47 [CRITICAL] SQL injection in user search endpoint
  #48 [HIGH] JWT secret hardcoded in auth middleware
```

---

## Install

**Option A — Global (available in all projects):**
```bash
gh repo clone sdfkr22/session-bug-hunter ~/.claude/skills/session-bug-hunter
```

**Option B — Project-scoped (shared with your team via git):**
```bash
gh repo clone sdfkr22/session-bug-hunter .claude/skills/session-bug-hunter
```

Start a new Claude Code session — the skill loads automatically.

---

## Requirements

- [Claude Code](https://claude.ai/code) installed
- [GitHub CLI](https://cli.github.com) installed and authenticated:
  ```bash
  gh auth login
  gh auth status   # should show Active account: true
  ```

Multiple GitHub accounts (e.g. github.com + GitHub Enterprise) are supported — the skill uses whichever account is active.

---

## Usage

Just talk to Claude naturally at the end of your session:

```
find bugs from this session
open github issues for what we found
what bugs did we introduce?
create issues for the TODOs we left
just critical bugs to github
```

The skill also triggers proactively when it detects you're wrapping up ("done", "that's it for today") and there were visible errors or workarounds during the session.

---

## GitHub issue format

Each opened issue includes:

```markdown
## 🐛 Description
...

## 📍 Location
src/middleware/auth.ts:12

## 🔁 Steps to Reproduce
...

## 💡 Suggested Fix
...

## 📊 Metadata
- Severity: high
- Type: tech-debt
- Detected by: session-bug-hunter skill
- Session date: 2026-04-28
- Source: conversation + code
```

Labels are created automatically if they don't exist yet.

---

## How it works

Claude Code gives the skill access to the full conversation history and the filesystem. When triggered, the skill:

1. Verifies GitHub CLI auth
2. Detects the current repo via `gh repo view`
3. Reads the entire session conversation looking for bug signals
4. Runs `git diff` and scans changed files for code-level issues
5. Deduplicates (same bug in conversation + code = one issue)
6. Checks for existing open issues before creating duplicates
7. Creates issues via `gh issue create` with structured body and labels

---

## Contributing

PRs welcome. If you find a bug in the bug hunter, the irony is not lost on us — please open an issue.

---

*Built with [Claude Code](https://claude.ai/code) · Licensed under MIT*
