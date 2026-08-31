#!/usr/bin/env bash
# PostToolUse-hook (matcher: Edit|Write) — lint het zojuist geschreven bestand.
# Sessie "Shift left — hooks > goede bedoelingen", zie /slides/claude-shift-left/
#
# Principes (slide 25):
# - faal open bij ontbrekende tools: geen linter -> hook doet niets
# - timeout, env-tunable: HOOK_LINT_TIMEOUT (default 10s)
# - exit 2 = stderr terug naar het model, dat het bestand zelf repareert
set -u

TIMEOUT="${HOOK_LINT_TIMEOUT:-10}"

lint_file() {
  local file=$1 out
  [ -f "$file" ] || return 0
  case "$file" in
    *.sh)
      command -v shellcheck >/dev/null 2>&1 || return 0   # faal open
      if ! out=$(timeout "$TIMEOUT" shellcheck -f gcc "$file" 2>&1); then
        printf '[shellcheck] %s is niet schoon:\n%s\n' "$file" "$out" >&2
        return 2
      fi ;;
    # breid hier uit met de check die bij JOU het vaakst in de CI faalt:
    # *.php) php -l "$file" ... ;;
    # *.ts|*.vue) node_modules/.bin/eslint "$file" ... ;;
  esac
  return 0
}

if [ "${1:-}" = "--self-test" ]; then
  command -v shellcheck >/dev/null 2>&1 || { echo "self-test overgeslagen: shellcheck ontbreekt (hook faalt dan open)"; exit 0; }
  tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
  # shellcheck disable=SC2016  # fixtures: $1/$USER mogen juist NIET expanderen
  printf '#!/bin/sh\nrm -rf $1/cache\n' > "$tmp/bad.sh"          # SC2086: ongequote var
  printf '#!/bin/sh\ncp "$1" "$1.orig"\necho $USER\n' > "$tmp/bad2.sh"  # idem
  printf '#!/bin/sh\nprintf '\''%%s\\n'\'' "ok"\n' > "$tmp/good.sh"
  printf 'gewoon tekst, geen shell\n' > "$tmp/notes.txt"
  blocked=0; passed=0; fail=0
  for f in "$tmp/bad.sh" "$tmp/bad2.sh"; do
    if lint_file "$f" 2>/dev/null; then echo "FAIL (had moeten blokkeren): $f" >&2; fail=1; else blocked=$((blocked+1)); fi
  done
  for f in "$tmp/good.sh" "$tmp/notes.txt"; do
    if lint_file "$f" 2>/dev/null; then passed=$((passed+1)); else echo "FAIL (had door gemoeten): $f" >&2; fail=1; fi
  done
  [ "$fail" -eq 0 ] && echo "self-test OK (${blocked} geblokkeerd, ${passed} doorgelaten)" || exit 1
  exit 0
fi

payload=$(cat)
file=$(printf '%s' "$payload" | python3 -c '
import json, sys
d = json.load(sys.stdin)
print(d.get("tool_input", {}).get("file_path", ""))
' 2>/dev/null) || exit 0   # feedbackloop, geen gate: bij twijfel niets doen

[ -n "$file" ] || exit 0
lint_file "$file"
exit $?
