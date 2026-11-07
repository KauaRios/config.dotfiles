# Testes das dotfiles

Execute como usuário normal. A biblioteca `unittest` do Python é suficiente para o executor; cada teste informa as ferramentas externas necessárias quando elas faltam.

```bash
python3 tests/run.py
python3 tests/run.py --gui --strict
```

O primeiro comando executa a suíte local e informa os testes gráficos como ignorados. `--gui` habilita a integração gráfica, que exige uma sessão Wayland acessível. `--strict` retorna erro também para testes ignorados ou falhas esperadas. Para saída detalhada, use `python3 -B -m unittest discover -s tests -v`; para habilitar gráficos nessa forma, defina `DOTFILES_TEST_GUI=1`.

## O que cada arquivo verifica

| Arquivo | Cobertura | Limites e dependências |
| --- | --- | --- |
| `run.py` | Descobre os testes, agrupa resultados em português, informa falhas, testes ignorados, duração e código de saída. Oferece `--gui` e `--strict`. | É o executor, não um teste. |
| `test_runner.py` | Executa o executor em diretórios temporários com suítes artificiais: sucesso, teste ignorado, dependência ausente na classe, subtestes com falha, erro de importação e sucesso inesperado. Confere relatórios e códigos de saída. | Não executa os outros testes recursivamente. |
| `test_dotfiles.py` — `ConfigTests` | Sintaxe Bash/Lua, referências dos módulos Lua, configuração dos módulos Waybar, CSS pelo GTK, tema Rofi, fallback de XDG vazio e momento de inicialização dos aplicativos. | Bash e Lua para sintaxe; GTK 3/PyGObject e Rofi para seus validadores. As simulações de Lua não substituem a API real. |
| `test_dotfiles.py` — `InstallTests` | Links e backups, preservação do KDE, reinstalação, mudança do caminho do repo, dry-run, symlink quebrado e rejeição de argumentos/caminhos inválidos ou origens ausentes. | Copia o instalador para diretórios temporários. Não altera a `.config` real nem instala pacotes. Requer execução sem root. |
| `test_dotfiles.py` — `ScreenshotTests` | Captura cancelada/vazia, falha do capturador, sucesso e falha do clipboard; preservação do conteúdo anterior e limpeza dos temporários. Confere argumentos de região e MIME. | Usa substitutos de `slurp`, `grim` e `wl-copy`; não captura a tela real. |
| `test_dotfiles.py` — `HyprlandSessionTests` | Consulta `hyprctl configerrors` na sessão ativa. | Somente leitura. Não comprova que a sessão carregou este checkout; é ignorado quando a sessão está inacessível. |
| `test_cheatsheets.py` | Descrições das binds, expansão dos workspaces 1–10, bind de mouse e comando do Super+H para a ajuda Lua no Kitty. | Usa Lua com objetos `hl` simulados; não abre o terminal. |
| `test_volume.py` | Argumentos de aumento/redução/mudo, limite de volume, porcentagem da notificação, estado mudo, argumentos inválidos e propagação de falhas de áudio. | Substitui `wpctl` e `notify-send`; não altera o áudio. |
| `test_hyprland_api.py` | O Hyprland instalado aceita a configuração base e rejeita uma opção inexistente e uma chamada Lua inválida. | Usa `--verify-config` sem iniciar o compositor, com HOME/XDG temporários e sem `local.lua` pessoal. |
| `test_graphical.py` | Janela GTK recebe foco; dispatchers alternam flutuação/fullscreen e movem janela/foco para o workspace 2. A Waybar real cria uma layer e reserva espaço no topo com o config/CSS do repo. Uma folha CSS inválida é rejeitada na inicialização real. | Opt-in, com Hyprland, hyprctl, Waybar, dbus-run-session e GTK 3/PyGObject. Requer acesso ao compositor Wayland pai. |

## Como a integração gráfica é isolada

