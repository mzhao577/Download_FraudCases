#!/usr/bin/env bash
#
# corpus_pull.sh - restore the downloaded corpus from a GitHub Release.
#
# Run this on the second machine after cloning the repo. It downloads the split
# archive, verifies every part against SHA256SUMS, and unpacks ./downloaded and
# ./state in place.
#
#   ./corpus_pull.sh                    # newest corpus-* release
#   ./corpus_pull.sh --tag corpus-2026-08-13
#   ./corpus_pull.sh --list             # show available snapshots
#   ./corpus_pull.sh --keep             # keep the downloaded parts afterwards
#
# The repo is private, so `gh` supplies the credentials - plain curl or a
# browser download will not work without a token.

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

STAGE_DIR="${STAGE_DIR:-.corpus_download}"
PREFIX="corpus.tar.gz.part-"
TAG=""
KEEP=0

usage() { awk 'NR<3 {next} /^#/ {sub(/^# ?/, ""); print; next} {exit}' "${BASH_SOURCE[0]}"; exit "${1:-0}"; }
die()   { printf 'error: %s\n' "$*" >&2; exit 1; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage 0 ;;
    --tag)     TAG="${2:?--tag needs a value}"; shift 2 ;;
    --keep)    KEEP=1; shift ;;
    --list)    gh release list --limit 30; exit 0 ;;
    *)         die "unknown argument: $1  (try --help)" ;;
  esac
done

command -v gh >/dev/null || die "gh not found - install the GitHub CLI"
gh auth status >/dev/null 2>&1 || die "gh is not authenticated - run: gh auth login"

# Default to the most recent corpus-* tag.
if [[ -z "$TAG" ]]; then
  TAG=$(gh release list --limit 50 --json tagName -q '[.[].tagName | select(startswith("corpus-"))] | .[0]' 2>/dev/null || true)
  [[ -n "$TAG" && "$TAG" != "null" ]] || die "no corpus-* release found - list them with --list"
  printf 'using most recent snapshot: %s\n' "$TAG"
fi

gh release view "$TAG" >/dev/null 2>&1 || die "release '$TAG' not found (try --list)"

# Refuse to clobber an existing corpus without the user saying so.
for d in downloaded state; do
  if [[ -d "$d" ]] && [[ -n "$(ls -A "$d" 2>/dev/null)" ]]; then
    printf 'warning: ./%s already exists and is not empty.\n' "$d" >&2
    printf '         Unpacking merges into it; existing files of the same name are overwritten.\n' >&2
    read -r -p '         Continue? [y/N] ' reply
    [[ "$reply" =~ ^[Yy]$ ]] || die "aborted"
    break
  fi
done

printf '=======================================================================\n'
printf ' release : %s\n' "$TAG"
printf ' target  : %s\n' "$SCRIPT_DIR"
printf '=======================================================================\n'

printf '\n[1/4] downloading assets...\n'
rm -rf "$STAGE_DIR"; mkdir -p "$STAGE_DIR"
gh release download "$TAG" --dir "$STAGE_DIR"

cd "$STAGE_DIR"
[[ -f SHA256SUMS ]] || die "SHA256SUMS missing from the release - cannot verify"
PARTS=( "$PREFIX"* )
[[ -e "${PARTS[0]}" ]] || die "no $PREFIX* assets in release $TAG"

printf '[2/4] verifying %s part(s)...\n' "${#PARTS[@]}"
if ! shasum -a 256 -c SHA256SUMS; then
  die "checksum mismatch - a part is corrupt or truncated. Delete $STAGE_DIR and retry."
fi

printf '[3/4] unpacking...\n'
cd "$SCRIPT_DIR"
cat "$STAGE_DIR/$PREFIX"* | tar -xzf -

printf '[4/4] result:\n'
for d in downloaded state; do
  [[ -d "$d" ]] && printf '        %-12s %6s  %s files\n' "$d" \
      "$(du -sh "$d" | cut -f1)" "$(find "$d" -type f | wc -l | tr -d ' ')"
done

if [[ "$KEEP" -eq 0 ]]; then
  rm -rf "$STAGE_DIR"
else
  printf '        parts kept in %s\n' "$STAGE_DIR"
fi

printf '\n=======================================================================\n'
printf ' restored. Check it with:  python verify.py\n'
[[ -f "$STAGE_DIR/MANIFEST.txt" ]] && cat "$STAGE_DIR/MANIFEST.txt"
printf '=======================================================================\n'
