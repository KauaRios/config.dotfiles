#!/usr/bin/env bash

# Executa a ação recebida (aumentar, diminuir ou mutar) limitando a 100% (1.0)
case "$1" in
    up)
        wpctl set-volume -l 1.0 @DEFAULT_AUDIO_SINK@ 5%+
        ;;
    down)
        wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-
        ;;
    toggle)
        wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle
        ;;
esac

# Captura o estado atual do áudio no sistema
VOLUME_INFO=$(wpctl get-volume @DEFAULT_AUDIO_SINK@)

# Verifica se está mutado e dispara a notificação síncrona
if [[ "$VOLUME_INFO" == *"MUTED"* ]]; then
    notify-send -a "Volume" -t 1500 -h string:x-canonical-private-synchronous:audio "Áudio Mutado 󰝟"
else
    # Extrai o valor decimal, converte para porcentagem e limpa as casas decimais
    VOL=$(echo "$VOLUME_INFO" | awk '{print int($2 * 100)}')
    
    # Envia a notificação com a barra de progresso (value:$VOL)
    notify-send -a "Volume" -t 1500 -h string:x-canonical-private-synchronous:audio -h int:value:"$VOL" "Volume: ${VOL}% 󰕾"
fi


