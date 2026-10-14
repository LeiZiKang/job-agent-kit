#!/bin/zsh
# Read-only inbox patrol. Runs every brief in briefs/patrol/*.md through Codex and appends each
# result's "## Changes" section to reports/patrol/<date>.md for the lead agent to review.
# Scheduled by bin/schedule.sh; safe to run by hand.
cd "$(dirname "$0")/.."
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
lock="${TMPDIR:-/tmp}/job-agent-kit-patrol.lock"
mkdir "$lock" 2>/dev/null || { echo "previous patrol still running"; exit 0; }
trap 'rmdir "$lock"' EXIT
mkdir -p reports/patrol
out="reports/patrol/$(date +%F).md"
[ -f "$out" ] || print -r -- "# $(date +%F) patrol (worker output, unverified; lead agent reviews before reporting)" > "$out"
print -r -- "\n## $(date +%H:%M) run" >> "$out"
for brief in briefs/patrol/*.md(N); do
  name=$(basename "$brief" .md); res="reports/patrol/$name-result.md"
  before=$(stat -f %m "$res" 2>/dev/null || echo 0)
  CODEX_EFFORT=${CODEX_EFFORT:-medium} caffeinate -dimsu bin/codex-run.sh "$brief" > /dev/null 2>&1
  print -r -- "\n### $name" >> "$out"
  if [ "$(stat -f %m "$res" 2>/dev/null || echo 0)" -gt "$before" ]; then
    awk '/^## Changes/{f=1;next} /^## /{f=0} f' "$res" >> "$out"
  else
    print -r -- "⚠️ result not updated (timeout, logged out, or screen locked); see reports/codex-logs/" >> "$out"
  fi
done
echo "done: $out"
