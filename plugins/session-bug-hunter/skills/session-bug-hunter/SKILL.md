---
name: session-bug-hunter
description: >
  Analyzes the current Claude Code session — conversation history AND changed
  code files — to detect potential bugs, technical debt, regressions, and
  performance issues, then creates structured GitHub issues for each one after
  user approval. Always use this skill when the user says "find bugs", "open
  issues", "create github issues", "bug report", "what bugs did we introduce",
  "session bugs", "hunt bugs", "report issues to github", or anything implying
  they want to capture problems from the current session as GitHub issues.
  Also trigger proactively when the user is wrapping up a session and there
  were visible errors, workarounds, or "fix later" comments during the session.
compatibility:
  tools: [bash, create_file]
  requires: gh CLI (GitHub CLI) authenticated — run `gh auth status` to verify
---

# Session Bug Hunter

Scans the current Claude Code session (conversation + changed files) for bugs
and potential issues, presents a prioritized list for user approval, then
creates GitHub issues automatically.

---

## Phase 1 — Detect the GitHub repo

Before anything else, run:

```bash
gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null
```

If this fails:
- Ask the user: "Which GitHub repo should I open issues in? (e.g. owner/repo)"
- Store the answer for all subsequent `gh issue create` calls.

Also check gh auth:
```bash
gh auth status 2>&1
```

Parse the output carefully:
- If output contains `Logged in to` AND `Active account: true` → auth is OK, proceed silently.
- If output contains `Logged in to` but no active account → run `gh auth switch` to activate.
- If output contains no `Logged in to` at all → tell the user:
  > "GitHub CLI is not authenticated. Run `gh auth login` first, then retry."
  > Stop here — do not proceed.

**Important:** Multiple accounts (e.g. github.com + github.company.cloud) is normal and valid.
Do NOT treat multiple accounts as an error. Only fail if there is truly no authenticated account.
Always use the account where `Active account: true` appears.

---

## Phase 2 — Scan for bugs

### 2a. Scan the conversation history

Read the entire conversation from top to bottom. Extract signals of problems:

**Hard signals** (almost certainly a bug):
- Error messages, stack traces, exceptions that appeared during the session
- Cases where something was tried, failed, and a workaround was applied
- Explicit statements: "this is a hack", "fix this later", "TODO", "FIXME",
  "this will break if...", "edge case we're ignoring", "not handling X"
- Retry loops — if the same problem was attempted more than once

**Soft signals** (potential issues worth flagging):
- "We should probably...", "ideally this would...", "technically this could..."
- Missing error handling noticed but not addressed
- Race conditions or concurrency issues mentioned in passing
- Security concerns mentioned (missing auth, exposed secrets, SQL injection risks)
- Performance notes ("this query might be slow", "N+1 problem here")

### 2b. Scan changed files

Run:
```bash
git diff --name-only HEAD 2>/dev/null || git status --short 2>/dev/null
```

For each changed file, read it and look for:
- `TODO`, `FIXME`, `HACK`, `XXX`, `BUG`, `TEMP` comments
- Empty catch blocks: `catch {}`, `except: pass`
- Hardcoded values that should be config/env vars (URLs, ports, credentials)
- Missing null/undefined checks before property access
- `console.log` / `print` / `debugger` statements left in
- Obvious off-by-one errors or boundary condition issues
- Functions that grew too large during the session (>80 lines, high complexity)

---

## Phase 3 — Build the bug list

For each detected issue, create a structured entry:

```
ID: BUG-001
Title: [concise, actionable — verb + noun, e.g. "UserService crashes on empty email input"]
Type: bug | tech-debt | regression | performance
Severity: critical | high | medium | low
Source: conversation | code | both
File: path/to/file.ts (line N) — if applicable
Description: 2-3 sentences. What is the problem, where does it occur,
             what is the risk or impact if left unfixed.
Reproduction: Step-by-step if inferable from context. "Unknown" if not.
Suggested fix: One sentence if obvious from context. "Needs investigation" if not.
```

**Severity rules:**
- `critical` — data loss, security vulnerability, auth bypass, crash on common path
- `high` — feature broken, workaround applied, error swallowed silently
- `medium` — edge case unhandled, tech debt with clear risk, degraded performance
- `low` — TODO comments, code style issues, minor optimizations, debug logs left in

