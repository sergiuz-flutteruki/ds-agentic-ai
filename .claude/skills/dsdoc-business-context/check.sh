#!/usr/bin/env bash
# Script check for business_context.md: sections, footnote targets, pending items.
# Usage: check.sh <business_context.md> <source> [<source> ...]
# Prints one line per failed check; exits 1 if any check fails.

set -u
doc="$1"
shift
sources=("$@")
fail=0

# Required sections, in this order.
required=("Problem" "Proposed models and scope" "Objective and success criteria"
  "Users and decisions" "Not intended for" "Constraints and risks"
  "Stakeholders and validators" "Glossary" "Other"
  "Conflicts between sources" "Open questions")
found=$(grep -E '^## ' "$doc" | sed 's/^## //')
expected=$(printf '%s\n' "${required[@]}")
if [ "$found" != "$expected" ]; then
  echo "FAIL sections: expected, in order:"
  printf '  %s\n' "${required[@]}"
  fail=1
fi

# Every footnote definition: "[^n]: <path> § <heading>", path listed, heading present.
while IFS= read -r line; do
  path=$(echo "$line" | sed -E 's/^\[\^[^]]+\]: *`?//; s/`? *§.*//')
  heading=$(echo "$line" | sed -E 's/^[^§]*§ *//')
  listed=0
  for s in "${sources[@]}"; do [ "$s" = "$path" ] && listed=1; done
  if [ "$listed" -eq 0 ]; then
    echo "FAIL footnote source not listed: $line"
    fail=1
  elif ! grep -qE "^#+ *" "$path" || ! grep -E '^#+ ' "$path" | sed -E 's/^#+ *//' | grep -qxF -- "$heading"; then
    echo "FAIL footnote heading not in $path: $heading"
    fail=1
  fi
done < <(grep -E '^\[\^[^]]+\]:' "$doc")

# Footnotes used without a definition.
for ref in $(grep -oE '\[\^[^]]+\]' "$doc" | sort -u); do
  if ! grep -qF -- "$ref:" "$doc"; then
    echo "FAIL footnote without definition: $ref"
    fail=1
  fi
done

# Every [PENDING] item of the sources appears in the document (first 40 characters).
for s in "${sources[@]}"; do
  while IFS= read -r item; do
    key=$(echo "$item" | sed -E 's/.*\[PENDING\] *//' | cut -c1-40)
    [ -z "$key" ] && continue
    if ! grep -qF -- "$key" "$doc"; then
      echo "FAIL pending item missing (from $s): $key"
      fail=1
    fi
  done < <(grep -F '[PENDING]' "$s")
done

# A gap has no source: an open question about an absence must not cite one, however it is
# worded. Absence = it says so ("not stated", "missing"), asks for a definition, asks who
# uses the output or what is excluded, or names a section that is "—".
empty_sections=$(awk '/^## /{h=substr($0,4); next} /^—$/{print h}' "$doc" | paste -sd'|' -)
gap_re='not (stated|in the source|defined|given|named)|no .* (defined|named)|missing|do not say|does not say|stand for|what do .* mean|who uses|which uses|what uses|excluded'
[ -n "$empty_sections" ] && gap_re="$gap_re|$empty_sections"
gap_hits=$(awk '/^## Open questions/{f=1;next} /^## /{f=0} f' "$doc" \
  | grep -iE "$gap_re" | grep -v '\[PENDING\]' \
  | grep -E '\[\^[^]]+\]')
if [ -n "$gap_hits" ]; then
  echo "FAIL open question states a gap but cites a source:"
  echo "$gap_hits"
  fail=1
fi

# Every section has content or "—".
empty=$(awk '/^## /{if (h && !c) print h; h=$0; c=0; next} /^\[\^/{next} NF{c=1} END{if (h && !c) print h}' "$doc")
if [ -n "$empty" ]; then
  echo "FAIL empty section (write — if the sources have nothing):"
  echo "$empty"
  fail=1
fi

# Quoted text (over 20 characters) is copied exactly from a source.
while IFS= read -r q; do
  found=0
  for s in "${sources[@]}"; do grep -qF -- "$q" "$s" && found=1; done
  if [ "$found" -eq 0 ]; then
    echo "FAIL quote not found in any source: \"$q\""
    fail=1
  fi
done < <(grep -v '^\[\^' "$doc" | grep -oE '"[^"]{21,}"' | sed 's/^"//; s/"$//' | sort -u)

# Sensitive data (shared check).
bash "$(dirname "$0")/../dsdoc/scripts/check_sensitive.sh" "$doc" || fail=1

exit $fail
