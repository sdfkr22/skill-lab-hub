---
name: session-summarizer
description: >
  Summarizes the current Claude Code session — the entire conversation from
  start to now — into a structured, readable report covering goals, decisions,
  changes made, open questions, and next steps. Always use this skill when the
  user says "özetle", "özet", "özet çıkar", "oturumu özetle", "konuşmayı özetle",
  "session özeti", "summarize", "summarize this session", "summary", "recap",
  "tldr", "wrap up", or anything implying they want a digest of what was
  discussed and done. Also trigger proactively when the user signals end of
  session ("bitirelim", "tamam bu kadar", "done for today") and a summary
  would help them resume later.
compatibility:
  tools: [bash]
  requires: none
---

# Session Summarizer

Reads the current Claude Code session and produces a clean, structured summary
the user can paste into notes, share with teammates, or use to resume work in a
future session.

The summary is **language-matched**: if the conversation has been in Turkish,
output Turkish. If English, output English. If mixed, follow the user's most
recent messages.

---

## Phase 1 — Detect scope

Before summarizing, decide what to cover:

- **Default**: full session from the first user message to the most recent.
- If the user says "son N mesajı özetle" / "summarize the last N messages" →
  scope to that window.
- If the user says "X konusunu özetle" / "summarize the X part" → filter to
  messages relevant to that topic only.
- If the user says "kısaca özetle" / "tldr" / "brief" → produce the short form
  (see Phase 3, "Short form").

Also detect if any files were changed in the session by running:

```bash
git diff --name-only HEAD 2>/dev/null
git status --short 2>/dev/null
```

If there are changed files, include them in the "Changes Made" section.
If not, omit that section entirely (don't show empty sections).

---

## Phase 2 — Extract signals from the conversation

Read the conversation top-to-bottom and pull out:

**Goals & intent**
- What the user originally asked for
- How the goal evolved or was refined mid-session

**Decisions**
- Choices made (e.g. "we decided to use Postgres over SQLite because…")
- Tradeoffs accepted
- Things explicitly ruled out

**Actions taken**
- Files created, edited, or deleted
- Commands run that had meaningful effect (installs, migrations, deploys)
- External operations (PRs opened, issues filed, services called)

**Findings**
- Bugs discovered
- Things learned about the codebase or system
- Surprises or non-obvious behavior uncovered

**Open questions / unresolved**
- Things the user asked but were not answered
- Errors that were worked around but not fixed
- "We'll come back to this" items

**Next steps**
- Explicit TODOs the user stated
- Logical next actions implied by where the session left off

Skip:
- Routine tool calls without meaningful outcome
- Back-and-forth clarifications that didn't change direction
- Anthropic boilerplate / system messages

---

## Phase 3 — Format the output

### Standard form (default)

```markdown
# 📋 Oturum Özeti — {YYYY-MM-DD}

## 🎯 Amaç
{1-2 cümle: kullanıcı bu oturumda ne yapmak istedi}

## ✅ Yapılanlar
- {Eylem 1 — somut, fiil ile başla}
- {Eylem 2}
- {…}

## 🧠 Kararlar
- {Karar 1 — neden alındı}
- {Karar 2}

## 📁 Değişen Dosyalar
- `path/to/file.ext` — {ne değişti, kısaca}
- `path/to/other.ext` — {…}

## 🔍 Bulgular
- {Bulgu 1}
- {Bulgu 2}

## ❓ Açık Konular
- {Cevaplanmamış soru veya çözülmemiş sorun}

## ⏭️ Sonraki Adımlar
- [ ] {TODO 1}
- [ ] {TODO 2}
```

For English sessions, use the same structure with English headers:
`Goal`, `Done`, `Decisions`, `Files Changed`, `Findings`, `Open Questions`,
`Next Steps`.

**Omit any section that has no content.** Do not output empty headers.

### Short form ("tldr" / "kısaca")

3-5 bullet points, no headers:

```markdown
**Özet ({YYYY-MM-DD})**
- {En önemli nokta 1}
- {En önemli nokta 2}
- {Sonraki adım}
```

---

## Phase 4 — Quality rules

- **Be specific.** "Auth middleware refactored" beats "made some changes".
  Name files, functions, decisions.
- **Be honest.** If something failed or was worked around, say so. Don't
  paint over partial work as complete.
- **One pass, no fluff.** No "In this session we explored…" intros, no
  "Hope this helps!" outros. Start with the heading, end with the last bullet.
- **Preserve user voice.** If the user used a specific term ("ingestion
  pipeline", "ödeme akışı"), reuse it instead of paraphrasing.
- **Group related items.** Don't list five separate "edited X" bullets when
  they all belong to one feature — collapse them.
- **Time-anchor open items.** If the user said "Thursday" or "next sprint",
  convert to absolute date (today is {{todays date}}) so the summary stays
  readable later.

---

## Phase 5 — Delivery

Output the summary directly in the chat as markdown. Do **not** write it to
a file unless the user explicitly asks ("dosyaya kaydet", "save to file").

If the user does ask to save:
- Default path: `./session-summary-{YYYY-MM-DD}.md`
- If file exists, append a counter: `-2.md`, `-3.md`
- Confirm the path after writing.

---

## Edge cases

- **Empty / very short session**: If the conversation has fewer than 3
  meaningful exchanges, say:
  > "Oturum çok kısa, özetlenecek bir şey yok henüz."
  > / "Session is too short to summarize yet."
- **Only questions, no actions**: Produce the Goal + Findings + Open Questions
  sections only; skip Done/Files Changed.
- **Multi-topic session**: Group the summary by topic with `## Konu: X`
  subheaders if there were 2+ unrelated workstreams.
- **User asks for re-summary**: If a summary was already produced earlier in
  the session, summarize what happened *since* that point and reference the
  prior summary briefly.

---

## Trigger phrases → behavior

| User says | Action |
|-----------|--------|
| "özetle" / "özet çıkar" | Standard form, full session |
| "kısaca özetle" / "tldr" | Short form |
| "son 10 mesajı özetle" | Standard form, scoped to last N |
| "X konusunu özetle" | Standard form, filtered to topic X |
| "summarize" / "summary" / "recap" | Standard form, English |
| "dosyaya kaydet özeti" | Standard form, write to file |