**Deduplication:** If the same issue appears in both conversation and code,
merge into one entry with `Source: both`.

---

## Phase 4 — Present for approval

Display the full list clearly before opening anything:

```
🔍 Session Bug Hunter — Found N potential issues
═══════════════════════════════════════════════

[CRITICAL] BUG-001 · bug
UserService crashes on empty email input
📁 src/services/user.ts:47
Seen in: conversation + code
─────────────────────────────────────────
The validateUser() function does not guard against null/empty email before
calling .toLowerCase(), causing a TypeError in production when email is
omitted from the request body. A workaround was applied during this session
but the root cause was not fixed.

[HIGH] BUG-002 · tech-debt
JWT secret hardcoded in auth middleware
📁 src/middleware/auth.ts:12
Seen in: code
─────────────────────────────────────────
...

[MEDIUM] BUG-003 · performance
...

───────────────────────────────────────────────────────
Which issues should I open as GitHub issues?
Type: "all", "1,2,3", "critical only", "high and above", or "none"
```

Wait for the user's response before proceeding.

---

## Phase 5 — Create GitHub issues

For each approved bug, create a GitHub issue using this exact template:

**Issue title:**
```
[{TYPE}] {Title}
```

**Issue body:**
```markdown
## 🐛 Description
{Description}

## 📍 Location
{File and line if available, otherwise "See session context"}

## 🔁 Steps to Reproduce
{Reproduction steps or "Needs investigation"}

## 💡 Suggested Fix
{Suggested fix}

## 📊 Metadata
- **Severity**: {severity}
- **Type**: {type}
- **Detected by**: session-bug-hunter skill
- **Session date**: {YYYY-MM-DD}
- **Source**: {conversation | code | both}

---
*Auto-generated from Claude Code session analysis*
```

**Labels to apply** (use `--label` flag, create if missing):
- Severity: `critical`, `high`, `medium`, `low`
- Type: `bug`, `tech-debt`, `regression`, `performance`

Run for each approved issue:
```bash
gh issue create \
  --repo {owner/repo} \
  --title "[{TYPE}] {Title}" \
  --body "{body}" \
  --label "{severity},{type}"
```

If a label doesn't exist yet, create it first:
```bash
gh label create "{label}" --color "{color}" --repo {owner/repo}
```

Label colors:
- `critical` → `#d73a4a`
- `high` → `#e4e669`
- `medium` → `#0075ca`
- `low` → `#cfd3d7`
- `bug` → `#d73a4a`
- `tech-debt` → `#e4e669`
- `regression` → `#d93f0b`
- `performance` → `#0075ca`

---

## Phase 6 — Summary report

After all issues are created, output:

```
✅ Session Bug Hunter — Done

Opened N GitHub issues in {owner/repo}:
  #142 [CRITICAL] UserService crashes on empty email input
  #143 [HIGH] JWT secret hardcoded in auth middleware
  #144 [MEDIUM] Missing pagination on /api/users endpoint

Skipped: BUG-003 (user declined)
No issues found for: BUG-005 (duplicate of existing #138)

Run `gh issue list --label bug` to view all open bugs.
```

---

## Edge cases

- **No bugs found**: Say "No bugs or issues detected in this session. 
  The session looks clean! 🎉" — do not open any issues.
- **gh CLI missing**: Tell user to install via `brew install gh` or 
  https://cli.github.com and retry.
- **Duplicate detection**: Before creating an issue, run:
  ```bash
  gh issue list --search "{title}" --state open --json number,title
  ```
  If a near-identical issue exists, flag it and ask the user whether to
  open a new one or skip.
- **No git repo**: Skip Phase 2b entirely, scan conversation only.
- **Private repo / no permissions**: Surface the error message clearly and 
  ask user to check repo access with `gh repo view`.

---

## Trigger phrases → behavior

| User says | Action |
|-----------|--------|
| "find bugs from this session" | Run full flow |
| "open github issues for what we found" | Run full flow |
| "what bugs did we introduce?" | Run full flow |
| "create issues for the TODOs we left" | Run full flow, focus on TODOs |
| "just critical bugs to github" | Run flow, pre-filter to critical only |
| "bug report" | Run full flow |
