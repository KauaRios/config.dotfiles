#!/usr/bin/env bash
set -euo pipefail
source /etc/os-release
family=" ${ID:-} ${ID_LIKE:-} "
common=(hyprland waybar rofi kitty dolphin firefox mako swaybg hyprlock grim slurp wl-clipboard brightnessctl playerctl wireplumber xdg-desktop-portal-hyprland xdg-desktop-portal-gtk)
run=()
if (( EUID != 0 )); then run=(sudo); fi
case "$family" in
    *arch*)
        command -v pacman >/dev/null
        "${run[@]}" pacman -Syu --needed "${common[@]}" pipewire pipewire-pulse ttf-dejavu lua
        ;;
    *fedora*)
        if [[ -e /run/ostree-booted ]]; then
            echo 'Fedora Atomic detectado: este instalador atende Fedora tradicional com DNF.' >&2
            exit 1
        fi
        command -v dnf >/dev/null
        # Fedora pode fornecer o launcher Wayland em um pacote separado.
        if dnf -q list --available rofi-wayland >/dev/null 2>&1 || rpm -q rofi-wayland >/dev/null 2>&1; then
            common[2]=rofi-wayland
        fi
        "${run[@]}" dnf install "${common[@]}" pipewire pipewire-pulseaudio dejavu-sans-mono-fonts lua
        ;;
    *) echo "Distribuição não suportada: ${ID:-desconhecida}. Use Fedora ou família Arch." >&2; exit 1 ;;
esac
Hyprland --version
echo 'Dependências instaladas. Execute ./install.sh sem sudo e escolha Hyprland na tela de login.'
