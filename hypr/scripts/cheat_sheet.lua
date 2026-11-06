local ciano   = "\27[36m"
local verde   = "\27[32m"
local roxo    = "\27[35m"
local amarelo = "\27[33m"
local branco  = "\27[37m"
local negrito = "\27[1m"
local reset   = "\27[0m" 

-- Base de dados completa com todos os meus comandos do keybinds.lua
local atalhos = {
    -- Sistema e Janelas
    { tecla = "SUPER + Q",             acao = "Abrir Terminal" },
    { tecla = "SUPER + C",             acao = "Fechar Janela Focada" },
    { tecla = "SUPER + M",             acao = "Sair do Hyprland" },
    { tecla = "SUPER + V",             acao = "Janela Flutuante (Toggle)" },
    { tecla = "SUPER + P",             acao = "Layout Pseudo-Tiling" },
    { tecla = "SUPER + J",             acao = "Alternar Divisão (Split)" },
    { tecla = "SUPER + SHIFT + SPACE", acao = "Tela Cheia (Fullscreen)" },
    { tecla=  "SUPER + SHIFT + Q",        acao="Abrir Terminal Em Float"},
    
    -- Aplicativos e Menus
    { tecla = "SUPER + E",             acao = "Gerenciador de Arquivos" },
    { tecla = "SUPER + R",             acao = "Menu de Aplicativos (Rofi)" },
    { tecla = "SUPER + B",             acao = "Navegador Zen" },
    { tecla = "SUPER + H",             acao = "Menu de Ajuda (Esta tela)" },
    { tecla = "SUPER + T",             acao = "Script Sweeper Rofi" },
    { tecla = "SUPER + W",             acao = "Listar Janelas Abertas" },
    
    -- Sistema e Ferramentas
    { tecla = "SUPER + L",             acao = "Reiniciar Waybar" },
    { tecla = "SUPER + I",             acao = "Captura de Tela (Clipboard)" },
    { tecla = "SUPER + SHIFT + P",     acao = "Reiniciar Hyprpaper" },

    -- Foco e Navegação
    { tecla = "SUPER + Setas",         acao = "Mudar Foco (Esq/Dir/Cima/Baixo)" },
    { tecla = "SUPER + 1..0",          acao = "Ir para Workspace 1 ao 10" },
    { tecla = "SUPER + SHIFT + 1..0",  acao = "Mover Janela p/ Workspace 1 ao 10" },

    -- Scratchpad
    { tecla = "SUPER + S",             acao = "Abrir/Fechar Scratchpad" },
    { tecla = "SUPER + SHIFT + S",     acao = "Mover Janela p/ Scratchpad" },
    { tecla = "SUPER + ALT + S",       acao = "Trazer Janela do Scratchpad" },

    -- Mouse e Controles Flutuantes
    { tecla = "SUPER + Mouse Esq.",    acao = "Mover Janela (Arrastar)" },
    { tecla = "SUPER + Mouse Dir.",    acao = "Redimensionar Janela" },
    { tecla = "SUPER + Scroll",        acao = "Alternar Workspaces (Prox/Ant)" },

    -- Multimídia e Hardware
    { tecla = "Fn + Vol Up/Down",      acao = "Aumentar/Diminuir Volume" },
    { tecla = "Fn + Mute",             acao = "Mutar Áudio" },
    { tecla = "Fn + Mic Mute",         acao = "Mutar Microfone" },
    { tecla = "Fn + Brilho Up/Down",   acao = "Aumentar/Diminuir Brilho" },
    { tecla = "Fn + Mídia",            acao = "Tocar/Pausar/Avançar/Voltar Mídia" },
}

-- Cabeçalho
os.execute("clear")
print("\n" .. amarelo .. negrito .. "    󰌌  SISTEMA DE ATALHOS - HYPRLAND" .. reset .. "\n")

local placar = 0

--Descobrir o tamanho da maior string de tecla
for index, valor in ipairs(atalhos) do
    local tamanho_atual = #valor.tecla
    if tamanho_atual > placar then
        placar = tamanho_atual
    end
end

--  Renderizar e alinhar perfeitamente
for index, valor in ipairs(atalhos) do
    local tamanho_atual = #valor.tecla

    local quantidade = placar - tamanho_atual
    local espacos = string.rep(" ", quantidade)

    local linha_formatada = "  " .. ciano .. negrito .. valor.tecla .. reset .. espacos .. roxo .. " 󰁔 " .. verde .. valor.acao .. reset
    print(linha_formatada)
end

-- Rodapé de saída
print("\n" .. roxo .. negrito .. "  Pressione [ENTER] para fechar..." .. reset)
io.read()
