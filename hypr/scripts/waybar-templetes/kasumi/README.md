# Kasumi

Modelo baseado em reference.png: fundo transparente, lançador claro, sete workspaces quadrados arredondados, grupo de três atalhos, música central e cartões separados à direita. Relógio com fundo claro. Altura solicitada de 38px, cartões de aproximadamente 30px e fonte de 13px para tamanho intermediário.

## Temperatura da CPU

O cartão de temperatura fica entre o visualizador e a bateria. Usa o sensor AMD k10temp/Tctl, confirmado neste notebook, em `/sys/devices/pci0000:00/0000:00:18.3/hwmon`, arquivo `temp1_input`. Atualiza a cada cinco segundos. O caminho evita depender do número hwmon5, que pode mudar entre inicializações. Em outro computador, ajuste o dispositivo. O destaque em 85°C é um alerta visual configurável.

## Paleta e ícones

`colors.css` é um link para a paleta dinâmica da Waybar. Os blocos, textos e seleção acompanham o wallpaper; portanto os tons azul e rosa da referência variam com sua paleta. Os quatro SVGs em assets foram desenhados para este modelo a partir das formas visíveis na captura; não são arquivos originais da referência. Eles têm cores próprias para preservar os símbolos e não dependem de Nerd Fonts.

## Conteúdo e ações

- Lançador abre Rofi. Os atalhos abrem Firefox, Spotify Web e Obsidian (comando `obsidian`, encontrado neste sistema).
- A música usa MPRIS: título e artista reais; clique pausa/continua, clique direito avança. Requer playerctl para os cliques e um player compatível aberto para mostrar conteúdo.
- Volume e rede usam os valores reais. As quatro barras são um visualizador real de áudio: CAVA analisa a saída padrão e atualiza as alturas a 30 quadros por segundo. No silêncio ficam baixas.
- Temperatura adicionada a pedido do usuário. Bateria e relógio usam valores reais.

Selecione `kasumi` com Super+Shift+R. A criação do template não aplica o tema à barra ativa. O seletor copia também assets, preservando colors.css.

## Validação

JSON, CSS GTK, SVGs e leitura do sensor foram conferidos. A suíte geral não compara pixels nem confirma a aparência na sessão gráfica. É necessário conferir visualmente após selecionar o modelo.

Ícones refinados: Obsidian em cristal facetado roxo, globo com linhas curvas, Spotify com arcos uniformes e lançador com anéis mais definidos. Atalhos têm área de 32px, ícones de 20px e realce ao passar o mouse.

## Visualizador de áudio

Requer `cava` (incluído em install-deps.sh). Instalação manual: `sudo pacman -S --needed cava` no Arch ou `sudo dnf install cava` no Fedora. Depois selecione Kasumi novamente.

`assets/kasumi-cava.conf` usa o monitor da saída padrão via PulseAudio/PipeWire-Pulse, sem usar o microfone. `assets/kasumi-cava.py` transforma quatro valores de 0 a 7 em caracteres de altura variável e envia JSON à Waybar. Os scripts e a configuração acompanham o modelo na pasta assets. A cor continua vindo de colors.css. O processo CAVA é encerrado quando o módulo recebe SIGTERM. Se o programa não estiver instalado ou falhar, aparece `!` com diagnóstico no tooltip.

A análise de áudio real precisa ser validada na sessão gráfica; os testes automatizados verificam a conversão e a integração usando saída CAVA simulada.

## Perfil de energia

O módulo nativo power-profiles-daemon fica entre a temperatura e a bateria. Clique para alternar entre os perfis disponíveis: ♧ economia, ◐ equilibrado e ϟ desempenho. O tooltip mostra o nome do perfil. Requer o serviço power-profiles-daemon em execução; o pacote já consta em install-deps.sh. A disponibilidade dos perfis depende do hardware.
