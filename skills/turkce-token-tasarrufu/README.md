# Turkish Token Saver Skill

A Claude Code skill that cuts token usage by ~40-50% in Turkish sessions.

## How it works

Applies a hybrid language strategy:

- **English**: code, comments, commit messages, logs/debug, planning, tool descriptions, file/variable names
- **Turkish**: only user-facing summaries, questions, and chat

Turkish is agglutinative and contains non-ASCII characters (`ğçşıöü`) that consume extra tokens in BPE tokenizers. Keeping the internal work in English yields significant savings while preserving the user experience by keeping the conversation in Turkish.

## Install

This skill ships as part of the [`skill-lab-hub`](https://github.com/sdfkr22/skill-lab-hub) plugin marketplace. In Claude Code:

```
/plugin marketplace add sdfkr22/skill-lab-hub
/plugin install pack@skill-lab-hub
/reload-plugins
```

Or install just this skill standalone:

```
/plugin install turkce-token-tasarrufu@skill-lab-hub
```

Then start writing in Turkish — the skill triggers automatically (`pack:turkce-token-tasarrufu`).

## Token measurement script

`scripts/token_check.py` compares Turkish vs. English token counts.

### Dependencies

Three tokenizer modes — pick what fits:

```bash
# 1. heuristic (no package needed, rough estimate)
python scripts/token_check.py --tokenizer heuristic "text"

# 2. tiktoken (local, fast, GPT-4 tokenizer — approximate for Claude)
pip install tiktoken
python scripts/token_check.py "text"  # default

# 3. anthropic (exact Claude token count, makes an API call)
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
python scripts/token_check.py --tokenizer anthropic "text"
```

### Usage

```bash
# Compare two strings
python scripts/token_check.py "Merhaba dünya" "Hello world"

# Token count for a file
python scripts/token_check.py --file sample.txt

# Compare two files
python scripts/token_check.py --file tr.md --english-file en.md
```

## Disabling hybrid mode

If you want everything in Turkish while the skill is active, tell Claude:

> "Her şey Türkçe olsun" *(Everything in Turkish)*

or

> "Yorumları da Türkçe yaz" *(Write the comments in Turkish too)*

The skill steps aside on its own.
