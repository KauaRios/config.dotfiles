# Akai

Baseado na nova reference1.png: barra técnica fina com extremidades diagonais, launcher em destaque, workspaces numéricos e composição data / título / relógio central. À direita: RAM, temperatura da CPU, uso de CPU, inibidor de suspensão, bloqueio e bandeja.

As cores vêm do colors.css separado, vinculado à paleta dinâmica. O vermelho da captura é substituído pela cor principal atual. Os recortes são gradientes GTK e podem variar conforme a largura dos módulos. Os ícones são Unicode; não exigem Nerd Fonts.

Não foi inventada uma segunda temperatura: a captura possui sensores cuja origem não é identificável. O modelo usa temperatura real do perfil AMD existente e carga da CPU. Ajuste hwmon-path-abs em outro hardware. O ponto alterna a inibição de suspensão; o quadrado bloqueia a sessão.

JSON e CSS validados sem aplicação. A aparência não foi comparada na sessão gráfica. Abra Super+Shift+R e escolha akai para aplicar quando desejar.

## Fidelidade à referência

Workspace ativo verde, demais números na cor principal, sem caixas ou sublinhados. O verde fica separado em assets/akai-colors.css; é uma cor fixa de estado para manter a distinção mesmo quando a paleta principal muda. O restante mantém colors.css dinâmico.

O launcher usa o SVG local assets/akai-arch.svg, silhueta do arquivo distribuído por archlinux-artwork, em preto sobre a cor principal, com recorte diagonal. O format contém um caractere de largura zero em vez de espaço vazio para manter o módulo presente. O seletor agora copia a pasta assets dos modelos antes do CSS. Não depende de fonte de ícones nem de data URI.
