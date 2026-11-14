# Graphite

Modelo baseado em `reference_waybar.png`: painel superior único centralizado, borda dupla visual, quatro workspaces quadrados, espectro largo à esquerda, data/hora ao centro e indicadores compactos à direita. Altura de 38px, fonte de 13px e largura de 1500px, pensada para seu monitor de 1920px. Para telas menores, reduza `width` e o número de módulos.

O espectro é real: 20 bandas do CAVA, monitorando a saída padrão. O adaptador Python deriva do Kasumi deste próprio repositório, com validação do quadro e encerramento do processo filho. Requer `cava` e PipeWire-Pulse/PulseAudio. Em silêncio, permanece discreto. Falhas aparecem como `!` no módulo.

O botão ▶ controla reprodução com playerctl, ♫ abre spotify-launcher e ◎ alterna a inibição de suspensão. A bandeja mostra os aplicativos realmente abertos; não simula os ícones da captura. CPU, memória, bateria e temperatura mostram os dados reais. O sensor de temperatura é o k10temp do seu Ryzen, herdado da configuração local.

As cores vêm do link `colors.css`, separado do estilo; a paleta do wallpaper substitui o cinza da referência. A temperatura e bateria foram mantidas para seu uso. Isso e os aplicativos da bandeja podem mudar a largura em relação à captura.

Selecione **graphite** em Super+Shift+R. Não aplicado automaticamente. JSON e CSS GTK verificados; fidelidade final de espaçamento e renderização depende de conferência na sua sessão.
