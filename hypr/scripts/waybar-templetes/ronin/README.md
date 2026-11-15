# Ronin

Baseada na Waybar de `reference.png`: faixa escura contínua, “menu” à esquerda, workspaces em um contorno fino, traços para workspaces ocupados, pontos para vazios e um traço maior para o ativo. À direita ficam a navegação anterior, inibição de suspensão, volume, hora e data.

Altura de 32px e fonte de 12px para manter legibilidade. As cores vêm de `colors.css`; o laranja da referência passa a ser o destaque do wallpaper. Nenhuma fonte de ícones extra é necessária.

- menu: abre Rofi.
- Traços/pontos: selecionam workspaces. Rolagem e chevrons ‹ › navegam entre eles.
- Monitor: alterna inibição de suspensão automática. Não desliga o monitor.
- Volume: clique alterna mudo; botão direito abre pavucontrol.
- Hora: clique alterna os segundos. Data é atualizada pelo relógio real.

Selecione **ronin** com Super+Shift+R. O modelo fica nos templates, sem substituir a Waybar ativa. A pasta assets acompanha a cópia. O Fastfetch correspondente é documentado em `fastfetch/README.md` na raiz do repositório.

Validação: JSON, CSS GTK, referências dos módulos, SVGs e cópia em diretório temporário. A captura foi usada como referência visual; escala, fonte, cores e estados reais dos workspaces afetam o resultado na sua sessão.
