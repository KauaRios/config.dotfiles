# Sora

Faixa superior contínua de 40px, com cantos discretos e fonte de 13px. Símbolo do Arch à esquerda, cinco workspaces com sublinhado e fundo suave no ativo, música central e relógio à direita. A área de status usa divisórias finas entre conectividade, temperatura/memória e energia.

- Arch: abre Rofi.
- Nota musical: abre o Spotify instalado via `spotify-launcher`.
- Música: clique pausa/continua; botão direito abre Spotify.
- Volume: clique alterna mudo; botão direito abre pavucontrol.
- Rede: abre as configurações de rede do KDE.
- Relógio: alterna hora/data.
- Perfil de energia: alterna os perfis disponíveis.

A temperatura usa o sensor k10temp do Ryzen deste computador. Memória, volume, bateria e temperatura mostram valores reais. O título da música é limitado para conter a largura.

`colors.css` permanece separado e acompanha a paleta do wallpaper. O ícone Arch vem do asset já presente no modelo Akai deste repositório; não depende de Nerd Fonts. O seletor copia `assets/sora-arch.svg` ao aplicar o modelo.

Selecione **sora** em Super+Shift+R. CSS GTK, JSON e links de cores são validados pelos testes; aparência e distribuição dos módulos precisam de conferência na sessão gráfica.

## Pesquisa inicial

A primeira versão explorava painéis arredondados inspirados em comentários sobre [este setup](https://www.reddit.com/r/unixporn/comments/1olgyf0/hyprland_my_first_rice/) e [este outro](https://www.reddit.com/r/unixporn/comments/1n0if4i/hyprland_what_do_you_think/). Após seu feedback, o layout foi refeito como faixa contínua. Não foram copiados arquivos CSS ou configurações desses autores.
