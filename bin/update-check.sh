#!/bin/sh
# Check whether a newer job-agent-kit release is on origin. Read-only: it fetches, never pulls.
#   bin/update-check.sh           at most once a week (prints nothing when up to date)
#   bin/update-check.sh --force   check now and always report
# Exit 0 = up to date or check skipped, 10 = update available.
cd "$(dirname "$0")/.." || exit 0
stamp=.git/job-agent-kit-update-check
[ -d .git ] || exit 0
if [ "$1" != "--force" ] && [ -f "$stamp" ] && [ -n "$(find "$stamp" -mtime -7 2>/dev/null)" ]; then exit 0; fi
branch=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||')
branch=${branch:-main}
if ! GIT_TERMINAL_PROMPT=0 git fetch --quiet origin "$branch" 2>/dev/null; then
  [ "$1" = "--force" ] && echo "update check: could not reach origin (offline?); skipped"
  exit 0
fi
touch "$stamp"
local_v=$(cat VERSION 2>/dev/null || echo 0.0.0)
remote_v=$(git show "origin/$branch:VERSION" 2>/dev/null || echo 0.0.0)
newer=$(printf '%s\n%s\n' "$local_v" "$remote_v" | sort -t. -k1,1n -k2,2n -k3,3n | tail -1)
if [ "$remote_v" = "$local_v" ] || [ "$newer" = "$local_v" ]; then
  [ "$1" = "--force" ] && echo "job-agent-kit $local_v is up to date"
  exit 0
fi
echo "job-agent-kit update available: $local_v -> $remote_v (run the update skill: say \"update the kit\")"
git show "origin/$branch:CHANGELOG.md" 2>/dev/null | awk -v v="$local_v" '/^## /{if (index($0, "## " v " ")==1) exit; on=1} on' | sed -n '1,40p'
changed=$(git status --porcelain --untracked-files=no)
[ -n "$changed" ] && printf 'Local edits to kit files (may conflict):\n%s\n' "$changed"
exit 10
