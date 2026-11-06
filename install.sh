#!/usr/bin/env bash
set -euo pipefail
[[ $EUID != 0 ]] || { echo 'Execute como usuário normal, sem sudo.' >&2; exit 1; }
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
config=${XDG_CONFIG_HOME:-$HOME/.config}
[[ $config = /* ]] || { echo 'XDG_CONFIG_HOME precisa ser absoluto.' >&2; exit 1; }
mode=${1:-}
[[ -z $mode || $mode = --dry-run ]] || { echo 'Uso: ./install.sh [--dry-run]'; exit 1; }
folders=(hypr waybar rofi wofi mako wallpapers qt6ct)
for name in "${folders[@]}"; do [[ -d $root/$name ]] || exit 1; done
backup=
for name in "${folders[@]}"; do
    src=$root/$name; dst=$config/$name
    if [[ -L $dst && $(readlink -f -- "$dst") = "$src" ]]; then
        echo "Já instalado: $name"; continue
    fi
    if [[ $mode = --dry-run ]]; then echo "Link: $dst -> $src (backup se existir)"; continue; fi
    mkdir -p -- "$config"
    if [[ -e $dst || -L $dst ]]; then
        if [[ -z $backup ]]; then backup=$(mktemp -d "$config/dot-backup.XXXXXXXX"); fi
        mv -- "$dst" "$backup/$name"
        echo "Backup: $backup/$name"
    fi
    ln -s -- "$src" "$dst"
    echo "Instalado: $name"
done
