# Sora — referência

Reconstruída a partir de `reference.png` na raiz do repositório. Uma cápsula escura única, com altura de 38px e largura de 1280px, centralizada no topo. Sem os painéis separados, abas retas e selo Arch das versões anteriores.

A ordem acompanha a captura:

1. Temperatura, ponto separador, hora em destaque e data discreta em uma linha.
2. Mídia sobre uma pequena cápsula interna; sem player aparece “Nothing playing right now”.
3. Dez workspaces, com apenas o ativo preenchido e circular.
4. Volume, bateria, uso da CPU com rótulo, Bluetooth, brilho, perfil de energia, faixa anterior e menu de sessão.

## Adaptações mantidas para suas dotfiles

- Os workspaces usam 一 二 三 四 五 六 七 八 九 十, conforme solicitado. Os atalhos seguem numéricos.
- O destaque alaranjado da foto é substituído pela cor do wallpaper; `colors.css` permanece separado.
- No lugar da temperatura do clima, exibimos a temperatura real da CPU Ryzen. Não há consulta de clima nem valor fictício.
- Os controles usam ícones simbólicos padrão do tema GTK (Breeze neste sistema, com fallback Adwaita), no tamanho de 18px. O termômetro usa SVG local. Dados e módulos disponíveis dependem do hardware/serviços; Bluetooth e brilho podem ficar ausentes em outros sistemas.
- Altura e fonte foram adaptadas para legibilidade; a fidelidade visual final precisa ser conferida na sessão gráfica.

## Controles

- Mídia: clique para pausar/continuar; botão direito abre `spotify-launcher`.
- Alto-falante: clique alterna mudo; botão direito abre pavucontrol.
- Bluetooth: abre `kcmshell6 kcm_bluetooth`.
- Brilho: rolagem ajusta com brightnessctl.
- Perfil de energia: alterna os perfis disponíveis; o ícone acompanha economia, equilibrado ou desempenho.
- Ícone de música anterior (barra + triângulo): executa `playerctl previous` no player ativo; não altera workspaces.
- Energia: abre menu no Rofi. Só executa bloquear, suspender, reiniciar ou desligar depois de selecionar a opção. Escape cancela.

A mídia usa `playerctl` com timeout, JSON e escape de markup. O menu de sessão recebe somente opções predefinidas e não executa conteúdo arbitrário do Rofi.

Selecione **sora** em Super+Shift+R; o seletor copia config, CSS e assets. Testes validam CSS/JSON, renderização dos SVG, cópia dos assets, estado vazio da mídia, escape de títulos e seleção/cancelamento do menu de sessão. Não comparam screenshots.


O uso da CPU aparece como `CPU 12%`, em vez de um chip isolado. Os nomes dos ícones foram conferidos nos temas Breeze e Adwaita instalados. A resolução visual do tema requer uma sessão gráfica; a análise de CSS sem display pode emitir avisos do GTK. Nenhum tema de ícones foi instalado ou copiado para o repositório.
