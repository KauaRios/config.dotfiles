# Ronin

Barra contínua com 40px de altura, margem superior de 10px e cantos de 9px. O desenho mantém a navegação em traços/pontos da referência e organiza três áreas:

- **Navegação:** menu, seta anterior, cinco workspaces e seta seguinte no mesmo grupo. Botões com largura fixa; o ativo usa um traço de 24×6px, os ocupados 12×4px e os vazios um ponto de 4px.
- **Janela:** título da janela ativa no monitor, limitado a 32 caracteres para preservar o espaço dos controles. O tooltip mostra o título completo. Sem título, aparece “Ronin”.
- **Status:** temperatura da CPU, inibição de suspensão e volume. Hora em destaque e data curta fecham a barra à direita.

As superfícies escuras, os textos claros e os estados de foco derivam de `colors.css`. A cor principal destaca menu, workspace ativo e relógio; textos auxiliares usam a cor discreta. A fonte é Noto Sans com fallback DejaVu Sans; números de temperatura, volume e hora usam DejaVu Sans Mono. Não exige Nerd Fonts.

## Controles

- **menu:** abre Rofi.
- **Workspaces:** clique seleciona; rolagem e setas navegam.
- **Monitor:** alterna inibição de suspensão automática. O fundo destacado indica que está ativa.
- **Volume:** clique alterna mudo; botão direito abre pavucontrol. Mudo usa ícone próprio e o texto “Mudo”.
- **Hora:** clique alterna os segundos.

A temperatura é lida do sensor k10temp do Ryzen deste computador, a cada cinco segundos. A partir de 85°C, o indicador ganha preenchimento. O caminho `temperature.hwmon-path-abs` deve ser ajustado em outros equipamentos.

## Aplicação e validação

Selecione **ronin** com Super+Shift+R. O seletor copia config, style.css e assets e preserva a paleta ativa. Super+L reinicia a Waybar.

JSON, referências dos módulos, CSS GTK, carregamento dos SVG e cópia para uma pasta temporária foram verificados. Uma maquete com Cairo/Pango foi usada para revisar proporções com duas paletas e dados ilustrativos; ela não é uma captura da Waybar. A sessão gráfica não estava acessível neste ambiente, portanto foco real, renderização do compositor e cliques ainda precisam de conferência na sessão.
