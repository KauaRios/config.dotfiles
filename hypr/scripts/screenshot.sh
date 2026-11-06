#!/usr/bin/env bash
set -euo pipefail
region=$(slurp) || exit 0
[[ -n $region ]] || exit 0
# Não substitui o clipboard se a captura falhar.
umask 077
capture=$(mktemp --suffix=.png)
trap 'rm -f -- "$capture"' EXIT
grim -g "$region" "$capture"
wl-copy --type image/png < "$capture"