Cada teste gráfico cria uma sessão Hyprland dentro de uma janela da sessão Wayland existente, usando renderização por software, `AQ_DRM_DEVICES=/dev/null`, HOME/XDG temporários e um barramento D-Bus próprio. A prontidão exige IPC funcional e monitores com backend `wayland`. As chamadas `hyprctl` sempre usam o socket e a assinatura da instância temporária.

A cópia da configuração carrega os módulos do repositório, exceto `autostart`, `monitors` e `workspaces`: o teste desabilita serviços pessoais e substitui o perfil físico por uma saída aninhada. `local.lua` não é copiado e animações são desativadas para tornar as verificações de estado determinísticas. A Waybar usa o config/CSS reais, mas o teste não clica nos módulos que executam comandos.

Os subprocessos são encerrados pelos grupos criados pelo teste, sem `pkill` global. Os diretórios temporários são removidos ao final, inclusive após falhas. Há limites de tempo para inicialização, IPC e encerramento. Se uma dependência ou sessão pai estiver ausente, os testes são ignorados; falhas depois da tentativa de inicialização são erros, não aprovação.

## O que ainda precisa de conferência manual

- Aparência agradável, legibilidade e comparação com `reference.png`; não há comparação automatizada de screenshots.
- Teclas físicas, combinações de modificadores e cliques: os testes atuais chamam os dispatchers via IPC.
- Conteúdo e atualização de cada módulo da Waybar, serviços de rede/energia e menus abertos por clique.
- Autostart real, múltiplos monitores físicos, escala, GPU, suspensão e retomada.

Validação feita com Hyprland 0.57.1. Para executar sem o sandbox que bloqueia o socket Wayland, use um terminal normal da sua sessão. Isso abre e fecha algumas janelas de teste; não execute como root.

## Testes do seletor de modelos da Waybar

`test_waybar_templates.py` testa funções de `hypr/scripts/waybar.py`. Cada teste que copia arquivos usa uma pasta temporária; as respostas do Rofi são simuladas.

| Teste | Situação e resultado conferido |
| --- | --- |
| `test_cancel` | O Rofi retorna código 1 (cancelamento); `escolher_template` retorna `None`. Não executa a main inteira. |
| `test_unknown_selection` | O seletor responde `../bad`, fora dos modelos oferecidos; a função lança `ValueError`. |
| `test_copy_preserves_palette_and_original_backup` | Aplica um modelo duas vezes, verifica que `colors.css` permanece igual e que o CSS de origem continua disponível. Aplica o backup e confirma que o CSS original volta, comprovando que o segundo uso não sobrescreveu esse backup. |
| `test_invalid_json_does_not_modify_destination` | O modelo contém JSON inválido; a função rejeita e o destino continua vazio. |

Esses quatro testes não comprovam aparência, abertura real do Rofi, recarga por SIGUSR2, recuperação de falhas de disco, execução simultânea nem validade de todos os modelos. Também não verificam todos os conteúdos copiados: o teste do backup confere explicitamente o CSS, não a igualdade do JSON restaurado.

Outras verificações relacionadas à Waybar:

- `test_dotfiles.py` confere o JSON/módulos e o CSS GTK da configuração ativa no repositório.
- `test_cheatsheets.py` confere que Super+Shift+R aponta para `waybar.py`, usando simulação Lua; não pressiona a tecla.
- `test_graphical.py`, habilitado com `--gui`, testa a layer/espaço reservado pela barra e rejeição de CSS inválido em sessão isolada. Não executa a troca de modelos pelo seletor.

Para rodar somente os quatro testes do seletor, mostrando a descrição de cada um:

```bash
python3 -B -m unittest discover -s tests -p test_waybar_templates.py -v
```

O teste `test_optional_assets_are_copied_without_changing_palette` verifica que recursos locais (ícones/CSS auxiliar) acompanham a cópia do modelo e que a paleta ativa continua intacta. Ele não verifica renderização do SVG.
