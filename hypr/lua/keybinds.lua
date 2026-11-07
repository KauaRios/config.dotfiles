local programs = require("lua.programs")

---------------------
---- KEYBINDINGS ----
---------------------

local mainMod = "SUPER"

-- Programas básicos
hl.bind(mainMod .. " + Q",           hl.dsp.exec_cmd(programs.terminal), { description = "Abrir terminal" })
hl.bind(mainMod .. " + C",           hl.dsp.window.close(), { description = "Fechar janela" })
hl.bind(mainMod .. " + M",           hl.dsp.exec_cmd("command -v hyprshutdown >/dev/null 2>&1 && hyprshutdown || hyprctl dispatch 'hl.dsp.exit()'"), { description = "Sair do Hyprland" })
hl.bind(mainMod .. " + E",           hl.dsp.exec_cmd(programs.fileManager), { description = "Abrir Dolphin" })
hl.bind(mainMod .. " + V",           hl.dsp.window.float({ action = "toggle" }), { description = "Alternar janela flutuante" })
hl.bind(mainMod .. " + R",           hl.dsp.exec_cmd(programs.menu), { description = "Abrir menu de aplicativos" })
hl.bind(mainMod .. " + P",           hl.dsp.window.pseudo(), { description = "Alternar pseudotiling" })
hl.bind(mainMod .. " + J",           hl.dsp.layout("togglesplit"), { description = "Alternar divisão do layout" })
hl.bind(mainMod .. " + B",           hl.dsp.exec_cmd(programs.firefox), { description = "Abrir Firefox" })
hl.bind(mainMod .. " + SHIFT + Q",    hl.dsp.exec_cmd(programs.terminal, { float = true, center = true, size = {800, 600} }), { description = "Abrir terminal flutuante" })

hl.bind(mainMod .. " + H", hl.dsp.exec_cmd("kitty -e lua \"${XDG_CONFIG_HOME:-$HOME/.config}/hypr/scripts/cheat_sheet.lua\"", { float = true, center = true, size = {800, 600} }), { description = "Consultar atalhos" })


hl.bind(mainMod .. " + L",           hl.dsp.exec_cmd("pkill -u \"$USER\" -x waybar; waybar"), { description = "Reiniciar Waybar" })
hl.bind(mainMod .. " + W", hl.dsp.exec_cmd('python3 "${XDG_CONFIG_HOME:-$HOME/.config}/hypr/scripts/wallpaper.py"'), { description = "Escolher wallpaper e cores" })
hl.bind(mainMod .. " + SHIFT + SPACE", hl.dsp.window.fullscreen({ mode = "fullscreen", action = "toggle" }), { description = "Alternar tela cheia" })

hl.bind(mainMod .. " + SHIFT + R", hl.dsp.exec_cmd("wofi --show drun"), { description = "Abrir Wofi" })

-- Foco com setas
hl.bind(mainMod .. " + left",        hl.dsp.focus({ direction = "left" }), { description = "Focar à esquerda" })
hl.bind(mainMod .. " + right",       hl.dsp.focus({ direction = "right" }), { description = "Focar à direita" })
hl.bind(mainMod .. " + up",          hl.dsp.focus({ direction = "up" }), { description = "Focar acima" })
hl.bind(mainMod .. " + down",        hl.dsp.focus({ direction = "down" }), { description = "Focar abaixo" })

-- Workspaces 1–10
for i = 1, 10 do
    local key = i % 10  -- 10 vira tecla 0
    hl.bind(mainMod .. " + " .. key,         hl.dsp.focus({ workspace = i }), { description = "Ir para workspace " .. i })
    hl.bind(mainMod .. " + SHIFT + " .. key, hl.dsp.window.move({ workspace = i }), { description = "Mover janela para workspace " .. i })
end

-- Scratchpad
hl.bind(mainMod .. " + S",          hl.dsp.workspace.toggle_special("magic"), { description = "Alternar scratchpad" })
hl.bind(mainMod .. " + SHIFT + S",  hl.dsp.window.move({ workspace = "special:magic" }), { description = "Mover janela para scratchpad" })
hl.bind(mainMod .. " + ALT + S",    hl.dsp.window.move({ workspace = "e+0" }), { description = "Trazer janela ao workspace atual" })

-- Mouse
hl.bind(mainMod .. " + mouse_down", hl.dsp.focus({ workspace = "e+1" }), { description = "Próximo workspace" })
hl.bind(mainMod .. " + mouse_up",   hl.dsp.focus({ workspace = "e-1" }), { description = "Workspace anterior" })
hl.bind(mainMod .. " + mouse:272",  hl.dsp.window.drag(),   { mouse = true, description = "Arrastar janela" })
hl.bind(mainMod .. " + mouse:273",  hl.dsp.window.resize(), { mouse = true, description = "Redimensionar janela" })

-- Multimídia / teclas de laptop
hl.bind("XF86AudioRaiseVolume",  hl.dsp.exec_cmd("\"${XDG_CONFIG_HOME:-$HOME/.config}/hypr/scripts/volume.sh\" up"),       { locked = true, repeating = true, description = "Aumentar volume" })
hl.bind("XF86AudioLowerVolume",  hl.dsp.exec_cmd("\"${XDG_CONFIG_HOME:-$HOME/.config}/hypr/scripts/volume.sh\" down"),     { locked = true, repeating = true, description = "Diminuir volume" })
hl.bind("XF86AudioMute",         hl.dsp.exec_cmd("\"${XDG_CONFIG_HOME:-$HOME/.config}/hypr/scripts/volume.sh\" toggle"),   { locked = true, repeating = true, description = "Silenciar áudio" })
hl.bind("XF86AudioMicMute",      hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle"), { locked = true, repeating = true, description = "Silenciar microfone" })
hl.bind("XF86MonBrightnessUp",   hl.dsp.exec_cmd("brightnessctl -e4 -n2 set 5%+"),             { locked = true, repeating = true, description = "Aumentar brilho" })
hl.bind("XF86MonBrightnessDown", hl.dsp.exec_cmd("brightnessctl -e4 -n2 set 5%-"),             { locked = true, repeating = true, description = "Diminuir brilho" })

-- Playerctl
hl.bind("XF86AudioNext",  hl.dsp.exec_cmd("playerctl next"),        { locked = true, description = "Próxima faixa" })
hl.bind("XF86AudioPause", hl.dsp.exec_cmd("playerctl play-pause"),  { locked = true, description = "Pausar reprodução" })
hl.bind("XF86AudioPlay",  hl.dsp.exec_cmd("playerctl play-pause"),  { locked = true, description = "Reproduzir ou pausar" })
hl.bind("XF86AudioPrev",  hl.dsp.exec_cmd("playerctl previous"),    { locked = true, description = "Faixa anterior" })
hl.bind("SUPER + I", hl.dsp.exec_cmd("bash \"${XDG_CONFIG_HOME:-$HOME/.config}/hypr/scripts/screenshot.sh\""), { description = "Capturar região da tela" })
hl.bind("SUPER + Escape", hl.dsp.exec_cmd("hyprlock"), { description = "Bloquear sessão" })
