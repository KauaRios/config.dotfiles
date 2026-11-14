# Marika — Fastfetch

Abra o Kitty e execute `fastfetch`. A imagem fornecida fica à esquerda; os blocos SYSTEM e HARDWARE seguem a organização da referência, com bordas finas, dados reais e temperatura da CPU. Use uma janela com aproximadamente 100 colunas para evitar quebras. Não é iniciado automaticamente a cada terminal.

## Cores do wallpaper

`wallpaper.py` recebe a paleta do Matugen e `apply_colors()` preenche `hypr/scripts/theme-templates/fastfetch.jsonc`. O resultado vai para `~/.config/fastfetch/config.jsonc` (ou `$XDG_CONFIG_HOME/fastfetch/config.jsonc`). O instalador vincula essa pasta ao repositório.

- `primary`: rótulos e bordas.
- `secondary`: título do usuário.
- `on_surface`: valores das informações.
- Os círculos finais mostram a paleta do terminal, independente da paleta do wallpaper.

A imagem da Marika permanece igual. Execute `fastfetch` novamente depois de trocar o wallpaper para ver as novas cores; texto já impresso não é atualizado. A restauração do wallpaper também reaplica as cores salvas.

Para mudar o layout permanentemente, edite o **template**: a configuração gerada será sobrescrita na próxima troca. Sem troca de wallpaper, a configuração incluída funciona normalmente.

## Imagem e instalação

A imagem original está em `assets/Queen Marika the Eternal, Ruan Zoe.jpg`. O protocolo gráfico Kitty exibe a imagem preservando a proporção; outros terminais podem não suportar esse protocolo. O caminho suporta espaços e XDG_CONFIG_HOME. O pacote `fastfetch` foi incluído nas dependências. `install.sh` instala os links de Kitty/Fastfetch com backup das pastas anteriores.

Para verificar somente os dados: `fastfetch --logo none`. Os testes validam a geração da paleta e a leitura pelo Fastfetch real, sem comprovar a aparência gráfica no terminal.

O logo fica explicitamente à esquerda, com duas linhas de margem superior para equilibrar o retrato com os dois blocos. A largura continua em 28 colunas, preservando a proporção; a altura visual depende das células da fonte do Kitty. Esses ajustes estão também no template para persistirem na troca de wallpaper.
