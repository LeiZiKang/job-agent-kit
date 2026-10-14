#!/bin/zsh
# Follow up with a finished Codex run (Codex exec sessions cannot be interrupted mid-run).
#   bin/codex-ask.sh --list              recent runs, session ids, running or done
#   bin/codex-ask.sh <run-name> "msg"    resume that session with a follow-up question
set -e
cd "$(dirname "$0")/.."
codex=$(command -v codex || echo /Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex)
logs=reports/codex-logs
running() { lsof -t "$1" >/dev/null 2>&1; }
sid_of() { grep -m1 '^session id:' "$1" | awk '{print $3}'; }
if [ "$1" = "--list" ]; then
  for f in $(ls -t $logs/*.log 2>/dev/null | head -${2:-12}); do
    printf '%-8s %-44s %s\n' "$(running "$f" && echo running || echo done)" "$(basename "$f" .log)" "$(sid_of "$f")"
  done
  exit 0
fi
name="$1"; msg="$2"
[ -n "$name" ] && [ -n "$msg" ] || { echo 'usage: bin/codex-ask.sh <run-name> "message" | --list' >&2; exit 2; }
[ "$msg" = "-" ] && msg=$(cat)
log=$(ls -t $logs/$name-[0-9]*.log 2>/dev/null | head -1)
[ -n "$log" ] || { echo "no $logs/$name-*.log" >&2; exit 2; }
sid=$(sid_of "$log"); [ -n "$sid" ] || { echo "no session id in $log" >&2; exit 2; }
running "$log" && { echo "still running; wait for it or stop it and re-brief" >&2; exit 3; }
out="$logs/$name-ask-$(date +%H%M%S).log"; last="$logs/$name-ask-last.md"
print -r -- "[Follow-up from lead agent] $msg" | perl -e 'alarm shift; exec @ARGV' 1500 \
  "$codex" exec resume "$sid" --dangerously-bypass-approvals-and-sandbox -o "$last" - > "$out" 2>&1 || true
cat "$last" 2>/dev/null || tail -20 "$out"
