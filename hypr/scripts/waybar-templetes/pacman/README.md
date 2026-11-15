# Pacman

Barra superior de 36px com relógio/mídia à esquerda, workspaces centrais e indicadores à direita. O Pac-Man ativo é um SVG de 27px, com boca e olho vazados, sobre fundo de destaque. Os demais workspaces são bolinhas, formando o percurso. Cliques e rolagem mantêm o comportamento anterior.

## Música e temperatura

- Barras CAVA reais de quatro bandas, reaproveitando o adaptador do Kasumi destas dotfiles. Capturam o monitor da saída padrão, não o microfone. Clique nas barras para abrir Spotify.
- Título da música via MPRIS. Clique para pausar/continuar; botão direito abre `spotify-launcher`. O título só aparece quando há player compatível aberto; em silêncio as barras ficam discretas.
- Temperatura da CPU via `k10temp` do Ryzen deste computador, atualizada a cada cinco segundos. Exibida como `CPU 54°C`, com destaque adicional a partir de 85°C. Ajuste o caminho do sensor em outros equipamentos.

A fonte geral passou de 9px para 12px para acompanhar os novos módulos e melhorar a leitura. `colors.css` continua separado e vinculado à paleta dinâmica: o Pac-Man acompanha a cor principal do wallpaper, sem amarelo fixo.

Selecione **pacman** em Super+Shift+R. O seletor copia config, style.css e assets; mantém colors.css ativo. CAVA e playerctl já fazem parte das dependências das dotfiles. Falta do CAVA ou erro de captura aparece como `!`, com explicação no tooltip.

Validação: JSON, CSS GTK, renderização do SVG, cópia dos assets e saída do visualizador com CAVA simulado. Não foi possível conferir a renderização na sessão gráfica.
