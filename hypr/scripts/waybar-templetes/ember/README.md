# Ember

Origem: reference1.png: blocos retangulares finos e separados, workspaces à esquerda e relógio central.

As cores ficam separadas em colors.css, vinculado à paleta ativa. Use o seletor (Super+Shift+R) para aplicar; nenhum modelo é aplicado automaticamente. O script copia config e style.css e preserva a paleta do wallpaper. Os tons das referências são adaptados às cores atuais.

Métricas são reais. Não há clima nem waveform fictícios; mídia depende de um player MPRIS, brilho de um dispositivo backlight e bateria de hardware disponível. Ícones Unicode substituem os glifos específicos das capturas. Não é uma reprodução pixel a pixel: fontes, escala, resolução e conteúdo influenciam o resultado. Os modelos foram validados em JSON e GTK CSS, sem iniciar uma barra na sessão.

## Lado direito

Faixa direita de telemetria com temperatura, nome da interface, bateria e volume, dividida por separadores retos. O botão de seta bloqueia a sessão. A temperatura usa o sensor AMD do perfil original; ajuste hwmon-path-abs em outro hardware.
