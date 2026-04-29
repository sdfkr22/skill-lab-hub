# skill-lab-hub

Personal Claude Code skills, packaged as a plugin marketplace.

## Skills

- **session-bug-hunter** — Analyzes the current session and opens structured GitHub issues for bugs / tech debt found.
- **turkce-token-tasarrufu** — Hybrid Turkish/English mode that cuts token usage ~40-50% in Turkish sessions.

## Install

In Claude Code:

```
/plugin marketplace add sdfkr22/skill-lab-hub
/plugin install pack@skill-lab-hub
```

For local development, point the marketplace at a clone instead:

```
/plugin marketplace add /path/to/skill-lab-hub
```

## Adding a new skill

1. Create `skills/<skill-name>/SKILL.md` with frontmatter (`name`, `description`).
2. Add `"./skills/<skill-name>"` to the `skills` array in `.claude-plugin/marketplace.json`.
3. Bump `metadata.version` in the same file.
4. Run `/plugin marketplace update skill-lab-hub` in Claude Code.
4. Commit.

## Layout

```
.
├── .claude-plugin/
│   └── marketplace.json
└── skills/
    ├── session-bug-hunter/
    └── turkce-token-tasarrufu/
```
