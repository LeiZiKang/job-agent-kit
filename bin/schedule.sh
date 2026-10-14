#!/bin/zsh
# Install/remove the macOS launchd job that runs bin/patrol.sh at the times in config.json
# ("patrol_times": ["10:30", "14:30", "19:00"], local time).
#   bin/schedule.sh install | uninstall | status
set -e
cd "$(dirname "$0")/.."
label="com.job-agent-kit.patrol"
plist="$HOME/Library/LaunchAgents/$label.plist"
case "$1" in
  install)
    times=$(python3 -c 'import json;print(" ".join(json.load(open("config.json")).get("patrol_times",[])))')
    [ -n "$times" ] || { echo "no patrol_times in config.json" >&2; exit 2; }
    entries=""
    for t in ${=times}; do
      entries+="<dict><key>Hour</key><integer>$((10#${t%%:*}))</integer><key>Minute</key><integer>$((10#${t##*:}))</integer></dict>"
    done
    mkdir -p reports/patrol "$HOME/Library/LaunchAgents"
    cat > "$plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>$label</string>
<key>ProgramArguments</key><array><string>/bin/zsh</string><string>$PWD/bin/patrol.sh</string></array>
<key>StartCalendarInterval</key><array>$entries</array>
<key>StandardOutPath</key><string>$PWD/reports/patrol/launchd.log</string>
<key>StandardErrorPath</key><string>$PWD/reports/patrol/launchd.log</string>
</dict></plist>
PLIST
    launchctl bootout "gui/$(id -u)/$label" 2>/dev/null || true
    launchctl bootstrap "gui/$(id -u)" "$plist"
    echo "installed $label at: $times" ;;
  uninstall)
    launchctl bootout "gui/$(id -u)/$label" 2>/dev/null || true
    rm -f "$plist"; echo "removed $label" ;;
  status)
    launchctl print "gui/$(id -u)/$label" 2>/dev/null | grep -E 'state|last exit' || echo "not installed" ;;
  *) echo "usage: bin/schedule.sh install|uninstall|status" >&2; exit 2 ;;
esac
