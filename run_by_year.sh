#!/bin/bash
# Download the corpus one year at a time, newest first, summarising after each.
# Resumable: rerunning skips whatever is already on disk.
set -u
cd "$(dirname "$0")"
YEARS="${*:-2026 2025 2024 2023 2022 2021}"

for y in $YEARS; do
  echo "=== $(date '+%H:%M:%S')  YEAR $y ==============================="
  python3 -u download.py --years "$y" --workers 5 >> "logs/download_$y.log" 2>&1
  python3 summarize.py
  echo "=== $(date '+%H:%M:%S')  YEAR $y done ==========================="
done
