#!/usr/bin/env bash
# Script check for stake_summary.md: banned terms, code terms from the card, length.
# Usage: check.sh <stake_summary.md> <model_card.md>
# Prints one line per failed check; exits 1 if any check fails.

set -u
summary="$1"
card="$2"
max_words=400
fail=0

# Fixed list, case-insensitive: technical terms a manager would not use.
banned_ci='feature|features|column|columns|target|label|labels|preprocessing|imputation|encoding|normalization|train/test|training set|validation set|holdout|xgboost|lightgbm|random forest|neural|regression|clustering|hyperparameter|hyperparameters|tuning|epoch|epochs|embedding|embeddings|shap|overfitting|leakage|cold start|pipeline|inference|latency|schema|query|queries|baseline|baselines|ranker|ranking|top-k|cohort|cohorts|outlier|outliers'
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

words=$(wc -w < "$summary")
if [ "$words" -gt "$max_words" ]; then
  echo "FAIL length: $words words, max $max_words"
  fail=1
fi

[ "$fail" -eq 0 ] && echo "PASS"
exit "$fail"
