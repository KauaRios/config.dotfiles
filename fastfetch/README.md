# Ronin — Fastfetch

Layout baseado na captura `reference.png`: máscara em texto à esquerda, três blocos SYSTEM / SOFTWARE / HARDWARE à direita, etiquetas curtas com fundo e uma linha de amostras de cores no rodapé.

A máscara em `assets/ronin.txt` foi transcrita dos pontos Braille visíveis na referência fornecida. É texto Unicode, não imagem; não precisa do protocolo gráfico Kitty. Os dados são coletados pelo Fastfetch: a distribuição aparece como EndeavourOS neste computador, junto com seu hardware real. O CT mostra a temperatura da CPU. Não há números fixos copiados da captura.

Execute `fastfetch`. Recomenda-se uma janela de pelo menos 100 colunas para os nomes das GPUs; fontes ou terminais diferentes podem mudar as proporções do desenho. O terminal controla o fundo da janela, não o Fastfetch.

## Paleta dinâmica

`wallpaper.py` preenche `hypr/scripts/theme-templates/fastfetch.jsonc` e grava em `${XDG_CONFIG_HOME:-~/.config}/fastfetch/config.jsonc`. Edite o **template** para mudanças permanentes de layout.

- `primary`: máscara e destaques.
- `outline`: fundo das etiquetas/blocos.
- `surface`: texto sobre essas etiquetas.
- `on_surface`: dados do sistema.
- `secondary`: amostras de cor.

O laranja da captura é substituído pela paleta do wallpaper. Execute Fastfetch de novo após trocar o tema: a saída já impressa não é redesenhada.

## Substituição e validação

A configuração e o PNG da Marika foram retirados. Antes da troca, a pasta Fastfetch foi copiada para `~/.local/state/fastfetch-before-ronin-*`.

Os testes geram duas paletas e executam o Fastfetch instalado sem logo gráfico. A leitura da máscara e o alinhamento textual também foram verificados com a CLI. A aparência da fonte no terminal precisa de conferência visual.
