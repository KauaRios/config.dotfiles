#  — Fedora / Arch

![Demonstração das dotfiles com Hyprland, Waybar e wallpaper de anime](visual.png)


Requer Hyprland 0.55 ou superior, com configuração exclusivamente Lua.

Wallpaper de anime com garota de cabelo branco. A paleta escura é gerada a partir da imagem escolhida pelo Matugen. Waybar fina e transparente, com indicadores em pequenos blocos escuros, ícones Unicode e tons de azul e lilás; os valores são métricas reais. O relógio alterna entre hora e data ao clicar. Os ícones usam DejaVu Sans e Noto Sans Symbols 2 quando disponível, sem depender de Nerd Fonts.

## Instalar

```bash
cd ~/dotfiles
./install-deps.sh
./install.sh --dry-run
./install.sh
```

O instalador de dependências solicita sudo e a confirmação do gerenciador. Instala o próprio Hyprland, Matugen e Python 3 para o seletor de wallpaper e a geração da paleta. Suporta Fedora tradicional e EndeavourOS, Arch, Manjaro, Garuda e outras distribuições que declarem ID_LIKE=arch com os pacotes disponíveis nos repositórios oficiais. No Fedora habilita o COPR comunitário nett00n/hyprland mediante confirmação do DNF; no Arch/EndeavourOS usa pacman para os pacotes oficiais e revisa o PKGBUILD do AUR para instalar zen-browser-bin. Não troca o gerenciador de login. Fedora Atomic não é suportado automaticamente.

O instalador dos links roda SEM sudo. Vincula somente hypr, waybar, rofi, wofi, mako, wallpapers, qt6ct, kitty e fastfetch dentro de `${XDG_CONFIG_HOME:-$HOME/.config}`. Não substitui a .config inteira. Configurações existentes dessas pastas são movidas para `.config/dot-backup.XXXXXXXX`; configurações do KDE permanecem no lugar. Pode executar novamente sem duplicar links. Não mova a pasta DOT depois da instalação.

Saia da sessão e escolha Hyprland no login. O wallpaper é restaurado pelo script Python no login e exibido com swaybg. Super+W permite escolher uma imagem e gerar cores com Matugen. Consulte [a documentação completa](WALLPAPER.md).

## Organização

- `hypr/hyprland.lua`: entrada para Hyprland 0.55+; módulos em `hypr/lua`.
- `hypr/local.lua`: arquivo opcional para ajustes pessoais carregado por último; crie para configurar monitores e dispositivos específicos.
- `hypr/scripts`: cheatsheet no terminal, controle de volume e captura de região para clipboard.
- `waybar/style.css`: cores e aparência do HUD; `waybar/config`: módulos.
- `rofi/oni.rasi`: launcher; `mako/config`: notificações; `wofi`: alternativa visual.

Teclado brasileiro; HDMI-A-1 principal a 1920×1080/144 Hz e eDP-1 secundário a 1920×1080/144 Hz, conforme o perfil original. Notebook à esquerda, HDMI à direita; workspace 1 e cursor inicial no HDMI. Outros monitores usam detecção automática. SUPER+Q terminal, SUPER+R launcher, SUPER+E Dolphin, SUPER+C fecha janela, SUPER+I captura região, SUPER+Escape bloqueia, SUPER+1…0 muda workspace e SUPER+Shift+1…0 move janela. SUPER+Shift+Space alterna fullscreen.

## Restaurar

Saia do Hyprland. Para cada pasta desejada, confira com `readlink ~/.config/hypr` se é o link para esta DOT; remova somente esse link com `unlink ~/.config/hypr` e mova a pasta correspondente do backup de volta. Repita para as outras pastas. Nunca remova a .config inteira.

## Limites e validação

Scripts verificados com bash -n e instalação testada em diretório temporário com conflito, backup e segunda execução. Não foram instalados pacotes nem iniciada uma sessão gráfica durante a preparação. Aparência e compatibilidade completa com a versão instalada precisam ser verificadas após login; use `hyprctl configerrors`. Os módulos Lua existentes foram preservados e adaptados à API 0.55; não é possível prometer compatibilidade com toda versão futura.

## Aparência dos aplicativos

GTK usa Adwaita escuro e Qt6 usa qt6ct/Fusion com paleta darker. A variável Qt só é aplicada na sessão Hyprland; não alteramos kdeglobals. A preferência GNOME color-scheme=prefer-dark é persistente para o usuário e pode afetar apps GTK em outras sessões. Zen Browser deve estar com tema Sistema/Automático; temas e preferências explícitos de um aplicativo têm prioridade. Não alteramos perfis do Zen Browser, não instalamos extensões e não forçamos sites sem suporte a modo escuro. Apps Qt5/Flatpak ou com tema próprio podem exigir ajuste no aplicativo. O visual do Hyprland e da Waybar foi mantido.

A revisão inclui qt6ct na lista de pastas vinculadas, com backup da configuração anterior. O tema darker é fornecido pelo pacote qt6ct.

