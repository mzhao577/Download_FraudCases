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
#   ./corpus_pull.sh --repo OWNER/NAME  # when not run from inside the clone
#
# gh works out which repository to use from the git remote of the current
# directory. Run this from inside the cloned repo, or pass --repo.
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
# gh works out which repo to talk to from the git remote of the current
# directory. Run this script outside a clone and every gh call fails, so allow
# an explicit override via --repo or the REPO environment variable.
REPO="${REPO:-}"

usage() { awk 'NR<3 {next} /^#/ {sub(/^# ?/, ""); print; next} {exit}' "${BASH_SOURCE[0]}"; exit "${1:-0}"; }
die()   { printf 'error: %s\n' "$*" >&2; exit 1; }

# `gh release list --json` and `gh repo view --json` are not in older gh builds
# (they fail with "unknown flag: --json"). Everything below therefore tries the
# JSON form first and falls back to output every gh version can produce, so the
# script does not require a particular gh version on the receiving machine.

repo_from_git_remote() {
  local url
  url=$(git remote get-url origin 2>/dev/null) || return 1
  url="${url%.git}"
  case "$url" in
    *github.com[:/]*) printf '%s\n' "${url#*github.com}" | sed 's|^[:/]||' ;;
    *) return 1 ;;
  esac
}

resolve_repo() {
  gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null && return 0
  repo_from_git_remote
}

# Every release tag, newest first, on any gh version.
list_tags() {
  gh release list "${GH_REPO_ARGS[@]}" --limit 50 --json tagName -q '.[].tagName' 2>/dev/null && return 0
  # Plain output is columns separated by tabs; the column order has shifted
  # between gh versions, so scan every field rather than assuming a position.
  gh release list "${GH_REPO_ARGS[@]}" --limit 50 2>/dev/null \
    | awk -F'\t' '{for (i = 1; i <= NF; i++) if ($i ~ /^[A-Za-z0-9._-]+$/ && $i != "") print $i}'
}

LIST_ONLY=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage 0 ;;
    --tag)     TAG="${2:?--tag needs a value}"; shift 2 ;;
    --repo)    REPO="${2:?--repo needs OWNER/NAME}"; shift 2 ;;
    --keep)    KEEP=1; shift ;;
    --list)    LIST_ONLY=1; shift ;;
    *)         die "unknown argument: $1  (try --help)" ;;
  esac
done

command -v gh >/dev/null || die "gh not found - install the GitHub CLI"
gh auth status >/dev/null 2>&1 || die "gh is not authenticated - run: gh auth login"

# ---------------------------------------------------------------- which repo
if [[ -z "$REPO" ]]; then
  REPO=$(resolve_repo 2>/dev/null || true)
fi
if [[ -z "$REPO" ]]; then
  printf 'error: cannot tell which GitHub repository to use.\n\n' >&2
  printf '  gh infers the repo from the git remote of the current directory, and\n' >&2
  printf '  this directory is not a clone with a GitHub remote:\n    %s\n\n' "$SCRIPT_DIR" >&2
  printf '  Fix it in one of these ways:\n' >&2
  printf '    1. Run the script from inside the cloned repo:\n' >&2
  printf '         gh repo clone OWNER/NAME && cd NAME && ./corpus_pull.sh\n' >&2
  printf '    2. Name the repo explicitly:\n' >&2
  printf '         ./corpus_pull.sh --repo OWNER/NAME\n' >&2
  printf '    3. Set it in the environment:\n' >&2
  printf '         REPO=OWNER/NAME ./corpus_pull.sh\n' >&2
  exit 1
fi
GH_REPO_ARGS=(--repo "$REPO")

if [[ "$LIST_ONLY" -eq 1 ]]; then
  printf 'releases in %s:\n' "$REPO"
  gh release list "${GH_REPO_ARGS[@]}" --limit 30
  exit 0
fi

# ---------------------------------------------------------------- which tag
if [[ -z "$TAG" ]]; then
  TAGS=$(list_tags || true)
  if [[ -z "$TAGS" ]]; then
    # Nothing came back from either form - show gh's own error rather than
    # guessing, since auth, network and permissions all land here too.
    printf 'gh could not list releases in %s:\n' "$REPO" >&2
    gh release list "${GH_REPO_ARGS[@]}" --limit 5 2>&1 | sed 's/^/  /' >&2
    exit 1
  fi
  TAG=$(printf '%s\n' "$TAGS" | grep -m1 '^corpus-' || true)
  if [[ -z "$TAG" || "$TAG" == "null" ]]; then
    printf 'error: %s has no release tagged corpus-*\n\n' "$REPO" >&2
    printf '  Releases that do exist:\n' >&2
    gh release list "${GH_REPO_ARGS[@]}" --limit 10 2>&1 | sed 's/^/    /' >&2
    printf '\n  Create one from the machine holding the data:  ./corpus_push.sh\n' >&2
    exit 1
  fi
  printf 'using most recent snapshot: %s\n' "$TAG"
fi

gh release view "$TAG" "${GH_REPO_ARGS[@]}" >/dev/null 2>&1 \
  || die "release '$TAG' not found in $REPO (list them with --list)"

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
printf ' repo    : %s\n' "$REPO"
printf ' release : %s\n' "$TAG"
printf ' target  : %s\n' "$SCRIPT_DIR"
printf '=======================================================================\n'

printf '\n[1/4] downloading assets...\n'
rm -rf "$STAGE_DIR"; mkdir -p "$STAGE_DIR"
gh release download "$TAG" "${GH_REPO_ARGS[@]}" --dir "$STAGE_DIR"

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
