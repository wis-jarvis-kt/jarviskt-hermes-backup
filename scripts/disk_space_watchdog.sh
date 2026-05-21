#!/bin/bash
# Disk Space Watchdog for Mac mini
# Alerts when free space drops below 50GB

THRESHOLD_GB=50

if [ "$(uname)" = "Darwin" ]; then
  AVAILABLE_GB=$(df -g / | tail -1 | awk '{print $7}')
else
  AVAILABLE_GB=$(df -BG / | tail -1 | awk '{print $4}' | tr -d 'G')
fi

if [ "$AVAILABLE_GB" -lt "$THRESHOLD_GB" ]; then
  USED=$(df / | tail -1 | awk '{print $3}')
  TOTAL=$(df / | tail -1 | awk '{print $2}')
  echo "⚠️ LOW DISK SPACE WARNING"
  echo ""
  echo "Available: ${AVAILABLE_GB}GB (below ${THRESHOLD_GB}GB threshold)"
  echo "Used: ${USED} | Total: ${TOTAL}"
  echo ""
  echo "Mac mini is running low on disk space. Consider cleanup."
else
  # Silent - no output means no message
  :
fi