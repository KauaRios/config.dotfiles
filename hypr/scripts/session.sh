#!/usr/bin/env bash
set -eu
config=${XDG_CONFIG_HOME:-$HOME/.config}
for app in waybar mako; do
    pgrep -u "$UID" -x "$app" >/dev/null || "$app" &
done
swaybg -i "$config/wallpapers/cool-japanese-samurai-backiee-4K.jpg" -m fill &
wait
