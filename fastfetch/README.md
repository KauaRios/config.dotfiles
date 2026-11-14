# Marika — Fastfetch

Abra o Kitty e execute `fastfetch`. O retrato da Marika fica à esquerda de uma composição compacta, com o título “MARIKA / THE ETERNAL QUEEN”, divisórias com losangos e o bloco VITALS. Os rótulos Tarnished e Realm representam usuário e sistema operacional; Heat mostra a temperatura real da CPU. Use uma janela com aproximadamente 80 colunas para evitar quebras. Não é iniciado automaticamente a cada terminal.

## Cores do wallpaper

`wallpaper.py` recebe a paleta do Matugen e `apply_colors()` preenche `hypr/scripts/theme-templates/fastfetch.jsonc`. O resultado vai para `~/.config/fastfetch/config.jsonc` (ou `$XDG_CONFIG_HOME/fastfetch/config.jsonc`). O instalador vincula essa pasta ao repositório.

- `primary`: rótulos, título Marika e primeiro grupo de círculos.
- `secondary`: subtítulo, VITALS e segundo grupo de círculos.
- `on_surface`: valores das informações.
- `outline`: divisórias e terceiro grupo de círculos. Todos os círculos acompanham o wallpaper.

A imagem da Marika permanece igual. Execute `fastfetch` novamente depois de trocar o wallpaper para ver as novas cores; texto já impresso não é atualizado. A restauração do wallpaper também reaplica as cores salvas.

Para mudar o layout permanentemente, edite o **template**: a configuração gerada será sobrescrita na próxima troca. Sem troca de wallpaper, a configuração incluída funciona normalmente.

## Imagem e instalação

A imagem original está em `assets/Queen Marika the Eternal, Ruan Zoe.jpg`. O protocolo gráfico Kitty exibe a imagem preservando a proporção; outros terminais podem não suportar esse protocolo. O caminho suporta espaços e XDG_CONFIG_HOME. O pacote `fastfetch` foi incluído nas dependências. `install.sh` instala os links de Kitty/Fastfetch com backup das pastas anteriores.

Para verificar somente os dados: `fastfetch --logo none`. Os testes validam a geração da paleta e a leitura pelo Fastfetch real, sem comprovar a aparência gráfica no terminal.

O retrato fica explicitamente à esquerda, sem margem superior, com largura de 26 colunas e quatro colunas de espaço até o texto. A proporção original é preservada; a altura visual depende das células da fonte do Kitty. O layout também está no template para persistir na troca de wallpaper.

## Retrato transparente

O Fastfetch usa `assets/Queen Marika-transparent.png`, com transparência. O JPG original foi preservado. Edição com a ferramenta integrada image_gen; pode haver pequenas diferenças no desenho por ser uma edição generativa.

Prompt: “Use case: background-extraction. Edit target: supplied Marika illustration. Remove only the dark background and floating background particles to create a clean transparent PNG cutout for a terminal Fastfetch logo. Preserve Marika's original face, anatomy, outstretched pose, hair, crown, dress, illustration style, colors and framing. Preserve the attached flowing gold ribbons. Real alpha transparency, clean fine hair edges, no checkerboard painted into the image, no new objects or text.”
