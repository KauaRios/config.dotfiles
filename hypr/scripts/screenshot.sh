#!/usr/bin/env bash
set -euo pipefail
region=$(slurp) || exit 0
grim -g "$region" - | wl-copy --type image/png
