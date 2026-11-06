-- Iniciar apenas depois que o compositor e seus sockets estiverem prontos.
hl.on("hyprland.start", function()
    hl.exec_cmd("gsettings set org.gnome.desktop.interface color-scheme prefer-dark")
    hl.exec_cmd("dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP HYPRLAND_INSTANCE_SIGNATURE QT_QPA_PLATFORMTHEME GTK_THEME; systemctl --user start hyprpolkitagent.service")
    hl.exec_cmd("waybar")
    -- O mako também pode ter sido iniciado por ativação D-Bus.
    hl.exec_cmd("pgrep -u \"$UID\" -x mako >/dev/null || mako")
    hl.exec_cmd("swaybg -i \"${XDG_CONFIG_HOME:-$HOME/.config}/wallpapers/cool-japanese-samurai-backiee-4K.jpg\" -m fill")
end)
