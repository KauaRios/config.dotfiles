#!/usr/bin/env bash
set -euo pipefail
[[ $EUID != 0 ]] || { echo 'Compile como usuário normal, sem sudo.' >&2; exit 1; }
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
cd "$root/hyprland-cheatsheets"
cargo build --locked --release
