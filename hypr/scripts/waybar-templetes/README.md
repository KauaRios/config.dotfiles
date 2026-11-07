# Modelos alternativos de Waybar

Estes modelos não estão instalados e não são iniciados pelo Hyprland.

- `original`: seu modelo anterior, recuperado do backup anterior à primeira troca; barra superior compacta.
- `reference-01`: referência `reference.png`, faixa contínua fina, marca à esquerda, workspaces centrais e mídia em destaque.
- `reference-02`: referência `reference1.png`, três blocos separados, relógio central e workspaces à esquerda.
- `reference-03`: referência `reference3.png`, painel escuro arredondado, data à esquerda e círculos centrais.
- `orbit`: barra inferior flutuante, painel arredondado, workspaces em cápsulas e relógio central grande.
- `ribbon`: faixa superior contínua, cantos retos, workspaces sublinhados e relógio central em bloco de destaque.

Cada pasta contém `config`, `style.css` e um link `colors.css` para `../../../../waybar/colors.css`. As cores seguem a paleta dinâmica existente: `panel` é fundo, `blue` é destaque principal (não necessariamente azul), `purple` é destaque secundário e `muted` é cor discreta. Alertas usam cores semânticas fixas. Não há dependência de Nerd Fonts.

Para o seu futuro seletor Python: copie somente `config` e `style.css` do modelo escolhido para a pasta ativa `~/.config/waybar/`, preservando o `colors.css` existente. Não copie o link relativo dos modelos para a pasta ativa: ele serve apenas para validar ou visualizar os modelos dentro deste repositório. Faça backup dos arquivos atuais antes de substituí-los. A troca de modelo deve recarregar/reiniciar a Waybar; alterar o wallpaper continua gerando a mesma paleta compartilhada.

Os módulos usam as configurações do projeto atual (inclusive a ação de rede específica do KDE). A ausência de bateria ou de serviços pode ocultar módulos. As larguras variam conforme texto, resolução e escala; confira em monitores pequenos. As configurações JSON e o CSS GTK são validados sem iniciar a barra. Não houve aplicação nem avaliação visual na sessão gráfica.

## Seletor Python

Execute `python3 ~/.config/hypr/scripts/waybar.py` para escolher pelo Rofi. Escape cancela. A main lista os modelos, recebe a escolha, copia os arquivos e recarrega a barra.

O script usa cópias simples com shutil.copy2 e preserva colors.css. O primeiro backup fica em `${XDG_STATE_HOME:-~/.local/state}/dotfiles-waybar/original`. Para recuperar esse backup manualmente, copie seus arquivos config e style.css para a pasta ativa da Waybar. Os modelos continuam disponíveis após a troca.

A versão simplificada não possui opções --list, --template ou --restore, lock nem escrita atômica. Evite executar duas trocas simultâneas. Uma falha durante a cópia pode exigir restauração manual do backup. JSON é validado antes da cópia; CSS e aparência devem ser conferidos ao criar os modelos. Nenhuma troca é aplicada apenas por instalar o script.

## Novos modelos

- **Ember**: reference1.png; blocos escuros retangulares com destaque da paleta.
- **Astral**: reference2.png; painel compacto com título central e workspaces à esquerda.
- **Tsuki**: criação autoral, três painéis flutuantes arredondados, lua e relógio com data.

Todos mantêm colors.css separado e usam a paleta dinâmica. São descobertos automaticamente pelo seletor.

- **Akai**: nova reference1.png, faixa técnica com recortes diagonais e título central destacado; cores dinâmicas separadas.
