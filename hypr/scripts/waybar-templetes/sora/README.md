# Sora

CSS reescrito com uma composição geométrica e altura de 44px. Superfícies planas, cantos de 2–3px e bordas finas substituem os painéis arredondados e gradientes anteriores.

- **Esquerda:** marca Arch separada, navegação em abas com numerais japoneses (一 二 三 四 五) e bloco de mídia. O workspace ativo tem preenchimento sólido.
- **Centro:** hora em 20px e data em um campo separado, unidos pela borda inferior.
- **Direita:** segmentos contíguos para temperatura, rede, volume, perfil e bateria; bandeja em um bloco separado. A temperatura recebe uma borda lateral de destaque.

Os ícones de status foram desenhados para este modelo, em SVG de 24px com traço uniforme. São exibidos em 18px e recoloridos pelo GTK conforme a propriedade `color` do módulo. A nota do Spotify foi substituída por um ícone vetorial; o Arch continua usando o asset do Akai deste repositório. Não precisa de Nerd Fonts.

## Cores e instalação

`colors.css` continua separado, apontando para a paleta compartilhada da Waybar. Fundo, textos, ícones simbólicos e workspace ativo acompanham o wallpaper. A marca do Arch mantém o desenho escuro sobre a cor principal.

Selecione **sora** em Super+Shift+R. O seletor copia também os arquivos `assets/sora-*.svg`. Não copie apenas o CSS: os ícones precisam acompanhar o modelo.

## Controles

- Arch: abre Rofi.
- Spotify: abre `spotify-launcher`.
- Música: clique pausa/continua; botão direito abre Spotify.
- Volume: clique alterna mudo; botão direito abre pavucontrol.
- Rede: abre as configurações de rede do KDE.
- Relógio: alterna exibição dos segundos.
- Perfil de energia: alterna os perfis disponíveis.

Temperatura usa k10temp do Ryzen deste computador. O título musical depende de um player MPRIS ativo, e a bandeja depende dos aplicativos abertos.

## Validação

Testes conferem JSON, referências de módulos, link da paleta e sintaxe CSS GTK. Os SVG são renderizados pelo librsvg; uma cópia temporária verifica o CSS com os assets fora do repositório. Isso não substitui a avaliação da aparência na sessão gráfica.

A implementação de recoloração segue a [documentação CSS do GTK 3](https://docs.gtk.org/gtk3/css-overview). O código deste modelo foi escrito para as dotfiles; não foram copiados estilos de outros autores.

Os workspaces de 1 a 10 usam 一 二 三 四 五 六 七 八 九 十. Apenas o rótulo visual muda; atalhos e IDs permanecem numéricos. O texto usa Noto Sans CJK JP (presente neste sistema), com fallback do sistema. As superfícies são planas; a cor do texto é derivada da paleta com maior luminosidade.