O Dolphin pode usar um esquema próprio, independente da paleta do qt6ct. Se abrir claro, selecione **Configurações → Esquema de cores → Breeze Dark** no Dolphin. A escolha é salva em `dolphinrc` e também pode afetar o Dolphin em outras sessões; o instalador não sobrescreve esse arquivo.

## Módulos do Hyprland

| Arquivo em `hypr/lua` | Responsabilidade |
| --- | --- |
| `monitors.lua` | Resolução, frequência, posição e monitor inicial do cursor |
| `workspaces.lua` | Associação dos workspaces aos monitores |
| `appearance.lua` | Bordas, cores, espaçamentos, transparência e blur |
| `animations.lua` | Curvas e animações |
| `layouts.lua` | Comportamento dos layouts |
| `input.lua` | Teclado, mouse, touchpad e gestos |
| `misc.lua` | Comportamento geral e cursor |
| `window-rules.lua` | Regras específicas de janelas |
| `keybinds.lua` | Atalhos |
| `programs.lua` | Aplicativos padrão |
| `variables.lua` | Variáveis de ambiente e tema dos apps |
| `autostart.lua` | Inicialização da sessão |

`hypr/local.lua` continua opcional e é carregado por último para ajustes pessoais. A configuração original dos monitores foi restaurada; confira os modos no hardware real com `hyprctl monitors all`. O ajuste de posição `1921x0` preserva o workaround original; pode ser mudado para `1920x0` caso já não seja necessário.

## Verificação na sessão gráfica

Depois de instalar e entrar no Hyprland, execute `hyprctl configerrors` e `hyprctl monitors all`. Confira fullscreen (Super+Shift+Space), terminal flutuante (Super+Shift+Q), ajuda (Super+H), scroll dos workspaces e captura (Super+I). A suíte valida a configuração com o verificador do Hyprland; aparência e comportamento durante uma sessão precisam ser conferidos manualmente. A versão dos pacotes da sua distribuição e os modos suportados pelos monitores precisam ser conferidos no sistema real.

## Testes automatizados

Execute como usuário normal, sem sudo, na raiz do repositório:

```bash
python3 tests/run.py
```

O resumo aparece em português. Se já estiver dentro de `tests`, execute `python3 run.py`. Para a lista técnica completa, use `python3 -B -m unittest discover -s tests -v` na raiz do repositório.

Requer Python 3, Bash e utilitários básicos de Linux. Para conferir a sintaxe Lua, instale também `lua` (com `luac`); sem ele, esse teste aparece como `skipped`, não como aprovado.

A suíte verifica sintaxe Bash/Lua, JSON da Waybar, referências dos módulos, links simbólicos, backups, preservação do KDE, reinstalação, mudança do nome da pasta, simulação sem escrita e entradas inválidas. Também testa captura cancelada, falhas de captura/clipboard e controle de volume com ferramentas simuladas. Quando PyGObject e GTK 3 estão disponíveis, valida o CSS da Waybar sem iniciar a barra.

Os testes de instalação usam diretórios temporários e uma cópia do instalador. Não instalam pacotes, não acessam a `.config` real e não capturam sua tela. A suíte também oferece testes gráficos opcionais em uma sessão Hyprland aninhada. Aparência dos temas, disponibilidade dos pacotes e compatibilidade dos monitores físicos continuam exigindo conferência no sistema real.

Quando disponíveis, a suíte também verifica a leitura do tema pelo Rofi e consulta `hyprctl configerrors` na sessão Hyprland ativa. A consulta verifica a configuração carregada na sessão, que pode ser diferente da configuração deste repositório; sem acesso à sessão, o teste é ignorado.

A Waybar mostra a RAM usada em GiB. O botão de energia alterna os perfis disponíveis do `power-profiles-daemon`; o serviço precisa estar ativo e os perfis disponíveis dependem do equipamento.

### Inicialização da sessão

Waybar, mako e swaybg são iniciados em `hypr/lua/autostart.lua`, no evento `hyprland.start`. A mesma configuração aplica as preferências de tema e inicia o agente de autenticação. O autostart chama `wallpaper.py --restore`.

Saia e entre novamente na sessão para aplicar a mudança e encerrar os supervisores da versão anterior. O evento de início não é uma ação de retorno da suspensão; a causa da perda da conexão Wayland após suspender ainda precisa ser investigada.

### Atalhos (Super+H)

Super+W abre o seletor manual de wallpaper e atualiza a paleta. Requer Matugen.

O Super+H abre a lista de atalhos no Kitty, usando `hypr/scripts/cheat_sheet.lua`.
Pressione Enter para fechar.

A Waybar consulta a temperatura da CPU AMD pelo sensor `k10temp` (Tctl). O caminho do dispositivo em `temperature.hwmon-path-abs` deve ser ajustado em outros computadores. Clicar no indicador de rede abre `kcmshell6 kcm_networkmanagement`, disponível com as configurações de rede do KDE neste sistema.

### Validação estrita

`python3 tests/run.py --strict` retorna erro se qualquer teste for ignorado ou tiver falha esperada. O modo normal também lista essas limitações, mas só retorna erro para falhas, erros e sucessos inesperados. O relatório inclui tempo total e grupos de volume, atalhos e funcionamento do próprio executor.

