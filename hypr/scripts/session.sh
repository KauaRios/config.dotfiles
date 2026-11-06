#!/usr/bin/env bash
set -eu
config=${XDG_CONFIG_HOME:-$HOME/.config}
# Preferência de apps GTK4/portais; persistente para este usuário.
gsettings set org.gnome.desktop.interface color-scheme prefer-dark || true
dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP HYPRLAND_INSTANCE_SIGNATURE || true
systemctl --user start hyprpolkitagent.service || true
for app in waybar mako; do
    pgrep -u "$UID" -x "$app" >/dev/null || "$app" &
done
swaybg -i "$config/wallpapers/cool-japanese-samurai-backiee-4K.jpg" -m fill &
wait
