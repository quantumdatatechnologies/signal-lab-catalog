#!/bin/bash
# Secret and internal-content scan for the public repo. Fails if anything private-looking is found.
# Maintainers can add extra private patterns (one ERE per line) in .scan-private, which is git-ignored.
cd "$(dirname "$0")/.."
FILES=$(git ls-files 2>/dev/null || find . -type f -not -path './.git/*')
FILES=$(echo "$FILES" | grep -v -E '^(data/|scripts/check-no-internal-content.sh)')
DATA="data/catalog.json data/catalog.csv"
P_SECRET='([Pp]assword[[:space:]]*[:=]|ghp_|gho_|github_pat_|sk-[A-Za-z0-9]{20}|AKIA[0-9A-Z]{16}|xox[bap]-|-----BEGIN [A-Z ]*PRIVATE KEY|Bearer [A-Za-z0-9._-]{20,}|[A-Z_]*_TOKEN)'
P_GENERIC='((^|[[:space:]"(])/home/[a-z]+|\.internal\b|localhost|127\.0\.0\.1|(^|[^0-9.])(10|192\.168|172\.(1[6-9]|2[0-9]|3[01]))\.[0-9]+\.[0-9]+\.[0-9]+)'
PATS=("$P_SECRET" "$P_GENERIC")
if [ -f .scan-private ]; then
  while IFS= read -r l; do [ -n "$l" ] && PATS+=("$l"); done < .scan-private
fi
N=0
for pat in "${PATS[@]}"; do
  for f in $FILES $DATA; do
    [ -f "$f" ] || continue
    OUT=$(grep -n -E "$pat" "$f" | grep -v 'Treasury Bill' | sed "s|^|$f:|" | cut -c1-200)
    [ -n "$OUT" ] && { echo "$OUT"; N=1; }
  done
done
[ $N = 0 ] && echo "OK: no secrets or internal content found" || { echo "FOUND matches above"; exit 1; }
