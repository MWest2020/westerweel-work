# Shift left — hooks > goede bedoelingen

Materiaal bij de sessie. De slides staan op
[westerweel.work/slides/claude-shift-left/](https://westerweel.work/slides/claude-shift-left/)
(pijltjes/spatie om te navigeren, `F` voor fullscreen; de
[leesversie](https://westerweel.work/slides/claude-shift-left/lees/) heeft
alle 25 slides onder elkaar).

## Wat hier staat

| Bestand | Wat het is |
|---|---|
| `hooks/deny-force-push.sh` | PreToolUse-guard: blokkeert `git push --force` met `exit 2` — de tool draait dan niet |
| `hooks/lint-changed-file.sh` | PostToolUse-feedbackloop: shellcheck op het zojuist geschreven bestand; `exit 2` geeft stderr terug aan het model, dat het zelf repareert |
| `settings.example.json` | De wiring voor `.claude/settings.json` (projectniveau, in git) |

## Zelf proberen (de hands-on van slide 19)

```bash
# 1. kopieer de hooks naar je project
mkdir -p .claude/hooks
cp hooks/*.sh .claude/hooks/ && chmod +x .claude/hooks/*.sh

# 2. wire ze in .claude/settings.json (zie settings.example.json)

# 3. bewijs dat ze doen wat je denkt — een hook is code
.claude/hooks/deny-force-push.sh --self-test
.claude/hooks/lint-changed-file.sh --self-test

# 4. laat de agent iets kapots schrijven en kijk of hij het zélf repareert
```

## De principes (kort)

- **CLAUDE.md is advies, hooks zijn afdwinging.** Context ≠ enforcement; zie
  slide 07–09 en [docs/en/memory](https://code.claude.com/docs/en/memory).
- **De grens is niet "belangrijk of niet"** maar: heeft de check meer nodig
  dan één bestand? Eén bestand → hook (ms). Meer → CI (de gate blijft).
- **Faal open bij ontbrekende tools, faal dicht bij oninspecteerbare input.**
- **Tokenize, geen regex-acrobatiek** — en onthoud: een hook matcht tekst,
  geen intentie (slide 15).
- **Een hook is code**: self-test, timeout, code review.

Licentie: zie de root van deze repo.
