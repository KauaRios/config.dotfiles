#!/usr/bin/env bash
set -euo pipefail
source /etc/os-release
family=" ${ID:-} ${ID_LIKE:-} "
common=(power-profiles-daemon hyprland waybar rofi kitty dolphin mako swaybg hyprlock grim slurp wl-clipboard brightnessctl playerctl wireplumber xdg-desktop-portal-hyprland xdg-desktop-portal-gtk hyprpolkitagent wofi qt6ct gsettings-desktop-schemas matugen cava)
run=()
if (( EUID != 0 )); then run=(sudo); fi
case "$family" in
    *" arch "*|*" endeavouros "*|*" manjaro "*|*" garuda "*)
        command -v pacman >/dev/null
        "${run[@]}" pacman -Syu --needed "${common[@]}" pipewire pipewire-pulse ttf-dejavu lua libnotify procps-ng python
        ;;
    *" fedora "*)
        if [[ -e /run/ostree-booted ]]; then
            echo 'Fedora Atomic detectado: este instalador atende Fedora tradicional com DNF.' >&2
            exit 1
        fi
        command -v dnf >/dev/null
        echo 'Fedora: habilitando o repositório comunitário COPR nett00n/hyprland.'
        echo 'O DNF pedirá confirmação antes de habilitar e instalar.'
        "${run[@]}" dnf install 'dnf-command(copr)'
        "${run[@]}" dnf copr enable nett00n/hyprland
        # Fedora pode fornecer o launcher Wayland em um pacote separado.
        if dnf -q list --available rofi-wayland >/dev/null 2>&1 || rpm -q rofi-wayland >/dev/null 2>&1; then
            common[3]=rofi-wayland
        fi
        "${run[@]}" dnf install "${common[@]}" pipewire pipewire-pulseaudio dejavu-sans-mono-fonts lua libnotify procps-ng python3
        ;;
    *) echo "Distribuição não suportada: ${ID:-desconhecida}. Use Fedora ou família Arch." >&2; exit 1 ;;
esac
version=$(Hyprland --version)
printf '%s\n' "$version"
number=
if [[ $version =~ ([0-9]+\.[0-9]+\.[0-9]+) ]]; then number=${BASH_REMATCH[1]}; fi
if [[ -z $number || $(printf '%s\n' 0.55.0 "$number" | sort -V | head -n1) != 0.55.0 ]]; then
    echo 'Estas dotfiles exigem Hyprland >= 0.55. Confira a versão do repositório.' >&2
    exit 1
fi
echo 'Dependências instaladas. Execute ./install.sh sem sudo e escolha Hyprland na tela de login.'

# Zen é instalado separadamente; não é um pacote comum a pacman e DNF.
if ! command -v zen-browser >/dev/null; then
    echo 'Instale Zen Browser separadamente e disponibilize o comando zen-browser.'
    echo 'Arch: pacote zen-browser-bin (AUR). Guia: https://docs.zen-browser.app/guides/install-linux'
fi
