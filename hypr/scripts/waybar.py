#!/usr/bin/env python3
"""Escolhe um modelo de Waybar sem substituir a paleta dinâmica."""
from pathlib import Path
import argparse
import fcntl
import json
import os
import subprocess
import tempfile

CONFIG_HOME = Path(os.environ.get('XDG_CONFIG_HOME') or Path.home() / '.config')
CONFIG = CONFIG_HOME / 'waybar'
TEMPLATES_DIR = Path(__file__).resolve().parent / 'waybar-templetes'
STATE = Path(os.environ.get('XDG_STATE_HOME') or Path.home() / '.local/state') / 'dotfiles-waybar'
ARQUIVOS = ('config', 'style.css')


def listar_templates(directory):
    """Lista apenas pastas que contêm os dois arquivos necessários."""
    return sorted(p.name for p in directory.iterdir()
                  if p.is_dir() and all((p / nome).is_file() for nome in ARQUIVOS))


def escolher_template(nomes):
    resultado = subprocess.run(
        ['rofi', '-dmenu', '-i', '-no-custom', '-p', 'Modelo da Waybar'],
        input='\n'.join(nomes), capture_output=True, text=True,
    )
    if resultado.returncode == 1:
        return None  # Escape: cancelar é uma ação normal.
    resultado.check_returncode()
    escolha = resultado.stdout.rstrip('\n')
    if escolha not in nomes:
        raise ValueError('Modelo inválido: ' + escolha)
    return escolha


def escrever_atomico(destino, conteudo):
    """Substitui o arquivo somente depois de terminar a escrita."""
    temporario = None
    try:
        with tempfile.NamedTemporaryFile(dir=destino.parent, delete=False) as arquivo:
            temporario = Path(arquivo.name)
            arquivo.write(conteudo)
        temporario.replace(destino)
    finally:
        if temporario is not None:
            temporario.unlink(missing_ok=True)


def aplicar_template(origem, destino, backup):
    """Copia config/CSS; cores e modelos originais permanecem no lugar."""
    novos = {nome: (origem / nome).read_bytes() for nome in ARQUIVOS}
    json.loads(novos['config'])  # Falha antes de alterar arquivos se o JSON for inválido.
    antigos = {nome: (destino / nome).read_bytes() for nome in ARQUIVOS}
    if not (destino / 'colors.css').is_file():
        raise ValueError('Paleta colors.css ausente na Waybar ativa.')

    # O primeiro backup fica guardado para permitir voltar à barra original.
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=backup.parent) as pasta:
            copia = Path(pasta) / 'original'
            copia.mkdir()
            for nome, conteudo in antigos.items():
                (copia / nome).write_bytes(conteudo)
            copia.rename(backup)

    try:
        for nome, conteudo in novos.items():
            escrever_atomico(destino / nome, conteudo)
    except OSError:
        for nome, conteudo in antigos.items():
            escrever_atomico(destino / nome, conteudo)
        raise


def recarregar_waybar():
    resultado = subprocess.run(['pkill', '-USR2', '-u', str(os.getuid()), '-x', 'waybar'])
    if resultado.returncode == 1:
        print('Modelo salvo. A Waybar não está em execução; será usado na próxima inicialização.')
    else:
        resultado.check_returncode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    opcoes = parser.add_mutually_exclusive_group()
    opcoes.add_argument('--template', help='Aplica um modelo pelo nome, sem abrir o Rofi.')
    opcoes.add_argument('--restore', action='store_true', help='Restaura a barra anterior à primeira troca.')
    opcoes.add_argument('--list', action='store_true', help='Lista modelos sem aplicar.')
    args = parser.parse_args()

    # 1. Descobrir os modelos disponíveis.
    nomes = listar_templates(TEMPLATES_DIR)
    if args.list:
        print('\n'.join(nomes))
        return

    # 2. Impedir duas trocas ao mesmo tempo.
    STATE.mkdir(parents=True, exist_ok=True)
    with (STATE / 'lock').open('w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print('Já existe uma troca de Waybar em andamento.')
            return

        # 3. Escolher a origem: backup, argumento ou seletor.
        backup = STATE / 'original'
        if args.restore:
            origem = backup
        else:
            if not nomes:
                raise ValueError('Nenhum modelo encontrado em ' + str(TEMPLATES_DIR))
            nome = args.template or escolher_template(nomes)
            if nome is None:
                return
            if nome not in nomes:
                raise ValueError('Modelo desconhecido: ' + nome)
            origem = TEMPLATES_DIR / nome

        # 4. Salvar o modelo e solicitar a atualização da barra.
        aplicar_template(origem, CONFIG, backup)
        recarregar_waybar()
        print('Waybar atualizada: ' + origem.name)


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, subprocess.SubprocessError) as erro:
        raise SystemExit('Não foi possível trocar a Waybar: ' + str(erro))
