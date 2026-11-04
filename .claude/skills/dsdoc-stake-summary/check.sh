#!/usr/bin/env bash
# Script check for stake_summary.md: banned terms, code terms from the card,
# numbers, section caps, length.
# Usage: check.sh <stake_summary.md> <model_card.md> [dsdoc.yaml]
# Prints one line per failed check; exits 1 if any check fails.

set -u
summary="$1"
card="$2"
yaml="${3:-dsdoc.yaml}"
max_words=400
fail=0

# Fixed list, case-insensitive: technical terms a manager would not use.
banned_ci='feature|features|column|columns|target|label|labels|preprocessing|imputation|encoding|normalization|train/test|training set|validation set|holdout|xgboost|lightgbm|random forest|neural|regression|clustering|hyperparameter|hyperparameters|tuning|epoch|epochs|embedding|embeddings|shap|overfitting|leakage|cold start|pipeline|inference|latency|schema|query|queries|baseline|baselines|ranker|ranking|top-k|cohort|cohorts|outlier|outliers|main metric'
# Acronyms, case-sensitive: the lowercase forms are ordinary words (map, als, api).
banned_cs='AUC|NDCG|MAP|RMSE|F1|ALS|API|SQL|NaN'

hits=$(grep -inwE "$banned_ci" "$summary"; grep -nwE "$banned_cs" "$summary")
if [ -n "$hits" ]; then
  echo "FAIL banned terms:"
  echo "$hits" | sort -t: -k1,1n -u
  fail=1
fi

# Code terms from the card: identifiers in backticks (with _ . = or parentheses).
# Brand codes and plain words in backticks are not code and stay allowed.
code_terms=$(grep -o '`[^`]*`' "$card" | tr -d '`' | grep -E '[_.=()]' | sort -u)
code_hits=""
while IFS= read -r term; do
  [ -z "$term" ] && continue
  if grep -qF -- "$term" "$summary"; then
    code_hits+="  $term"$'\n'
  fi
done <<< "$code_terms"
if [ -n "$code_hits" ]; then
  echo "FAIL code terms from the card:"
  printf '%s' "$code_hits"
  fail=1
fi

# Decimal numbers are copied, never computed or rounded: each must appear
# as written in dsdoc.yaml or in the card.
sources="$card"
[ -f "$yaml" ] && sources="$card $yaml"
num_hits=""
for n in $(grep -oE '[0-9]+\.[0-9]+' "$summary" | sort -u); do
  # shellcheck disable=SC2086
  if ! grep -qE "(^|[^0-9.])${n//./\\.}([^0-9]|$)" $sources; then
    num_hits+="  $n"$'\n'
  fi
done
if [ -n "$num_hits" ]; then
  echo "FAIL numbers not found in the card or dsdoc.yaml:"
  printf '%s' "$num_hits"
  fail=1
fi

# Items in a "## <heading>" section: lines starting with "- ", "* " or "1. ".
count_items() {
  awk -v h="## $1" '
    $0 == h { inside = 1; next }
    /^## / { inside = 0 }
    inside && /^[[:space:]]*([-*]|[0-9]+\.)[[:space:]]/ { n++ }
    END { print n + 0 }' "$summary"
}
n=$(count_items "How it works")
if [ "$n" -gt 3 ]; then
  echo "FAIL \"How it works\": $n bullets, max 3"
  fail=1
fi
n=$(count_items "Still to be confirmed")
if [ "$n" -gt 3 ]; then
  echo "FAIL \"Still to be confirmed\": $n items, max 3"
  fail=1
fi

if ! grep -q 'Not intended for' "$summary"; then
  echo "FAIL \"Not intended for\" line missing"
  fail=1
fi

words=$(wc -w < "$summary")
if [ "$words" -gt "$max_words" ]; then
  echo "FAIL length: $words words, max $max_words"
  fail=1
fi

# Sensitive data (shared check).
bash "$(dirname "$0")/../dsdoc/scripts/check_sensitive.sh" "$summary" || fail=1

[ "$fail" -eq 0 ] && echo "PASS"
exit "$fail"
