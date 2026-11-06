-- Perfil original: notebook à esquerda, HDMI principal à direita.
-- Consulte os nomes/modos disponíveis com: hyprctl monitors all
hl.monitor({
    output = "eDP-1",
    mode = "1920x1080@144",
    position = "0x0",
    scale = 1,
})
hl.monitor({
    output = "HDMI-A-1",
    mode = "1920x1080@144",
    position = "1921x0", -- preserva o ajuste de 1px da configuração original
    scale = 1,
})
-- Outros monitores continuam com detecção automática.
hl.monitor({ output = "", mode = "preferred", position = "auto", scale = 1 })
hl.config({ cursor = { default_monitor = "HDMI-A-1" } })
