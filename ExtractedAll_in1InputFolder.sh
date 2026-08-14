#!/usr/bin/env bash
#
# ExtractedAll_in1InputFolder.sh - extract case features and fraud patterns from
# one folder of case PDFs, writing the results to a subfolder of ./extracted/
# with the same name as the input folder.
#
#   ./ExtractedAll_in1InputFolder.sh testdata_DOJ_2026
#       ./downloaded/testdata_DOJ_2026/   ->   ./extracted/testdata_DOJ_2026/
#
#   ./ExtractedAll_in1InputFolder.sh downloaded/2026/DOJ
#       ./downloaded/2026/DOJ/            ->   ./extracted/DOJ/
#
#   ./ExtractedAll_in1InputFolder.sh /abs/path/to/cases --effort high --limit 5
#       any extra arguments are passed straight through to extract_patterns.py
#
# Outputs, in ./extracted/<folder>/ :
#   cases.csv     one row per case
#   cases.json    the same rows plus the computed counts
#   patterns.md   counts + the pattern analysis
#   errors.json   only if a document failed
#   run.log       the console output of this run

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PYTHON="${PYTHON:-python3}"
EXTRACT_ROOT="./extracted"

usage() {
  # Print the header comment block, stopping at the first line of real code.
  awk 'NR<3 {next} /^#/ {sub(/^# ?/, ""); print; next} {exit}' "${BASH_SOURCE[0]}"
  exit "${1:-0}"
}

die() { printf 'error: %s\n' "$*" >&2; exit 1; }

# ---------------------------------------------------------------- arguments
[[ $# -ge 1 ]] || usage 1
case "$1" in
  -h|--help) usage 0 ;;
esac

RAW_INPUT="${1%/}"        # strip any trailing slash so basename is stable
shift                     # everything left over goes to extract_patterns.py

# Accept a full path, a path relative to the project, or a bare folder name
# under ./downloaded/ - so `... testdata_DOJ_2026` works as well as a full path.
INPUT_DIR=""
for candidate in "$RAW_INPUT" "./downloaded/$RAW_INPUT" "./$RAW_INPUT"; do
  if [[ -d "$candidate" ]]; then INPUT_DIR="${candidate%/}"; break; fi
done
[[ -n "$INPUT_DIR" ]] || die "input folder not found: '$RAW_INPUT' (tried it directly, and under ./downloaded/)"

FOLDER_NAME="$(basename -- "$INPUT_DIR")"
OUTPUT_DIR="$EXTRACT_ROOT/$FOLDER_NAME"

# ---------------------------------------------------------------- pre-flight
PDF_COUNT=$(find "$INPUT_DIR" -type f -name '*.pdf' | wc -l | tr -d ' ')
[[ "$PDF_COUNT" -gt 0 ]] || die "no PDF files found in $INPUT_DIR"

[[ -f extract_patterns.py ]] || die "extract_patterns.py not found in $SCRIPT_DIR"

command -v "$PYTHON" >/dev/null 2>&1 || die "'$PYTHON' not found (set PYTHON=/path/to/python3)"

if [[ -z "${ANTHROPIC_API_KEY:-}" && -z "${ANTHROPIC_AUTH_TOKEN:-}" ]]; then
  # An `ant auth login` profile also works, so this is a warning, not an error.
  printf 'warning: ANTHROPIC_API_KEY is not set - relying on an `ant auth login` profile\n' >&2
fi

mkdir -p "$OUTPUT_DIR"
LOG="$OUTPUT_DIR/run.log"

printf '=======================================================================\n'
printf ' input      : %s (%s PDF%s)\n' "$INPUT_DIR" "$PDF_COUNT" "$([[ "$PDF_COUNT" == 1 ]] || printf s)"
printf ' output     : %s\n' "$OUTPUT_DIR"
printf ' started    : %s\n' "$(date '+%Y-%m-%d %H:%M:%S')"
printf '=======================================================================\n'

# ---------------------------------------------------------------- run
set +e
"$PYTHON" -u extract_patterns.py \
    --input-dir "$INPUT_DIR" \
    --output-dir "$OUTPUT_DIR" \
    "$@" 2>&1 | tee "$LOG"
STATUS=${PIPESTATUS[0]}
set -e

printf '=======================================================================\n'
if [[ "$STATUS" -ne 0 ]]; then
  printf ' FAILED (exit %s) - see %s\n' "$STATUS" "$LOG"
  printf '=======================================================================\n'
  exit "$STATUS"
fi

if [[ -f "$OUTPUT_DIR/cases.csv" ]]; then
  # Parse as CSV rather than counting lines: SchemeSummary can contain newlines
  # inside a quoted field, which makes `wc -l` overcount.
  ROWS=$("$PYTHON" -c 'import csv,sys;print(sum(1 for _ in csv.DictReader(open(sys.argv[1]))))' \
         "$OUTPUT_DIR/cases.csv" 2>/dev/null || echo "?")
  printf ' extracted  : %s case row%s\n' "$ROWS" "$([[ "$ROWS" == 1 ]] || printf s)"
fi
[[ -f "$OUTPUT_DIR/errors.json" ]] && printf ' WARNING    : some documents failed - see %s\n' "$OUTPUT_DIR/errors.json"
printf ' finished   : %s\n' "$(date '+%Y-%m-%d %H:%M:%S')"
printf '=======================================================================\n'
for f in cases.csv cases.json patterns.md; do
  [[ -f "$OUTPUT_DIR/$f" ]] && printf ' -> %s\n' "$OUTPUT_DIR/$f"
done
exit 0
