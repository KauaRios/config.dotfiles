# Wallpaper e cores

Super+W abre o Rofi com imagens de `${XDG_CONFIG_HOME:-~/.config}/wallpapers`, incluindo subpastas. A seleção é manual; Escape cancela sem modificar o tema. São listados PNG, JPG, JPEG e WebP. Nomes com espaços são suportados; nomes com quebra de linha são omitidos. O seletor lista nomes, sem miniaturas.

## Dependências

Python 3, Rofi, swaybg, Matugen com `image --dry-run --json hex`, hyprctl, makoctl, notify-send e procps (pgrep/pkill). A correção foi validada com Matugen 4.2.0 instalado. No Arch/EndeavourOS, instale `matugen` pelo gerenciador de pacotes; no Fedora, confira sua disponibilidade para a versão utilizada antes de habilitar um repositório. O instalador existente continua instalando swaybg; Matugen é uma dependência adicional da troca de paleta.

Após instalar Matugen, execute `hyprctl reload` e pressione Super+W. Para escolher diretamente:

```bash
python3 ~/.config/hypr/scripts/wallpaper.py --image ~/Imagens/exemplo.jpg
```

## Fluxo e arquivos

`hypr/lua/keybinds.lua` chama `hypr/scripts/wallpaper.py`. O script consulta o Rofi, executa Matugen em modo escuro e valida as cores antes de alterar o wallpaper. Matugen usa `--dry-run`: o Python controla a aplicação dos arquivos, sem hooks pessoais do Matugen.

Os modelos estão em `hypr/scripts/theme-templates/`:

- `waybar.css` gera `waybar/colors.css`, importado pelo estilo. Fundo, destaques e cores principais passam a acompanhar a imagem; alertas mantêm cores próprias.
- `rofi.rasi` gera `rofi/colors.rasi`, importado pelo tema existente.
- `mako.conf` gera `mako/config`. Faça personalizações persistentes no template, pois a próxima escolha sobrescreve esse arquivo.
- `hypr.lua` gera `hypr/lua/colors.lua`, carregado após as opções de aparência para atualizar bordas.

A imagem só é substituída após o novo swaybg permanecer em execução por 0,4 segundo. Isso detecta encerramento imediato, mas não comprova renderização. As instâncias anteriores de swaybg do mesmo usuário são encerradas. A troca pode afetar outra sessão gráfica simultânea desse usuário.

Cada arquivo é substituído atomicamente. O conjunto inteiro não constitui uma transação: erro de disco ou de recarregamento pode deixar uma aplicação parcial. As falhas de recarregamento são impressas; o tema pode ser reaplicado pelo seletor. O script solicita reload ao Hyprland, SIGUSR2 à Waybar e reload ao Mako; Rofi lê o tema na próxima abertura.

A última escolha e sua paleta ficam em `${XDG_STATE_HOME:-~/.local/state}/dotfiles-wallpaper/selection.json`. Um lock nesse diretório impede execuções simultâneas. O script termina após aplicar; apenas swaybg permanece em execução.

`hypr/lua/autostart.lua` chama `--restore` no evento de início. A restauração usa a paleta salva sem chamar Matugen. Sem seleção salva, utiliza a imagem de anime incluída. Se a imagem salva foi removida, volta à anime e conserva a paleta salva. Recarregar Hyprland não abre o seletor.

Como as pastas são links para este repositório, os arquivos gerados aparecem como modificações no Git. Configuração pessoal em `hypr/local.lua`, carregada por último, pode sobrescrever as cores das bordas.

## Verificação

`python3 tests/run.py`: 47 passaram e 4 foram ignorados após a correção do Matugen. Os cinco testes novos verificam cancelamento, nomes com espaços, rejeição de cor inválida, falha de geração antes da aplicação e restauração sem Matugen. Há também testes de diagnóstico de erro, formato JSON atual e extração com Matugen real nas imagens disponíveis. A aparência ainda exige conferência na sessão gráfica.

A suíte também aprovou a configuração com o binário instalado do Hyprland, sintaxe Lua/Bash, CSS GTK e tema Rofi. A consulta à sessão ativa ficou inacessível; três testes gráficos são opcionais. Na sessão local, execute `python3 tests/run.py --gui --strict` e confira manualmente Super+W, Escape, mudança de cores e restauração após novo login. Essa suíte gráfica não testa o seletor de wallpaper de ponta a ponta.

## Retorno ao tema anterior

Os arquivos de cores iniciais e o Mako original estão no Git. Restaure esses arquivos a partir do commit anterior à escolha, remova `selection.json` e recarregue os componentes. Para desativar a integração, volte o autostart para swaybg direto e o atalho para reaplicar a imagem.

## Correção do Matugen 4.2

A execução sem terminal agora fornece `--source-color-index 0`, escolhendo a cor dominante da imagem que o usuário selecionou. Isso não escolhe wallpapers aleatórios. O leitor aceita cores no formato atual `colors.primary.dark.color` e nos formatos anteriores. Erros do Matugen incluem o diagnóstico original na mensagem. A troca acontece na mesma sessão, sem precisar sair e entrar.
