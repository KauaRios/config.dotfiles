#!/usr/bin/env bash
set -eu
config=${XDG_CONFIG_HOME:-$HOME/.config}
# Preferência de apps GTK4/portais; persistente para este usuário.
gsettings set org.gnome.desktop.interface color-scheme prefer-dark || true
dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP HYPRLAND_INSTANCE_SIGNATURE QT_QPA_PLATFORMTHEME GTK_THEME || true
systemctl --user start hyprpolkitagent.service || true
state=${XDG_STATE_HOME:-$HOME/.local/state}/dotfiles
mkdir -p "$state"
for app in waybar mako swaybg; do
    python3 "$config/hypr/scripts/supervise.py" "$app" >>"$state/$app.log" 2>&1 &
done
wait
