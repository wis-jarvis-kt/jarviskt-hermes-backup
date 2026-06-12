#!/bin/bash
# Disk Space Watchdog + Auto-Cleanup for Mac mini
# Runs every 24h. Cleans up when free space drops below threshold.

THRESHOLD_GB=50
DAYSOLD=7

if [ "$(uname)" = "Darwin" ]; then
  AVAILABLE_GB=$(df -g / | tail -1 | awk '{print $4}')
else
  AVAILABLE_GB=$(df -BG / | tail -1 | awk '{print $4}' | tr -d 'G')
fi

echo "Disk check: ${AVAILABLE_GB}GB free"

if [ "$AVAILABLE_GB" -lt "$THRESHOLD_GB" ]; then
  echo "⚠️ Low disk space — running cleanup..."

  # 1. Old cron output
  CRON_OUTPUT="$HOME/.hermes/cron/output"
  if [ -d "$CRON_OUTPUT" ]; then
    DELETED_CRON=$(find "$CRON_OUTPUT" -type d -mtime +${DAYSOLD} -exec rm -rf {} +2>/dev/null | wc -l | tr -d ' ')
    echo " Cleanup: $DELETED_CRON old cron output dirs"
  fi

  # 2. Old session files
  SESSIONS="$HOME/.hermes/sessions"
  if [ -d "$SESSIONS" ]; then
    DELETED_SESSIONS=$(find "$SESSIONS" -name "session_*" -mtime +${DAYSOLD} -delete 2>/dev/null | wc -l | tr -d ' ')
    echo "  Cleanup: $DELETED_SESSIONS old session files"
  fi

  # 3. Old memory logs
  MEMORIES="$HOME/.hermes/memories"
  if [ -d "$MEMORIES" ]; then
    DELETED_MEM=$(find "$MEMORIES" \( -name "research-*" -o -name "war-news-*" -o -name "stock-radar-*" -o -name "victor-study-*" \) -type f -mtime +${DAYSOLD} -delete 2>/dev/null | wc -l | tr -d ' ')
    echo "  Cleanup: $DELETED_MEM old daily memory logs"
  fi

  # 4. Hermes agent logs
  LOGS="$HOME/.hermes/logs"
  if [ -d "$LOGS" ]; then
    find "$LOGS" -name "*.log" -mtime +${DAYSOLD} -type f -delete 2>/dev/null
    echo "  Cleanup: old log files"
  fi

  # 5. macOS sleepimage (can be regenerated on wake)
  SLEEPIMAGE="/private/var/vm/sleepimage"
  if [ -f "$SLEEPIMAGE" ]; then
    SIZE=$(du -k "$SLEEPIMAGE" 2>/dev/null | cut -f1)
    if [ "$SIZE" -gt 1024 ]; then  # only if > 1GB
      rm -f "$SLEEPIMAGE" 2>/dev/null
      echo "  Cleanup: removed sleepimage ($(($SIZE/1024))GB)"
    fi
  fi

  # Report new space
  if [ "$(uname)" = "Darwin" ]; then
    NEW_AVAILABLE_GB=$(df -g / | tail -1 | awk '{print $4}')
  else
    NEW_AVAILABLE_GB=$(df -BG / | tail -1 | awk '{print $4}' | tr -d 'G')
  fi
  echo ""
  echo "✅ Cleanup done. Free space: ${NEW_AVAILABLE_GB}GB"
else
  echo "✅ Disk space fine (${AVAILABLE_GB}GB free, threshold ${THRESHOLD_GB}GB)"
fi
