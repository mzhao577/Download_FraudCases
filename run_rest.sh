#!/bin/bash
set -u
cd "$(dirname "$0")"
echo "=== $(date '+%H:%M:%S') FBI discovery ==="
python3 -u discover.py --sources FBI --append > logs/discover_fbi.log 2>&1
echo "=== $(date '+%H:%M:%S') FBI discovery done ==="
./run_by_year.sh 2026 2025 2024 2023 2022 2021
echo "=== $(date '+%H:%M:%S') ALL YEARS DONE ==="
