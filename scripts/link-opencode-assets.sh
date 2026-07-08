#!/usr/bin/env bash
set -euo pipefail

# Link this repo's skills and command files into the local user-level locations.
#
# Usage:
#   scripts/link-opencode-assets.sh          # create/update safe symlinks
#   scripts/link-opencode-assets.sh --force  # replace existing non-matching paths
#   scripts/link-opencode-assets.sh --dry-run

force=0
dry_run=0

for arg in "$@"; do
  case "$arg" in
    --force) force=1 ;;
    --dry-run) dry_run=1 ;;
    -h|--help)
      sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "Unknown argument: $arg" >&2
      exit 2
      ;;
  esac
done

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd -- "$script_dir/.." && pwd)"

skill_dest="${HOME}/.agents/skills"
command_dest="${HOME}/.config/opencode/commands"

run() {
  if (( dry_run )); then
    printf 'DRY-RUN: '
    printf '%q ' "$@"
    printf '\n'
  else
    "$@"
  fi
}

link_path() {
  local source="$1"
  local dest_dir="$2"
  local name="$3"
  local dest="${dest_dir}/${name}"

  if [[ -L "$dest" ]]; then
    local current
    local current_abs
    current="$(readlink -- "$dest")"
    if [[ "$current" = /* ]]; then
      current_abs="$current"
    else
      current_abs="$(realpath -m -- "$(dirname -- "$dest")/$current")"
    fi

    if [[ "$current_abs" == "$source" ]]; then
      echo "ok: ${dest} -> ${source}"
      return 0
    fi

    if (( ! force )); then
      echo "conflict: ${dest} already links to ${current}; use --force to replace" >&2
      return 1
    fi

    run rm -f -- "$dest"
  elif [[ -e "$dest" ]]; then
    if (( ! force )); then
      echo "conflict: ${dest} already exists; use --force to replace" >&2
      return 1
    fi

    run rm -rf -- "$dest"
  fi

  run mkdir -p -- "$dest_dir"
  run ln -s -- "$source" "$dest"
  if (( dry_run )); then
    echo "would link: ${dest} -> ${source}"
  else
    echo "linked: ${dest} -> ${source}"
  fi
}

mapfile -d '' skill_dirs < <(
  find "$repo_root/skills" \
    -path "$repo_root/skills/.to-sort" -prune -o \
    -type f -name SKILL.md -print0 \
    | sort -z
)

status=0

for skill_file in "${skill_dirs[@]}"; do
  skill_dir="$(dirname -- "$skill_file")"
  skill_name="$(basename -- "$skill_dir")"
  link_path "$skill_dir" "$skill_dest" "$skill_name" || status=1
done

for command_dir in "$repo_root/commands" "$repo_root/.opencode/commands"; do
  [[ -d "$command_dir" ]] || continue

  while IFS= read -r -d '' command_file; do
    link_path "$command_file" "$command_dest" "$(basename -- "$command_file")" || status=1
  done < <(find "$command_dir" -maxdepth 1 -type f -name '*.md' -print0 | sort -z)
done

exit "$status"
