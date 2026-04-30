#!/usr/bin/env bash
# Check for horizontal rules (---, ***, ___) outside YAML frontmatter.
# Usage: check-horizontal-rules.sh [file ...]
# Exit 0 if clean, 1 if violations found.

set -euo pipefail

status=0

for file in "$@"; do
  [ -f "$file" ] || continue

  result=$(awk '
    NR == 1 && /^---[[:space:]]*$/ { fm = 1; next }
    fm && /^---[[:space:]]*$/ { fm = 0; next }
    !fm && /^[[:space:]]*[-*_][[:space:]]*[-*_][[:space:]]*[-*_][-*_ ]*$/ {
      printf "%s:%d: horizontal rule found\n", FILENAME, NR
      found = 1
    }
  ' "$file") || true

  if [ -n "$result" ]; then
    echo "$result"
    status=1
  fi
done

if [ "$status" -ne 0 ]; then
  echo ""
  echo "Error: Horizontal rules are not allowed outside YAML frontmatter."
  echo "Use headings (## Section) to separate sections instead."
fi

exit "$status"
