# Akai

Baseado na nova reference1.png: barra técnica fina com extremidades diagonais, launcher em destaque, workspaces numéricos e composição data / título / relógio central. À direita: RAM, temperatura da CPU, uso de CPU, inibidor de suspensão, bloqueio e bandeja.

As cores vêm do colors.css separado, vinculado à paleta dinâmica. O vermelho da captura é substituído pela cor principal atual. Os recortes são gradientes GTK e podem variar conforme a largura dos módulos. Os ícones são Unicode; não exigem Nerd Fonts.

Não foi inventada uma segunda temperatura: a captura possui sensores cuja origem não é identificável. O modelo usa temperatura real do perfil AMD existente e carga da CPU. Ajuste hwmon-path-abs em outro hardware. O ponto alterna a inibição de suspensão; o quadrado bloqueia a sessão.

JSON e CSS validados sem aplicação. A aparência não foi comparada na sessão gráfica. Abra Super+Shift+R e escolha akai para aplicar quando desejar.

## Contraste e marca

Workspace ativo usa fundo principal preenchido, texto escuro, negrito e sublinhado; vazios são discretos e os demais mantêm texto secundário. O hover não apaga a seleção. O launcher usa a silhueta do Arch Linux em SVG, obtida de /usr/share/pixmaps/archlinux-logo.svg (archlinux-artwork), incorporada como data URI no CSS para funcionar após a cópia do modelo. O símbolo é escuro sobre o destaque dinâmico e não depende de fonte de ícones.
