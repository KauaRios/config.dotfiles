# Kasumi

Modelo baseado em reference.png: fundo transparente, lançador claro, sete workspaces quadrados arredondados, grupo de três atalhos, música central e cartões separados à direita. Relógio com fundo claro. Altura solicitada de 38px, cartões de aproximadamente 30px e fonte de 13px para tamanho intermediário.

## Temperatura da CPU

O cartão de temperatura fica entre memória e bateria. Usa o sensor AMD k10temp/Tctl, confirmado neste notebook, em `/sys/devices/pci0000:00/0000:00:18.3/hwmon`, arquivo `temp1_input`. Atualiza a cada cinco segundos. O caminho evita depender do número hwmon5, que pode mudar entre inicializações. Em outro computador, ajuste o dispositivo. O destaque em 85°C é um alerta visual configurável.

## Paleta e ícones

`colors.css` é um link para a paleta dinâmica da Waybar. Os blocos, textos e seleção acompanham o wallpaper; portanto os tons azul e rosa da referência variam com sua paleta. Os quatro SVGs em assets foram desenhados para este modelo a partir das formas visíveis na captura; não são arquivos originais da referência. Eles têm cores próprias para preservar os símbolos e não dependem de Nerd Fonts.

## Conteúdo e ações

- Lançador abre Rofi. Os atalhos abrem Firefox, Spotify Web e OBS Studio (requer OBS instalado).
- A música usa MPRIS: título e artista reais; clique pausa/continua, clique direito avança. Requer playerctl para os cliques e um player compatível aberto para mostrar conteúdo.
- Volume e rede usam os valores reais. Os quatro quadrados reproduzem o detalhe da referência: são decorativos, com uso real da RAM no tooltip; não são um gráfico de carga.
- Temperatura adicionada a pedido do usuário. Bateria e relógio usam valores reais.

Selecione `kasumi` com Super+Shift+R. A criação do template não aplica o tema à barra ativa. O seletor copia também assets, preservando colors.css.

## Validação

JSON, CSS GTK, SVGs e leitura do sensor foram conferidos. A suíte geral não compara pixels nem confirma a aparência na sessão gráfica. É necessário conferir visualmente após selecionar o modelo.
