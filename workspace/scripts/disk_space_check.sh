#!/usr/bin/env bash
# Disk space monitor — alerts if free space drops below 60GB on data volume
set -euo pipefail

STATE_FILE="/Users/ktoclaw/.openclaw/workspace/memory/disk-monitor-state.json"
THRESHOLD_GB=60
CURRENT_GB=$(df -g /System/Volumes/Data 2>/dev/null | awk 'NR==2 {print $4}')

if [ -f "$STATE_FILE" ]; then
  LAST_ALERT=$(jq -r '.last_alert_gb // 999' "$STATE_FILE")
else
  LAST_ALERT=999
fi

ALERTED=0
if [ "$CURRENT_GB" -lt "$THRESHOLD_GB" ] && [ "$LAST_ALERT" -ge "$THRESHOLD_GB" ]; then
  echo "⚠️ DISK SPACE ALERT: ${CURRENT_GB}GB free on data volume (threshold: ${THRESHOLD_GB}GB)"
  ALERTED=1
elif [ "$CURRENT_GB" -ge "$THRESHOLD_GB" ] && [ "$LAST_ALERT" -lt "$THRESHOLD_GB" ]; then
  echo "✅ Disk space recovered: ${CURRENT_GB}GB free"
fi

CURRENT_GB=$CURRENT_GB jq -n \
  --argjson current "$CURRENT_GB" \
  --argjson threshold "$THRESHOLD_GB" \
  --argjson alerted "$ALERTED" \
  --argjson now "$(date +%s)" \
  '{current_gb: $current, threshold_gb: $threshold, alerted: $alerted, last_check: $now, last_alert_gb: $current}' \
  > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
