# ONI — Fedora / Arch

Requer Hyprland 0.55 ou superior, com configuração exclusivamente Lua.

Tema baseado no samurai do wallpaper: vermelho, carvão e azul gelo. Waybar em estilo HUD com setores numerados, CPU/RAM e bateria como HP; os valores são métricas reais.

## Instalar

```bash
cd ~/dotfiles
./install-deps.sh
./install.sh --dry-run
./install.sh
```

O instalador de dependências solicita sudo e a confirmação do gerenciador. Instala o próprio Hyprland. Suporta Fedora tradicional e EndeavourOS, Arch, Manjaro, Garuda e outras distribuições que declarem ID_LIKE=arch com os pacotes disponíveis nos repositórios oficiais. No Fedora habilita o COPR comunitário nett00n/hyprland mediante confirmação do DNF; no Arch/EndeavourOS usa pacman e não usa AUR nem troca o gerenciador de login. Fedora Atomic não é suportado automaticamente.

O instalador dos links roda SEM sudo. Vincula somente hypr, waybar, rofi, wofi, mako e wallpapers dentro de `${XDG_CONFIG_HOME:-$HOME/.config}`. Não substitui a .config inteira. Configurações existentes dessas pastas são movidas para `.config/dot-backup.XXXXXXXX`; configurações do KDE permanecem no lugar. Pode executar novamente sem duplicar links. Não mova a pasta DOT depois da instalação.

Saia da sessão e escolha Hyprland no login. O wallpaper é iniciado com swaybg em todos os monitores. Arquivos legados inativos estão em archive/ e não são vinculados à .config.

## Organização

- `hypr/hyprland.lua`: entrada para Hyprland 0.55+; módulos em `hypr/lua`.
- `hypr/local.lua`: arquivo opcional para ajustes pessoais carregado por último; crie para configurar monitores e dispositivos específicos.
- `hypr/scripts`: inicialização da sessão e captura de região para clipboard.
- `waybar/style.css`: cores e aparência do HUD; `waybar/config`: módulos.
- `rofi/oni.rasi`: launcher; `mako/config`: notificações; `wofi`: alternativa visual.

Teclado brasileiro; monitores detectados automaticamente. SUPER+Q terminal, SUPER+R launcher, SUPER+E Dolphin, SUPER+C fecha janela, SUPER+I captura região, SUPER+Escape bloqueia, SUPER+1…0 muda workspace e SUPER+Shift+1…0 move janela. SUPER+Shift+Space alterna fullscreen.

## Restaurar

Saia do Hyprland. Para cada pasta desejada, confira com `readlink ~/.config/hypr` se é o link para esta DOT; remova somente esse link com `unlink ~/.config/hypr` e mova a pasta correspondente do backup de volta. Repita para as outras pastas. Nunca remova a .config inteira.

## Limites e validação

Scripts verificados com bash -n e instalação testada em diretório temporário com conflito, backup e segunda execução. Não foram instalados pacotes nem iniciada uma sessão gráfica durante a preparação. Aparência e compatibilidade completa com a versão instalada precisam ser verificadas após login; use `hyprctl configerrors`. Os módulos Lua existentes foram preservados e adaptados à API 0.55; não é possível prometer compatibilidade com toda versão futura.

## Aparência dos aplicativos

GTK usa Adwaita escuro e Qt6 usa qt6ct/Fusion com paleta darker. A variável Qt só é aplicada na sessão Hyprland; não alteramos kdeglobals. A preferência GNOME color-scheme=prefer-dark é persistente para o usuário e pode afetar apps GTK em outras sessões. Firefox deve estar com tema Sistema/Automático; temas e preferências explícitos de um aplicativo têm prioridade. Não alteramos perfis do Firefox, não instalamos extensões e não forçamos sites sem suporte a modo escuro. Apps Qt5/Flatpak ou com tema próprio podem exigir ajuste no aplicativo. O visual do Hyprland e da Waybar foi mantido.

A revisão inclui qt6ct na lista de pastas vinculadas, com backup da configuração anterior. O tema darker é fornecido pelo pacote qt6ct.
