# Modelos alternativos de Waybar

Estes modelos não estão instalados e não são iniciados pelo Hyprland.

- `original`: seu modelo anterior, recuperado do backup anterior à primeira troca; barra superior compacta.
- `orbit`: barra inferior flutuante, painel arredondado, workspaces em cápsulas e relógio central grande.
- `ribbon`: faixa superior contínua, cantos retos, workspaces sublinhados e relógio central em bloco de destaque.

Cada pasta contém `config`, `style.css` e um link `colors.css` para `../../../../waybar/colors.css`. As cores seguem a paleta dinâmica existente: `panel` é fundo, `blue` é destaque principal (não necessariamente azul), `purple` é destaque secundário e `muted` é cor discreta. Alertas usam cores semânticas fixas. Não há dependência de Nerd Fonts.

Para o seu futuro seletor Python: copie somente `config` e `style.css` do modelo escolhido para a pasta ativa `~/.config/waybar/`, preservando o `colors.css` existente. Não copie o link relativo dos modelos para a pasta ativa: ele serve apenas para validar ou visualizar os modelos dentro deste repositório. Faça backup dos arquivos atuais antes de substituí-los. A troca de modelo deve recarregar/reiniciar a Waybar; alterar o wallpaper continua gerando a mesma paleta compartilhada.

Os módulos usam as configurações do projeto atual (inclusive a ação de rede específica do KDE). A ausência de bateria ou de serviços pode ocultar módulos. As larguras variam conforme texto, resolução e escala; confira em monitores pequenos. As configurações JSON e o CSS GTK são validados sem iniciar a barra. Não houve aplicação nem avaliação visual na sessão gráfica.

## Seletor Python

`python3 ~/.config/hypr/scripts/waybar.py` abre o Rofi. `--list` apenas lista modelos; `--template orbit` aplica diretamente; `--restore` recupera a barra anterior à primeira troca. O backup fica em `${XDG_STATE_HOME:-~/.local/state}/dotfiles-waybar/original`. O script copia config e CSS, preserva cores, e solicita reload com SIGUSR2. Não foi aplicado automaticamente nem associado a atalho. Modelos novos devem conter JSON válido em `config` e CSS GTK válido em `style.css`; o script valida JSON, mas não valida CSS em execução. A recarga real deve ser conferida na sessão gráfica.
