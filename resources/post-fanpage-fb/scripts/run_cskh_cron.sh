#!/usr/bin/env bash
set -uo pipefail

PROJECT_ROOT="/root/.agents/skills/tao-tro-ly-openclaw-windows-macos-linux/resources/post-fanpage-fb"
SCRIPT_PATH="$PROJECT_ROOT/scripts/Facebook_Message_CSKH.py"
LOG_DIR="$PROJECT_ROOT/logs"
LOG_FILE="$LOG_DIR/cskh_cron.log"
PYTHON_BIN="$PROJECT_ROOT/venv/bin/python"

mkdir -p "$LOG_DIR"
export TZ="Asia/Ho_Chi_Minh"

{
  echo "============================================================"
  echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] Start CSKH auto message"
  cd "$PROJECT_ROOT" || exit 1
  
  if [ -f "$PYTHON_BIN" ]; then
    "$PYTHON_BIN" "$SCRIPT_PATH"
  else
    /usr/bin/python3 "$SCRIPT_PATH"
  fi
  
  status=$?
  echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] Finished with exit code $status"
  exit "$status"
} >> "$LOG_FILE" 2>&1
