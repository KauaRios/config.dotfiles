local programs = require("lua.programs")

---------------------
---- KEYBINDINGS ----
---------------------

local mainMod = "SUPER"

-- Programas básicos
hl.bind(mainMod .. " + Q",           hl.dsp.exec_cmd(programs.terminal))
hl.bind(mainMod .. " + C",           hl.dsp.window.close())
hl.bind(mainMod .. " + M",           hl.dsp.exec_cmd("command -v hyprshutdown >/dev/null 2>&1 && hyprshutdown || hyprctl dispatch exit"))
hl.bind(mainMod .. " + E",           hl.dsp.exec_cmd(programs.fileManager))
hl.bind(mainMod .. " + V",           hl.dsp.window.float({ action = "toggle" }))
hl.bind(mainMod .. " + R",           hl.dsp.exec_cmd(programs.menu))
hl.bind(mainMod .. " + P",           hl.dsp.window.pseudo())
hl.bind(mainMod .. " + J",           hl.dsp.layout("togglesplit"))
hl.bind(mainMod .. " + B",           hl.dsp.exec_cmd(programs.firefox))
hl.bind(mainMod .. " + SHIFT+ Q",    hl.dsp.exec_cmd("[float; center; size 800 600] kitty"))

-- O ATALHO QUE CHAMA O cheat_sheet
hl.bind(mainMod .. " + H", hl.dsp.exec_cmd("[float; center; size 800 600] kitty -e lua \"${XDG_CONFIG_HOME:-$HOME/.config}/hypr/scripts/cheat_sheet.lua\""))


hl.bind(mainMod .. " + L",           hl.dsp.exec_cmd("pkill waybar; waybar"))
hl.bind(mainMod .. " + SHIFT + SPACE", hl.dsp.window.fullscreen(0))

-- Foco com setas
hl.bind(mainMod .. " + left",        hl.dsp.focus({ direction = "left" }))
hl.bind(mainMod .. " + right",       hl.dsp.focus({ direction = "right" }))
hl.bind(mainMod .. " + up",          hl.dsp.focus({ direction = "up" }))
hl.bind(mainMod .. " + down",        hl.dsp.focus({ direction = "down" }))

-- Workspaces 1–10
for i = 1, 10 do
    local key = i % 10  -- 10 vira tecla 0
    hl.bind(mainMod .. " + " .. key,         hl.dsp.focus({ workspace = i }))
    hl.bind(mainMod .. " + SHIFT + " .. key, hl.dsp.window.move({ workspace = i }))
end

-- Scratchpad
hl.bind(mainMod .. " + S",          hl.dsp.workspace.toggle_special("magic"))
hl.bind(mainMod .. " + SHIFT + S",  hl.dsp.window.move({ workspace = "special:magic" }))
hl.bind(mainMod .. " + ALT + S",    hl.dsp.window.move({ workspace = "e+0" }))

-- Mouse
hl.bind(mainMod .. " + mouse_down", hl.dsp.focus({ workspace = "e+1" }))
hl.bind(mainMod .. " + mouse_up",   hl.dsp.focus({ workspace = "e-1" }))
hl.bind(mainMod .. " + mouse:272",  hl.dsp.window.drag(),   { mouse = true })
hl.bind(mainMod .. " + mouse:273",  hl.dsp.window.resize(), { mouse = true })

-- Multimídia / teclas de laptop
hl.bind("XF86AudioRaiseVolume",  hl.dsp.exec_cmd("\"${XDG_CONFIG_HOME:-$HOME/.config}/hypr/scripts/volume.sh\" up"),       { locked = true, repeating = true })
hl.bind("XF86AudioLowerVolume",  hl.dsp.exec_cmd("\"${XDG_CONFIG_HOME:-$HOME/.config}/hypr/scripts/volume.sh\" down"),     { locked = true, repeating = true })
hl.bind("XF86AudioMute",         hl.dsp.exec_cmd("\"${XDG_CONFIG_HOME:-$HOME/.config}/hypr/scripts/volume.sh\" toggle"),   { locked = true, repeating = true })
hl.bind("XF86AudioMicMute",      hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle"), { locked = true, repeating = true })
hl.bind("XF86MonBrightnessUp",   hl.dsp.exec_cmd("brightnessctl -e4 -n2 set 5%+"),             { locked = true, repeating = true })
hl.bind("XF86MonBrightnessDown", hl.dsp.exec_cmd("brightnessctl -e4 -n2 set 5%-"),             { locked = true, repeating = true })

-- Playerctl
hl.bind("XF86AudioNext",  hl.dsp.exec_cmd("playerctl next"),        { locked = true })
hl.bind("XF86AudioPause", hl.dsp.exec_cmd("playerctl play-pause"),  { locked = true })
hl.bind("XF86AudioPlay",  hl.dsp.exec_cmd("playerctl play-pause"),  { locked = true })
hl.bind("XF86AudioPrev",  hl.dsp.exec_cmd("playerctl previous"),    { locked = true })
hl.bind("SUPER + I", hl.dsp.exec_cmd("bash \"${XDG_CONFIG_HOME:-$HOME/.config}/hypr/scripts/screenshot.sh\""))
hl.bind("SUPER + Escape", hl.dsp.exec_cmd("hyprlock"))
