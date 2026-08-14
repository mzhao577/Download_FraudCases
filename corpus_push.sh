#!/usr/bin/env bash
#
# corpus_push.sh - upload the downloaded corpus to a GitHub Release.
#
# The corpus is gitignored (4.7 GB of documents + 1.5 GB of cache), so a clone
# gets the code but no data. GitHub Releases are the right home for it: assets
# live outside git history, so the repo stays small and clonable.
#
#   ./corpus_push.sh                    # tag corpus-YYYY-MM-DD
#   ./corpus_push.sh --tag my-snapshot
#   ./corpus_push.sh --dry-run          # build the parts, upload nothing
#   ./corpus_push.sh --no-state         # ship ./downloaded only
#
# GitHub limits: 2 GiB per asset, up to 1000 assets, no total-size or bandwidth
# limit. The archive is therefore streamed through `split` into 1900 MB parts.
# On a private repo the assets are private too - `gh` authenticates the download.
#
# Pull them back on the other machine with ./corpus_pull.sh

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PART_SIZE="${PART_SIZE:-1900m}"          # under GitHub's 2 GiB per-asset cap
STAGE_DIR="${STAGE_DIR:-.corpus_upload}"
SOURCES=(downloaded state)
TAG=""
DRY_RUN=0

usage() { awk 'NR<3 {next} /^#/ {sub(/^# ?/, ""); print; next} {exit}' "${BASH_SOURCE[0]}"; exit "${1:-0}"; }
die()   { printf 'error: %s\n' "$*" >&2; exit 1; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)  usage 0 ;;
    --tag)      TAG="${2:?--tag needs a value}"; shift 2 ;;
    --dry-run)  DRY_RUN=1; shift ;;
    --no-state) SOURCES=(downloaded); shift ;;
    *)          die "unknown argument: $1  (try --help)" ;;
  esac
done

TAG="${TAG:-corpus-$(date +%Y-%m-%d)}"
PREFIX="corpus.tar.gz.part-"

# ---------------------------------------------------------------- pre-flight
command -v gh >/dev/null || die "gh not found - install the GitHub CLI"
gh auth status >/dev/null 2>&1 || die "gh is not authenticated - run: gh auth login"
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || die "not inside a git repository"
git remote get-url origin >/dev/null 2>&1 || die "no 'origin' remote - create the repo first"

PRESENT=()
for d in "${SOURCES[@]}"; do [[ -d "$d" ]] && PRESENT+=("$d"); done
[[ ${#PRESENT[@]} -gt 0 ]] || die "none of these folders exist: ${SOURCES[*]}"

RAW_KB=$(du -sk "${PRESENT[@]}" | awk '{s+=$1} END {print s}')
FREE_KB=$(df -k . | tail -1 | awk '{print $4}')
# `--json` is absent from older gh builds; fall back to the git remote.
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)
if [[ -z "$REPO" ]]; then
  REPO=$(git remote get-url origin 2>/dev/null | sed -e 's|\.git$||' -e 's|.*github\.com[:/]||')
fi
[[ -n "$REPO" ]] || die "cannot determine the GitHub repo from this directory"

printf '=======================================================================\n'
printf ' repo       : %s\n' "$REPO"
printf ' tag        : %s\n' "$TAG"
printf ' folders    : %s\n' "${PRESENT[*]}"
printf ' raw size   : %.1f GB\n' "$(echo "$RAW_KB/1048576" | bc -l)"
printf ' staging    : %s (parts of %s)\n' "$STAGE_DIR" "$PART_SIZE"
printf ' disk free  : %.1f GB\n' "$(echo "$FREE_KB/1048576" | bc -l)"
printf '=======================================================================\n'

# The compressed archive needs room alongside the originals. HTML compresses
# well and PDFs barely, so budget ~70% of raw and warn rather than fail.
NEED_KB=$(( RAW_KB * 7 / 10 ))
if [[ "$FREE_KB" -lt "$NEED_KB" ]]; then
  printf 'warning: only %.1f GB free, the parts may need about %.1f GB\n' \
    "$(echo "$FREE_KB/1048576" | bc -l)" "$(echo "$NEED_KB/1048576" | bc -l)" >&2
  printf '         set STAGE_DIR to a path on another volume if this fails\n' >&2
fi

# ---------------------------------------------------------------- build parts
rm -rf "$STAGE_DIR"; mkdir -p "$STAGE_DIR"

printf '\n[1/4] archiving and splitting (this is the slow part)...\n'
# Stream tar straight into split - never materialises a single 4 GB file.
tar -czf - "${PRESENT[@]}" | split -b "$PART_SIZE" - "$STAGE_DIR/$PREFIX"

cd "$STAGE_DIR"
PARTS=( "$PREFIX"* )
[[ ${#PARTS[@]} -gt 0 ]] || die "split produced no parts"

printf '[2/4] checksumming %s part(s)...\n' "${#PARTS[@]}"
shasum -a 256 "${PARTS[@]}" > SHA256SUMS

# A manifest so the other machine can tell what it is getting.
{
  printf 'corpus snapshot\n'
  printf 'created   : %s\n' "$(date '+%Y-%m-%d %H:%M:%S %Z')"
  printf 'source    : %s\n' "$REPO"
  printf 'commit    : %s\n' "$(git -C "$SCRIPT_DIR" rev-parse --short HEAD 2>/dev/null || echo unknown)"
  printf 'folders   : %s\n' "${PRESENT[*]}"
  printf 'parts     : %s x %s\n' "${#PARTS[@]}" "$PART_SIZE"
  printf 'files     : %s\n' "$(find "$SCRIPT_DIR/${PRESENT[0]}" -type f | wc -l | tr -d ' ')"
  printf '\nrestore with:  ./corpus_pull.sh --tag %s\n' "$TAG"
  printf 'or manually :  cat %s* | tar -xzf -\n' "$PREFIX"
} > MANIFEST.txt

printf '[3/4] parts built:\n'
ls -lh "${PARTS[@]}" | awk '{printf "        %6s  %s\n", $5, $9}'
cd "$SCRIPT_DIR"

if [[ "$DRY_RUN" -eq 1 ]]; then
  printf '\n[4/4] --dry-run: nothing uploaded. Parts are in %s/\n' "$STAGE_DIR"
  printf '      remove them with: rm -rf %s\n' "$STAGE_DIR"
  exit 0
fi

# ---------------------------------------------------------------- upload
printf '[4/4] uploading to release %s ...\n' "$TAG"
if gh release view "$TAG" >/dev/null 2>&1; then
  printf '      release exists - adding/overwriting assets\n'
  gh release upload "$TAG" "$STAGE_DIR"/* --clobber
else
  gh release create "$TAG" "$STAGE_DIR"/* \
    --title "Corpus snapshot $TAG" \
    --notes "Downloaded medical-fraud corpus (${PRESENT[*]}), split into ${#PARTS[@]} parts.

Restore on another machine:

    git clone https://github.com/$REPO.git
    cd \$(basename $REPO)
    ./corpus_pull.sh --tag $TAG

Verify with SHA256SUMS. See MANIFEST.txt for what this snapshot contains."
fi

printf '\n=======================================================================\n'
printf ' done: https://github.com/%s/releases/tag/%s\n' "$REPO" "$TAG"
printf ' staging kept at %s - delete with: rm -rf %s\n' "$STAGE_DIR" "$STAGE_DIR"
printf '=======================================================================\n'
