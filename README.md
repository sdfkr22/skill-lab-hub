# skill-lab-hub

A personal [Claude Code](https://claude.ai/code) plugin marketplace. Contains a small but growing collection of skills that I use day to day.

## What is this?

Claude Code supports **plugins** — bundles of skills, commands, hooks, and agents you can install with one command. This repo is a *marketplace* (a catalog of plugins) shipping each skill as its own standalone plugin.

## Skills

| Skill | Summary |
|---|---|
| [`session-bug-hunter`](plugins/session-bug-hunter) | Scans the current Claude Code session (conversation + diff) for bugs and tech debt, then opens structured GitHub issues after your approval. |
| [`session-summarizer`](plugins/session-summarizer) | Turns the current session into a structured, language-matched summary covering goals, decisions, changes, open questions, and next steps. Triggered by "özetle" / "summarize". |
| [`turkce-token-tasarrufu`](plugins/turkce-token-tasarrufu) | Hybrid Turkish/English mode that cuts token usage ~40-50% in Turkish sessions by keeping internal work in English while user-facing chat stays Turkish. |

Click a row for full docs and usage examples.

## Install

First, add the marketplace (once):

```
/plugin marketplace add sdfkr22/skill-lab-hub
```

Then install whichever skills you want:

```
/plugin install turkce-token-tasarrufu@skill-lab-hub
/plugin install session-bug-hunter@skill-lab-hub
/plugin install session-summarizer@skill-lab-hub
```

Each plugin exposes its skill under its own namespace (e.g. `turkce-token-tasarrufu:turkce-token-tasarrufu`).

Then `/reload-plugins` after any install.

For local development, point the marketplace at a clone instead:

```
/plugin marketplace add /path/to/skill-lab-hub
```

## Layout

```
.
├── .claude-plugin/
│   └── marketplace.json          # marketplace catalog
├── LICENSE
├── README.md
└── plugins/
    ├── session-bug-hunter/
    │   ├── .claude-plugin/plugin.json
    │   ├── README.md
    │   └── skills/session-bug-hunter/SKILL.md
    ├── session-summarizer/
    │   ├── .claude-plugin/plugin.json
    │   ├── README.md
    │   └── skills/session-summarizer/SKILL.md
    └── turkce-token-tasarrufu/
        ├── .claude-plugin/plugin.json
        ├── README.md
        └── skills/turkce-token-tasarrufu/
            ├── SKILL.md
            └── scripts/
```

## Adding a new skill

1. Create `plugins/<name>/skills/<name>/SKILL.md` with frontmatter (`name`, `description`).
2. Create `plugins/<name>/.claude-plugin/plugin.json` with `name`, `version`, `description`.
3. Add a `README.md` at `plugins/<name>/README.md` explaining what it does.
4. Add a new entry to the `plugins` array in `.claude-plugin/marketplace.json` pointing `source` at `./plugins/<name>`.
5. Commit and push.
6. In Claude Code: `/plugin marketplace update skill-lab-hub` then `/plugin install <name>@skill-lab-hub`.

## Contributing

Issues and PRs welcome. If you build a skill you think belongs here, open a PR — keep one skill per plugin folder, include a `SKILL.md` with proper frontmatter, a `plugin.json`, and a short `README.md`.

## License

[MIT](LICENSE)
