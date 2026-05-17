#!/bin/bash
#
# Smoke test the built Hugo site.
#
# What this checks (and what it does not):
#   - All expected pages render (file exists in public/).
#   - Translation pairs are wired via hreflang.
#   - Header lang-menu links to the current page's translation, not the
#     home page (regression test for the "switch to EN goes to /en/" bug).
#   - Cookie-banner partial is included on both language homes.
#
# It does NOT exercise JavaScript, does NOT hit the live site, and does
# NOT validate HTML beyond grep-level pattern matches. Run from repo root:
#
#   bash scripts/test-site.sh
#
# Exits non-zero on the first failure.

set -euo pipefail

cd "$(dirname "$0")/.."

readonly PUBLIC_DIR="public"
readonly HUGO_BIN="${HUGO_BIN:-hugo}"

PASS=0
FAIL=0

note() { printf '  %s\n' "$*"; }
ok()   { note "ok   $*"; PASS=$((PASS+1)); }
fail() { note "FAIL $*"; FAIL=$((FAIL+1)); }

assert_file_exists() {
  local f="$1"
  if [[ -f "$f" ]]; then ok "$f exists"
  else fail "$f missing"
  fi
}

assert_grep() {
  local file="$1"
  local pattern="$2"
  local description="${3:-$file matches /$pattern/}"
  if [[ ! -f "$file" ]]; then
    fail "$description (file $file missing)"
    return
  fi
  if grep -qE "$pattern" "$file"; then ok "$description"
  else fail "$description"
  fi
}

assert_not_grep() {
  local file="$1"
  local pattern="$2"
  local description="${3:-$file does NOT match /$pattern/}"
  if [[ ! -f "$file" ]]; then
    fail "$description (file $file missing)"
    return
  fi
  if ! grep -qE "$pattern" "$file"; then ok "$description"
  else fail "$description"
  fi
}

echo "==> building site"
"$HUGO_BIN" --gc --minify --quiet

echo "==> expected pages render"
for f in \
  "$PUBLIC_DIR/index.html" \
  "$PUBLIC_DIR/en/index.html" \
  "$PUBLIC_DIR/diensten/index.html" \
  "$PUBLIC_DIR/en/services/index.html" \
  "$PUBLIC_DIR/about/index.html" \
  "$PUBLIC_DIR/en/about/index.html" \
  "$PUBLIC_DIR/posts/index.html" \
  "$PUBLIC_DIR/en/posts/index.html"
do
  assert_file_exists "$f"
done

echo "==> no stale page at root /services/ or /en/diensten/"
# Regression guard: services.md must not bleed to root, diensten.md must not bleed to /en/.
if [[ -f "$PUBLIC_DIR/services/index.html" ]]; then
  fail "$PUBLIC_DIR/services/index.html should not exist (EN services belongs at /en/services/)"
else
  ok "no stray /services/ at root"
fi
if [[ -f "$PUBLIC_DIR/en/diensten/index.html" ]]; then
  fail "$PUBLIC_DIR/en/diensten/index.html should not exist"
else
  ok "no stray /en/diensten/"
fi

echo "==> hreflang pairs"
assert_grep "$PUBLIC_DIR/diensten/index.html"        'hreflang=en href=https://westerweel.work/en/services/' "diensten -> en/services hreflang"
assert_grep "$PUBLIC_DIR/en/services/index.html"     'hreflang=nl href=https://westerweel.work/diensten/'    "en/services -> diensten hreflang"
assert_grep "$PUBLIC_DIR/about/index.html"           'hreflang=en href=https://westerweel.work/en/about/'    "about -> en/about hreflang"
assert_grep "$PUBLIC_DIR/en/about/index.html"        'hreflang=nl href=https://westerweel.work/about/'       "en/about -> about hreflang"

echo "==> header lang-menu links to current-page translation, not home"
# The lang-menu block in the header must contain the translated page URL,
# not the bare language home. Pattern matches "lang-menu" followed by the
# translated path within the same <ul>.
assert_grep "$PUBLIC_DIR/diensten/index.html"    'lang-menu[^<]*<li>[^<]*<a href=[^>]*/en/services/'  "header on /diensten/ links to /en/services/"
assert_grep "$PUBLIC_DIR/en/services/index.html" 'lang-menu[^<]*<li>[^<]*<a href=[^>]*/diensten/'     "header on /en/services/ links to /diensten/"
assert_grep "$PUBLIC_DIR/about/index.html"       'lang-menu[^<]*<li>[^<]*<a href=[^>]*/en/about/'     "header on /about/ links to /en/about/"
assert_grep "$PUBLIC_DIR/en/about/index.html"    'lang-menu[^<]*<li>[^<]*<a href=[^>]*/about/'        "header on /en/about/ links to /about/"

echo "==> cookie banner partial included"
assert_grep "$PUBLIC_DIR/index.html"    'cookie-term' "NL home includes cookie banner partial"
assert_grep "$PUBLIC_DIR/en/index.html" 'cookie-term' "EN home includes cookie banner partial"

echo "==> home intro flips per language"
assert_grep    "$PUBLIC_DIR/index.html"    'Ik bouw' "NL home intro is Dutch"
assert_grep    "$PUBLIC_DIR/en/index.html" 'I build' "EN home intro is English"
assert_not_grep "$PUBLIC_DIR/en/index.html" 'Ik bouw' "EN home intro is NOT Dutch"

echo
echo "==> $PASS passed, $FAIL failed"
[[ "$FAIL" -eq 0 ]]
