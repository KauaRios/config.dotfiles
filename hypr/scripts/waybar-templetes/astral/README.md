# Astral

Origem: reference2.png: faixa escura compacta, relógio/workspaces à esquerda e título central.

As cores ficam separadas em colors.css, vinculado à paleta ativa. Use o seletor (Super+Shift+R) para aplicar; nenhum modelo é aplicado automaticamente. O script copia config e style.css e preserva a paleta do wallpaper. Os tons das referências são adaptados às cores atuais.

Métricas são reais. Não há clima nem waveform fictícios; mídia depende de um player MPRIS, brilho de um dispositivo backlight e bateria de hardware disponível. Ícones Unicode substituem os glifos específicos das capturas. Não é uma reprodução pixel a pixel: fontes, escala, resolução e conteúdo influenciam o resultado. Os modelos foram validados em JSON e GTK CSS, sem iniciar uma barra na sessão.

## Lado direito

Faixa direita com brilho, inibidor de suspensão por clique, Bluetooth, bandeja, rede e áudio em ícones. CPU discreta e bateria em destaque. Os detalhes de rede/volume aparecem no tooltip. Bluetooth requer BlueZ/controlador; o inibidor depende do suporte do compositor e do gerenciador de inatividade.

## Áudio e temperatura

O CAVA fica ao lado do volume, com oito bandas reais a 24 quadros por segundo. Captura a saída padrão pelo PulseAudio/PipeWire-Pulse; em silêncio, fica discreto. O adaptador `assets/astral-cava.py` deriva do Kasumi, com configuração própria em `astral-cava.conf`. CAVA já está nas dependências do instalador.

A temperatura ao lado do uso da CPU usa o sensor Tctl do Ryzen (`k10temp`), atualizado a cada cinco segundos. A partir de 85 °C, ganha destaque visual. O caminho do sensor é específico deste notebook e precisa ser ajustado em outro hardware. As cores usam exclusivamente a paleta separada em `colors.css`.
