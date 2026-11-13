#!/usr/bin/env bash
# Executar como usuário normal. Código do AUR só é executado após consentimento.
set -euo pipefail
if (( EUID == 0 )); then
    echo 'Execute sem sudo: makepkg não deve rodar como root.' >&2
    exit 1
fi
if pacman -Q zen-browser-bin >/dev/null 2>&1; then
    echo 'Zen Browser já instalado; nenhuma instalação pelo AUR necessária.'
    exit 0
fi
command -v git >/dev/null
command -v makepkg >/dev/null
build_dir=$(mktemp -d -t dotfiles-zen.XXXXXXXX)
trap 'rm -rf -- "$build_dir"' EXIT

echo 'Baixando a receita de https://aur.archlinux.org/zen-browser-bin.git'
git clone --depth 1 -- https://aur.archlinux.org/zen-browser-bin.git "$build_dir/package"
cd -- "$build_dir/package"
[[ -f PKGBUILD && ! -L PKGBUILD ]] || { echo 'PKGBUILD ausente ou inválido.' >&2; exit 1; }
printf '\nRevisão que será instalada: '
git rev-parse HEAD
echo 'Leia os arquivos abaixo. O pacote é mantido pela comunidade AUR.'
echo 'Aceitar autoriza executar a receita, baixar suas fontes e instalar o pacote.'
# Mostra também hooks .install e arquivos auxiliares, não apenas o PKGBUILD.
# cat -v torna caracteres de controle visíveis, sem interpretá-los no terminal.
while IFS= read -r -d '' file; do
    [[ -f $file && ! -L $file ]] || { echo 'Arquivo não regular na receita; instalação abortada.' >&2; exit 1; }
    printf '\n--- %q ---\n' "$file"
    cat -v -- "$file"
done < <(git ls-files -z)
printf '\nVocê leu e confia nesta receita? Digite CONFIO para instalar: '
answer=
if ! IFS= read -r answer || [[ $answer != CONFIO ]]; then
    echo 'Zen não instalado: receita não aprovada.'
    exit 1
fi
# Usa a mesma cópia exibida; não faz pull nem invoca um helper AUR depois da revisão.
# Dependências e instalação final continuam sujeitas às confirmações do pacman.
makepkg --syncdeps --install --needed
