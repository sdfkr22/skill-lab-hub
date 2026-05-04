# skill-lab-hub

A personal [Claude Code](https://claude.ai/code) plugin marketplace. Contains a small but growing collection of skills that I use day to day.

## What is this?

Claude Code supports **plugins** — bundles of skills, commands, hooks, and agents you can install with one command. This repo is a *marketplace* (a catalog of plugins) shipping each skill both as a standalone plugin and bundled together in `pack`.

## Skills

| Skill | Summary |
|---|---|
| [`session-bug-hunter`](skills/session-bug-hunter) | Scans the current Claude Code session (conversation + diff) for bugs and tech debt, then opens structured GitHub issues after your approval. |
| [`session-summarizer`](skills/session-summarizer) | Turns the current session into a structured, language-matched summary covering goals, decisions, changes, open questions, and next steps. Triggered by "özetle" / "summarize". |
| [`turkce-token-tasarrufu`](skills/turkce-token-tasarrufu) | Hybrid Turkish/English mode that cuts token usage ~40-50% in Turkish sessions by keeping internal work in English while user-facing chat stays Turkish. |

Click a row for full docs and usage examples.

## Install

First, add the marketplace (once):

```
/plugin marketplace add sdfkr22/skill-lab-hub
```

**Install everything at once:**

```
/plugin install pack@skill-lab-hub
```

Skills become available under the `pack:` namespace (e.g. `pack:session-bug-hunter`).

**Install a single skill:**

```
/plugin install turkce-token-tasarrufu@skill-lab-hub
/plugin install session-bug-hunter@skill-lab-hub
/plugin install session-summarizer@skill-lab-hub
```

Each standalone plugin exposes its skill under its own namespace (e.g. `turkce-token-tasarrufu:turkce-token-tasarrufu`).

Then `/reload-plugins` after any install.

For local development, point the marketplace at a clone instead:

```
/plugin marketplace add /path/to/skill-lab-hub
```

## Layout

```
.
├── .claude-plugin/
│   └── marketplace.json    # marketplace + plugin manifest
├── LICENSE
├── README.md
└── skills/
    ├── session-bug-hunter/
    │   ├── README.md
    │   └── SKILL.md
    ├── session-summarizer/
    │   ├── README.md
    │   └── SKILL.md
    └── turkce-token-tasarrufu/
        ├── README.md
        ├── SKILL.md
        └── scripts/
```

## Adding a new skill

1. Create `skills/<skill-name>/SKILL.md` with frontmatter (`name`, `description`).
2. Add `"./skills/<skill-name>"` to the `skills` array of the `pack` plugin in `.claude-plugin/marketplace.json`.
3. Optionally add a standalone plugin entry for the skill so users can install it individually.
4. Bump the plugin `version` (and optionally `metadata.version`) in the same file.
5. Commit and push.
6. In Claude Code: `/plugin marketplace update skill-lab-hub` then `/plugin install pack@skill-lab-hub` to refresh.

## Contributing

Issues and PRs welcome. If you build a skill you think belongs here, open a PR — keep one skill per folder, include a `SKILL.md` with proper frontmatter, and add a short `README.md` next to it explaining what it does and how to use it.

## License

[MIT](LICENSE)
