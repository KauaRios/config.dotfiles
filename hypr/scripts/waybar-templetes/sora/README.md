# Sora

Três blocos flutuantes com altura de 44px e cantos de 12px. A composição organiza as funções, sem criar uma cápsula por indicador:

- **Esquerda:** Arch, cinco workspaces e música com título limitado. O workspace ativo recebe preenchimento sólido da cor principal.
- **Centro:** hora em 18px e dia/data em duas linhas, sobre fundo escuro.
- **Direita:** temperatura da CPU, rede, volume, perfil de energia, bateria e bandeja. Memória foi retirada para reduzir informação.

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
