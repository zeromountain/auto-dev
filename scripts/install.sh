#!/usr/bin/env bash
# Manual fallback installer: symlinks skills/* into a target project's
# .claude/skills/ and .agents/skills/, so both Claude Code and Codex
# discover the same skill source. Prefer the plugin install flow in
# README.md (`plugin marketplace add` / `plugin add`) when available —
# this script is for hosts or setups where installing as a plugin isn't
# an option.
#
# Usage:
#   scripts/install.sh <target-repo-path> [--copy]
#
# --copy: copy files instead of symlinking (for filesystems/hosts without
#         symlink support, e.g. some Windows setups). Updates must then be
#         re-run manually to propagate.
set -euo pipefail

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../skills" && pwd -P)"
TARGET="${1:-}"
MODE="link"

if [[ -z "$TARGET" ]]; then
  echo "usage: $0 <target-repo-path> [--copy]" >&2
  exit 1
fi
if [[ "${2:-}" == "--copy" ]]; then
  MODE="copy"
fi
if [[ ! -d "$TARGET" ]]; then
  echo "error: target directory does not exist: $TARGET" >&2
  exit 1
fi

TARGET="$(cd "$TARGET" && pwd -P)"

install_skill() {
  local skill_name="$1"
  local src="$SOURCE_DIR/$skill_name"
  if [[ ! -d "$src" ]]; then
    echo "error: no such skill: $skill_name (looked in $src)" >&2
    exit 1
  fi

  for host_dir in ".claude/skills" ".agents/skills"; do
    local dest_parent="$TARGET/$host_dir"
    local dest="$dest_parent/$skill_name"
    mkdir -p "$dest_parent"

    if [[ -e "$dest" || -L "$dest" ]]; then
      echo "skip: $dest already exists"
      continue
    fi

    if [[ "$MODE" == "copy" ]]; then
      cp -R "$src" "$dest"
      echo "copied: $dest"
    else
      # relative symlink so the target repo stays portable if moved together
      # with its clone of this repo's parent directory structure
      local rel_src
      rel_src="$(python3 -c "import os,sys; print(os.path.relpath(sys.argv[1], sys.argv[2]))" "$src" "$dest_parent")"
      ln -s "$rel_src" "$dest"
      echo "linked: $dest -> $rel_src"
    fi
  done
}

for skill_dir in "$SOURCE_DIR"/*/; do
  skill_name="$(basename "$skill_dir")"
  [[ -f "$skill_dir/SKILL.md" ]] || continue
  install_skill "$skill_name"
done

echo "Done. Restart Claude Code / Codex in '$TARGET' to pick up new skill directories."
