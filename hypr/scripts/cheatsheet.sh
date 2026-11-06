#!/usr/bin/env bash
set -euo pipefail
# Resolve o link ~/.config/hypr para localizar o binário compilado neste repo.
script=$(realpath -- "${BASH_SOURCE[0]}")
root=$(dirname -- "$(dirname -- "$(dirname -- "$script")")")
binary="$root/hyprland-cheatsheets/target/release/hyprland-cheatsheets"
if [[ ! -x $binary ]]; then
    notify-send 'Atalhos do Hyprland' "Compile o aplicativo com: $root/build-cheatsheets.sh" || true
    exit 1
fi
exec "$binary" --section hyprland
