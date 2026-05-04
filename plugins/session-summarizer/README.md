# 📋 session-summarizer

> A Claude Code skill that turns your current session into a clean, structured summary — ready to paste into notes, share with teammates, or use to resume work tomorrow.

---

## What it does

Long Claude Code sessions are hard to recap. By message 80 you've forgotten what was decided at message 20, which TODOs are still open, and which files you actually touched. **session-summarizer** reads the entire conversation (plus `git diff`) and produces a structured digest covering goals, decisions, changes, findings, open questions, and next steps.

**Language-aware:** if you've been chatting in Turkish, the summary is in Turkish. English sessions get English summaries. Mixed sessions follow your most recent messages.

---

## Demo

```
You: summarize

# 📋 Session Summary — 2026-05-04

## 🎯 Goal
Refactor the payment service's Stripe integration and increase test coverage.

## ✅ Done
- Stripe calls in `src/services/payment.ts` moved into a new `StripeClient` class
- Signature verification added to the webhook handler
- 4 new unit tests written, coverage 62% → 78%

## 🧠 Decisions
- Used UUID v7 for idempotency key generation (sortable → more efficient DB index)
- Retry logic kept at the queue layer, not inside the SDK

## 📁 Files Changed
- `src/services/payment.ts` — Stripe calls extracted
- `src/clients/stripe-client.ts` — new file
- `src/middleware/webhook.ts` — signature verification

## ❓ Open Questions
- Will old production webhooks pass the new signature check? Not tested yet.

## ⏭️ Next Steps
- [ ] Manually test webhooks in staging
- [ ] Open PR and request review from @backend-team
```

Short form too:

```
You: tldr

**Summary (2026-05-04)**
- Stripe integration moved into StripeClient class
- Webhook signature verification added (not tested in staging)
- Coverage 62% → 78%
- Next: staging test + PR
```

---

## Install

This skill ships as part of the [`skill-lab-hub`](https://github.com/sdfkr22/skill-lab-hub) plugin marketplace. In Claude Code:

```
/plugin marketplace add sdfkr22/skill-lab-hub
/plugin install session-summarizer@skill-lab-hub
/reload-plugins
```

---

## Usage

Just talk to Claude naturally:

**English:**
```
summarize
summary
recap
tldr
summarize this session
summarize the last 10 messages
summarize the X part
save the summary to a file
wrap up
```

**Turkish:**
```
özetle
özet çıkar
oturumu özetle
kısaca özetle
son 10 mesajı özetle
X konusunu özetle
dosyaya kaydet özeti
```

The skill triggers proactively when you signal end of session ("done for today", "that's it", "bitirelim").

---

## What's in the summary

| Section | Content |
|---------|---------|
| 🎯 Goal | What you set out to do |
| ✅ Done | Concrete actions taken |
| 🧠 Decisions | Choices made + why |
| 📁 Files Changed | From `git diff`, with a one-line per-file note |
| 🔍 Findings | Bugs found, things learned |
| ❓ Open Questions | Unresolved items |
| ⏭️ Next Steps | Checkbox TODOs |

Empty sections are omitted — no "no findings" placeholders cluttering the output.

---

## Modes

**Standard** (default) — full structured summary with all relevant sections.

**Short / tldr** — 3-5 bullets, no headers, for quick recaps.

**Scoped** — "summarize the last 10 messages" / "summarize the auth refactor part" limits the summary to a window or topic.

**File output** — "save the summary to a file" writes to `./session-summary-YYYY-MM-DD.md`.

---

## How it works

Claude Code gives the skill access to the full conversation history. When triggered, the skill:

1. Detects the requested scope (full / last N / topic / short form)
2. Runs `git diff --name-only HEAD` to find changed files
3. Reads the conversation top-to-bottom, extracting goals, decisions, actions, findings, open items, next steps
4. Deduplicates and groups related items
5. Outputs a markdown summary in the language matching the conversation

No external services, no API calls — everything runs locally inside the Claude Code session.

---

## Contributing

PRs welcome at [skill-lab-hub](https://github.com/sdfkr22/skill-lab-hub).

---

*Built with [Claude Code](https://claude.ai/code) · Licensed under MIT*
