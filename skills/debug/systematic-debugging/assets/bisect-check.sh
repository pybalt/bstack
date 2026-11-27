#!/usr/bin/env bash
# Copy this script OUTSIDE the tracked repo (e.g., /tmp/bisect_check.sh) and chmod +x it.
# Usage:
#   git bisect start
#   git bisect bad HEAD
#   git bisect good <known-good-sha-or-tag>
#   git bisect run /tmp/bisect_check.sh
#   git bisect reset
set -u

# 1. Build / dependency sanity check.
# Exit 125 tells git bisect to SKIP commits that fail to build for unrelated reasons.
BUILD_CMD="${BUILD_CMD:-true}"
eval "$BUILD_CMD" >/dev/null 2>&1 || exit 125

# 2. Red-capable reproduction command:
#    exit 0 -> commit is GOOD (bug absent)
#    exit 1 -> commit is BAD  (bug present)
REPRO_CMD="${REPRO_CMD:?Set REPRO_CMD or replace this line with your exact repro command}"
eval "$REPRO_CMD"
rc=$?
if [ "$rc" -eq 0 ]; then
  exit 0
elif [ "$rc" -eq 125 ]; then
  exit 125
else
  exit 1
fi