Os testes de volume substituem `wpctl` e `notify-send`: conferem os comandos, o limite de 100%, porcentagem, mudo e falhas sem alterar o áudio real. Os testes do executor usam suítes temporárias para verificar falhas de importação, subtestes, resultados inesperados e códigos de saída.

### Validação da API real do Hyprland

`tests/test_hyprland_api.py` executa o binário instalado com `Hyprland --verify-config --config <cópia temporária>/hyprland.lua`. A configuração base é copiada para um diretório temporário, sem `local.lua` pessoal. HOME e diretórios XDG são isolados; as variáveis de conexão com a sessão gráfica e D-Bus são removidas. O comando tem limite de 20 segundos e não inicia o compositor nem dispara o evento de autostart.

Três testes verificam a aceitação da configuração base, a rejeição de uma opção inexistente e a rejeição de uma chamada Lua inexistente. A validação usa a versão instalada (verificada com Hyprland 0.57.1), sem garantir compatibilidade com outras versões ou o comportamento de janelas, atalhos e monitores em execução.

Para rodar somente esses testes:

```bash
python3 -B -m unittest discover -s tests -p test_hyprland_api.py -v
```

Sem Hyprland ou sem suporte a `--verify-config`, o grupo é informado como ignorado; `--strict` retorna erro nesses casos. Falhas ao executar o verificador ou configurações rejeitadas fazem os testes falharem. A consulta separada a `hyprctl configerrors` continua conferindo apenas a sessão ativa.

### Integração gráfica

`python3 tests/run.py --gui --strict` abre sessões Hyprland isoladas dentro de janelas Wayland e testa foco, flutuação, fullscreen e mudança de workspace via IPC. Também inicia a Waybar com o config/CSS do repositório, verifica a layer e a reserva de espaço e confirma a rejeição de CSS inválido. Requer uma sessão Wayland acessível, `dbus-run-session`, GTK 3/PyGObject, Hyprland e Waybar.

O autostart e o perfil dos monitores físicos são desativados apenas nas cópias temporárias. Os testes não pressionam teclas físicas nem avaliam beleza ou comparam screenshots. Consulte [tests/README.md](tests/README.md) para a cobertura de **cada arquivo**, dependências, isolamento e limites.

### Créditos

O tema do seletor de wallpapers (`rofi/wallpapers.rasi`) foi adaptado de
[di0gosilva/hyprland-dotfiles](https://github.com/di0gosilva/hyprland-dotfiles),
com integração às cores dinâmicas destas dotfiles.

### Navegador padrão: Zen Browser

Super+B e o atalho de navegador do Kasumi usam `zen-browser`. No Arch, o instalador inclui Zen pelo AUR, com revisão e consentimento explícito. Neste computador, o Zen é fornecido pelo pacote `zen-browser-bin`, com lançador `zen.desktop`. No Fedora, instale o Zen separadamente conforme o [guia oficial](https://docs.zen-browser.app/guides/install-linux) e garanta que o comando `zen-browser` esteja no PATH. Se usar Flatpak, ajuste o comando para `flatpak run app.zen_browser.zen` em `hypr/lua/programs.lua`, no template Kasumi e na variável BROWSER.

Para definir os links HTTP/HTTPS e páginas HTML com a instalação nativa:

```bash
xdg-mime default zen.desktop x-scheme-handler/http x-scheme-handler/https text/html application/xhtml+xml
```

As associações pertencem ao usuário e também afetam links abertos em outras sessões gráficas. PDFs continuam com o leitor configurado. Depois de mudar um template, selecione-o novamente para atualizar a Waybar ativa.

### Aprovação do PKGBUILD do Zen (Arch)

Execute `./install-deps.sh` como usuário normal. O script instala git e base-devel pelos repositórios oficiais e chama `scripts/install-zen-arch.sh`. Se zen-browser-bin já estiver instalado, essa etapa é ignorada.

A etapa do AUR baixa a receita de https://aur.archlinux.org/zen-browser-bin.git, mostra a revisão e todos os arquivos versionados, incluindo PKGBUILD e eventuais hooks .install. Nenhum makepkg é executado antes da revisão. Caracteres de controle são mostrados de forma visível. Para prosseguir é necessário digitar exatamente `CONFIO`; Enter, outra resposta ou fim de entrada abortam a instalação do Zen e encerram o instalador com erro. Os pacotes oficiais instalados anteriormente permanecem.

Após aceitar, `makepkg --syncdeps --install --needed` usa a mesma cópia mostrada, como usuário normal. O pacman solicita elevação/confirmação quando necessário. A pasta temporária é removida ao sair. Não há aprovação automática nem helper AUR. A revisão é feita pelo usuário: exibir o PKGBUILD não certifica sua segurança nem a dos arquivos que ele baixa. No Fedora não existe etapa PKGBUILD, pois esse formato pertence ao Arch.

### Fastfetch

Execute `fastfetch` no Kitty para ver a imagem da Marika e os blocos de sistema/hardware. As cores acompanham o wallpaper nas próximas execuções. Veja [configuração e personalização](fastfetch/README.md).
