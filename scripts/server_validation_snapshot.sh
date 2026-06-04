#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${OUT_DIR:-reports}"
STAMP="$(date +%Y%m%d-%H%M%S)"
HOST="$(hostname 2>/dev/null || echo demo-host)"
OUT="$OUT_DIR/server-validation-snapshot-$HOST-$STAMP.md"

mkdir -p "$OUT_DIR"

cmd_or_note() {
  local label="$1"
  shift
  echo "## $label" >> "$OUT"
  echo "" >> "$OUT"
  echo '```text' >> "$OUT"
  if command -v "$1" >/dev/null 2>&1; then
    "$@" 2>&1 | head -200 >> "$OUT" || true
  else
    echo "$1 not available on this system." >> "$OUT"
  fi
  echo '```' >> "$OUT"
  echo "" >> "$OUT"
}

cat > "$OUT" <<EOF
# Server Validation Snapshot

Generated: $(date -Is)
Host: $HOST

This is a safe read-only snapshot script for public portfolio demonstration.
It does not apply firmware updates, clear logs, reset management controllers or run destructive tests.
EOF

cmd_or_note "System Identity" hostnamectl
cmd_or_note "CPU Summary" lscpu
cmd_or_note "Memory Summary" free -h
cmd_or_note "Block Devices" lsblk -o NAME,TYPE,SIZE,MODEL,SERIAL,MOUNTPOINT
cmd_or_note "Filesystem Usage" df -h

echo "Generated $OUT"
