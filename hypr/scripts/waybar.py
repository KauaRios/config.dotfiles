from pathlib import Path
import json
import os
import shutil
import subprocess

CONFIG = Path(os.environ.get('XDG_CONFIG_HOME') or Path.home() / '.config') / 'waybar'
DIRETORIO_ATUAL = Path(__file__).resolve().parent
TEMPLATES_DIR = DIRETORIO_ATUAL / 'waybar-templetes'
BACKUP = Path(os.environ.get('XDG_STATE_HOME') or Path.home() / '.local/state') / 'dotfiles-waybar/original'


def listar_templates(directory):
    modelos = []
    for pasta in directory.iterdir():
        if (pasta / 'config').is_file() and (pasta / 'style.css').is_file():
            modelos.append(pasta.name)
    return sorted(modelos)


def escolher_template(modelos):
    resultado = subprocess.run(
        ['rofi', '-dmenu', '-i', '-no-custom', '-p', 'Modelo da Waybar'],
        input='\n'.join(modelos), text=True, capture_output=True,
    )
    if resultado.returncode == 1:
        return None  # Escape cancela sem alterar nada.
    resultado.check_returncode()
    nome = resultado.stdout.rstrip('\n')
    if nome not in modelos:
        raise ValueError('Modelo inválido: ' + nome)
    return nome


def aplicar_template(origem, destino, backup):
    # Verifica os arquivos antes de começar a copiar.
    json.loads((origem / 'config').read_text())
    (origem / 'style.css').read_text()
    if not (destino / 'colors.css').is_file():
        raise ValueError('colors.css não encontrado na Waybar ativa.')

    # Guarda a configuração anterior apenas na primeira troca.
    if not backup.exists():
        backup.mkdir(parents=True)
        shutil.copy2(destino / 'config', backup / 'config')
        shutil.copy2(destino / 'style.css', backup / 'style.css')

    # Alguns modelos possuem ícones/CSS auxiliares referenciados pelo estilo.
    if (origem / 'assets').is_dir():
        shutil.copytree(origem / 'assets', destino / 'assets', dirs_exist_ok=True)

    # Copia o modelo; colors.css continua com a paleta atual.
    shutil.copy2(origem / 'config', destino / 'config')
    shutil.copy2(origem / 'style.css', destino / 'style.css')


def copy_template(name_template):
    origem = TEMPLATES_DIR / name_template
    aplicar_template(origem, CONFIG, BACKUP)


def main():
    modelos = listar_templates(TEMPLATES_DIR)
    if not modelos:
        print('Nenhum modelo encontrado.')
        return

    escolhido = escolher_template(modelos)
    if escolhido is None:
        return

    copy_template(escolhido)
    resultado = subprocess.run(['pkill', '-USR2', '-u', str(os.getuid()), '-x', 'waybar'])
    if resultado.returncode == 1:
        print('Modelo salvo. Abra a Waybar para visualizá-lo.')
    else:
        resultado.check_returncode()
        print('Modelo aplicado: ' + escolhido)


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, subprocess.SubprocessError) as erro:
        raise SystemExit('Erro ao trocar a Waybar: ' + str(erro))
