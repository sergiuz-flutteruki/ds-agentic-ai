#!/usr/bin/env bash
# Sensitive-data check shared by every dsdoc check.sh: emails, URLs, keys, passwords, hostnames.
# Usage: check_sensitive.sh <document.md>
# Prints one line per hit; exits 1 if any.

set -u
doc="$1"
patterns="$(dirname "$0")/sensitive_patterns.txt"
fail=0
while IFS=$'\t' read -r name re; do
  case "$name" in ''|\#*) continue ;; esac
  hits=$(grep -nE -- "$re" "$doc")
  if [ -n "$hits" ]; then
    echo "FAIL sensitive data ($name):"
    echo "$hits"
    fail=1
  fi
done < "$patterns"
exit $fail
