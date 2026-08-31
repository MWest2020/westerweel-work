#!/usr/bin/env bash
# PreToolUse-hook (matcher: Bash) — blokkeert force-pushes.
# Sessie "Shift left — hooks > goede bedoelingen", zie /slides/claude-shift-left/
#
# Principes (slide 25):
# - tokenize, geen regex-acrobatiek: splits het commando en vergelijk exact
# - faal dicht bij twijfel: kan de input niet gelezen worden -> blokkeer
# - een hook is code: draai ./deny-force-push.sh --self-test
set -u

block() {
  echo "BLOCKED: een force-push herschrijft geschiedenis op de remote." >&2
  echo "Dat vereist expliciete bevestiging van een mens." >&2
  exit 2
}

check_cmd() {
  # tokenize op whitespace; vlag telt alleen ná 'git ... push' in hetzelfde
  # deelcommando (; && || | beginnen opnieuw). Bewust simpel en auditbaar.
  local w seen_git=0 seen_push=0
  for w in $1; do
    case "$w" in
      ';'|'&&'|'||'|'|') seen_git=0; seen_push=0 ;;
      git)  seen_git=1 ;;
      push) [ "$seen_git" -eq 1 ] && seen_push=1 ;;
      --force|-f|--force-with-lease|--force-if-includes)
            [ "$seen_push" -eq 1 ] && return 1 ;;
    esac
  done
  return 0
}

if [ "${1:-}" = "--self-test" ]; then
  blocked=0; passed=0; fail=0
  must_block=("git push --force origin main" "git push -f")
  must_pass=("git push origin main" "rm -f /tmp/scratch && git status")
  for c in "${must_block[@]}"; do
    if check_cmd "$c"; then echo "FAIL (had moeten blokkeren): $c" >&2; fail=1; else blocked=$((blocked+1)); fi
  done
  for c in "${must_pass[@]}"; do
    if check_cmd "$c"; then passed=$((passed+1)); else echo "FAIL (had door gemoeten): $c" >&2; fail=1; fi
  done
  [ "$fail" -eq 0 ] && echo "self-test OK (${blocked} geblokkeerd, ${passed} doorgelaten)" || exit 1
  exit 0
fi

payload=$(cat)
cmd=$(printf '%s' "$payload" | python3 -c '
import json, sys
d = json.load(sys.stdin)
print(d.get("tool_input", {}).get("command", ""))
' 2>/dev/null) || block   # input niet te inspecteren -> faal dicht

check_cmd "$cmd" || block
exit 0
