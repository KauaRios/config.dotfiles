# Wallpaper e cores

Super+W abre o Rofi com imagens de `${XDG_CONFIG_HOME:-~/.config}/wallpapers`, incluindo subpastas. A seleção é manual; Escape cancela sem modificar o tema. São listados PNG, JPG, JPEG e WebP. Nomes com espaços são suportados; nomes com quebra de linha, retorno de carro ou separador de campos são omitidos. O seletor mostra cartões com miniaturas e nomes.

## Dependências

Python 3, Rofi, swaybg, Matugen com `image --dry-run --json hex`, hyprctl, makoctl, notify-send e procps (pgrep/pkill). A correção foi validada com Matugen 4.2.0 instalado. `install-deps.sh` inclui Matugen nos pacotes comuns e Python 3 nos dois caminhos: `python` no Arch/EndeavourOS e `python3` no Fedora. Matugen existe nos repositórios oficiais de ambas as distribuições; a versão fornecida pode variar. A integração foi testada com 4.2.0, sem garantir compatibilidade com versões anteriores.

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

## Galeria visual de wallpapers

O menu exclusivo `rofi/wallpapers.rasi` segue a referência de cartões horizontais: quatro colunas, imagem acima do nome, fundo escuro, contorno fino e seleção preenchida com a cor principal. Mostra somente a lista de cartões, sem campo de pesquisa e sem rodapé. A geometria padrão é 900×300px, com cartões de 240px e área quadrada de miniatura. Abaixo de 940px passa para duas colunas em uma janela de 480px; somente em telas menores que 520px usa largura percentual. As miniaturas preservam a proporção; não há recorte forçado.

`choose()` envia cada nome relativo e o campo nativo `icon` com `thumbnail://` seguido do caminho absoluto da imagem. O Rofi usa um thumbnailer XDG do sistema e seu cache. Neste sistema, glycin-thumbnailer já está instalado e declara suporte a JPEG, PNG e WebP. Em outra instalação, é necessário um thumbnailer para esses formatos. A seleção continua retornando o índice original, para distinguir nomes iguais em subpastas. Escape mantém a imagem atual. Nomes longos podem aparecer abreviados visualmente. Use as setas para navegar, Enter para aplicar e Escape para fechar.

O tema importa `rofi/colors.rasi` (bg, fg, accent), que já recebe cores do Matugen. O argumento `-no-config` isola o seletor das configurações do launcher, e `-theme` carrega somente o tema da galeria. Super+R e o seletor de Waybar permanecem com o tema anterior. Super+W já chama o script atualizado: basta fechar e abrir o menu.

Arquivos desta mudança:
- `hypr/scripts/wallpaper.py`: geração das entradas com miniaturas e uso do tema exclusivo.
- `rofi/wallpapers.rasi`: layout, tipografia, estados de seleção e adaptação à largura.
- `tests/test_wallpaper.py`: testes de miniaturas, seleção por índice, caracteres especiais e leitura do tema pelo Rofi.
- `tests/README.md` e este documento: cobertura e instruções.

Validação da galeria: 55 testes passaram e 4 foram ignorados. O Rofi instalado aceitou o tema. Os testes simulam seleção e verificam os caminhos das miniaturas; não comprovam decodificação/renderização real das imagens. A sessão gráfica não é acessível neste ambiente, portanto a aparência não foi comparada pixel a pixel com a referência. A cor selecionada acompanha o wallpaper, em vez de ficar rosa fixa.

Correção da galeria: removidos inputbar e texto de ajuda; o ícone de cada item solicita agora uma miniatura XDG. Mensagens stderr do Rofi são exibidas pelo script para diagnosticar falhas de imagem. O carregamento gráfico ainda não pôde ser validado neste ambiente por bloqueio de D-Bus/Wayland.

Estabilidade do layout: a janela, a lista e os cartões têm altura explícita; as miniaturas reservam uma área quadrada mesmo durante o carregamento. A regra anterior de 92% abaixo de 1100px foi removida, pois podia deixar o menu mais largo em um monitor menor. A renderização ainda precisa ser conferida na sessão real.
