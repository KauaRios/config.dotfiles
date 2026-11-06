-- Também executa ao recarregar: os supervisores usam locks por sessão.
hl.exec_cmd("bash \"${XDG_CONFIG_HOME:-$HOME/.config}/hypr/scripts/session.sh\"")
