#!/usr/bin/env bash
# Script check for model_card.md: footnotes, metric values, sections, open questions, source names.
# Usage: check.sh <model_card.md> [dsdoc.yaml]
# Prints one line per failed check; exits 1 if any check fails.

set -u
card="$1"
yaml="${2:-dsdoc.yaml}"
fail=0

# Every file:line or file:a-b in a footnote, with or without backticks; a range is checked by its end.
while IFS= read -r ref; do
  f="${ref%%:*}"; l="${ref##*:}"; l="${l##*-}"
  if [ ! -f "$f" ]; then
    echo "FAIL footnote file not found: $ref"; fail=1
  elif [ "$l" -gt "$(awk 'END{print NR}' "$f")" ]; then
    echo "FAIL footnote line past end of file: $ref"; fail=1
  fi
done < <(grep -E '^\[\^[^]]+\]:' "$card" | grep -oE '[A-Za-z0-9_./-]+\.(py|sql):[0-9]+(-[0-9]+)?' | sort -u)

# Every metric value in dsdoc.yaml is in the Evaluation table (before the first ### of the
# section), on the metric's own row, as written. A copy elsewhere (e.g. a baseline table)
# does not count.
if [ -f "$yaml" ]; then
  eval_table=$(awk '/^## Evaluation/{f=1;next} /^## |^### /{f=0} f' "$card")
  while IFS= read -r kv; do
    [ -z "$kv" ] && continue
    k=$(echo "$kv" | sed -E 's/^ *([^:]+):.*/\1/'); v=$(echo "$kv" | sed -E 's/.*: *//')
    rows=$(echo "$eval_table" | grep -F "\`$k\`")
    if [ -z "$rows" ]; then
      echo "FAIL metric missing from the Evaluation table: $k"; fail=1
    elif ! echo "$rows" | grep -qE "\| *${v//./\\.} *\|"; then
      echo "FAIL metric value changed in the Evaluation table: $k = $v"; fail=1
    fi
  done < <(awk '/^  metrics:/{f=1;next} /^  [a-z_]+:/{f=0} f' "$yaml" | grep -oE '^ +[A-Za-z0-9_]+: *[0-9.]+')
fi

# Required sections, in this order (Business context, Not intended for, Variants are optional).
order=$(grep -E '^## ' "$card" | sed 's/^## //' | grep -vxE 'Business context|Not intended for|Variants')
expected=$(printf '%s\n' Overview Data Preprocessing Features Model Evaluation Output Limitations "Open Questions")
if [ "$order" != "$expected" ]; then
  echo "FAIL sections: expected Overview, [Business context], [Not intended for], [Variants], Data, Preprocessing, Features, Model, Evaluation, Output, Limitations, Open Questions"
  fail=1
fi

# At most 8 open questions, and the stated count matches.
n=$(awk '/^## Open Questions/{f=1;next} /^## |^---/{f=0} f' "$card" | grep -cE '^[0-9]+\. ')
stated=$(grep -oE '^Open questions: [0-9]+' "$card" | grep -oE '[0-9]+$')
[ "$n" -le 8 ] || { echo "FAIL more than 8 open questions: $n"; fail=1; }
[ "${stated:-x}" = "$n" ] || { echo "FAIL 'Open questions: N' says ${stated:-nothing}, found $n"; fail=1; }

# No source names or first-person voice in the text.
hits=$(grep -nv '^\[\^' "$card" | sed -E 's/`[^`]*`//g; s/[A-Za-z0-9]+([-_][A-Za-z0-9]+)+//g' \
  | grep -iwE 'lean canvas|ds_notes|dsdoc\.yaml|business context file|the team|we|I' | grep -v ':## Business context')
[ -z "$hits" ] || { echo "FAIL source names or voice:"; echo "$hits"; fail=1; }

# Sensitive data (shared check).
bash "$(dirname "$0")/../dsdoc/scripts/check_sensitive.sh" "$card" || fail=1

exit $fail
