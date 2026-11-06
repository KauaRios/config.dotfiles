hl.on("hyprland.start", function()
    hl.exec_cmd("bash \"${XDG_CONFIG_HOME:-$HOME/.config}/hypr/scripts/session.sh\"")
end)
