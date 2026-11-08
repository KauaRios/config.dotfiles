#!/usr/bin/env python3
"""Escolha explícita de wallpaper e paleta escura; sem troca aleatória."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import re
import subprocess as sp
import tempfile

CONFIG = Path(os.environ.get('XDG_CONFIG_HOME') or Path.home() / '.config')
STATE = Path(os.environ.get('XDG_STATE_HOME') or Path.home() / '.local/state') / 'dotfiles-wallpaper'
DEFAULT = 'anime-girl-white-hair-background-hd-wallpaper-uhdpaper.com-763@5@t.jpg'


def run(*args, **kwargs):
    return sp.run(args, check=True, text=True, **kwargs)


def palette(image):
    try:
        result = run('matugen', 'image', str(image), '--dry-run', '--json', 'hex',
                     '-m', 'dark', '--source-color-index', '0', capture_output=True)
    except sp.CalledProcessError as error:
        raise RuntimeError('Matugen: ' + (error.stderr or error.stdout or str(error)).strip()) from error
    data = json.loads(result.stdout)['colors']
    keys = ('surface', 'on_surface', 'primary', 'secondary', 'outline')
    colors = {}
    for key in keys:
        value = data['dark'][key] if 'dark' in data else data[key]['dark']
        colors[key] = value['color'] if isinstance(value, dict) else value
        if not re.fullmatch(r'#[0-9a-fA-F]{6}', colors[key]):
            raise ValueError('Cor inválida: ' + key)
    return {key: colors[key] for key in keys}


def choose(folder):
    images = []
    for path in folder.rglob('*'):
        if not path.is_file() or path.suffix.lower() not in ('.png', '.jpg', '.jpeg', '.webp'):
            continue
        # Esses caracteres separam linhas/campos no protocolo de entrada do Rofi.
        if any(char in str(path) for char in ('\n', '\r', '\x1f')):
            continue
        images.append(path)
    images = sorted(images)
    if not images:
        raise ValueError('Nenhuma imagem na pasta ' + str(folder))
    # thumbnail:// solicita o gerador de miniaturas do sistema, com cache do Rofi.
    entries = []
    for image in images:
        name = str(image.relative_to(folder))
        entries.append(name + '\0icon\x1fthumbnail://' + str(image.resolve()))
    theme = CONFIG / 'rofi/wallpapers.rasi'
    # A lista inteira deve estar pronta antes de abrir a galeria.
    result = sp.run(
        ['rofi', '-no-config', '-dmenu', '-sync', '-i', '-no-custom', '-format', 'i',
         '-show-icons', '-theme', str(theme)],
        input='\n'.join(entries), text=True, capture_output=True,
    )
    if result.stderr:
        print(result.stderr.strip())
    if result.returncode == 1:
        return None
    result.check_returncode()
    index = int(result.stdout.strip())
    if not 0 <= index < len(images):
        raise ValueError('Seleção inválida')
    return images[index].resolve()


def atomic(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', dir=path.parent, delete=False) as f:
        f.write(text)
        temp = f.name
    os.replace(temp, path)


def apply(image, colors):
    if not image.is_file():
        raise ValueError('Imagem não encontrada: ' + str(image))
    # Valida a inicialização antes de encerrar instâncias anteriores.
    old = sp.run(['pgrep', '-u', str(os.getuid()), '-x', 'swaybg'], capture_output=True, text=True)
    process = sp.Popen(['swaybg', '-i', str(image), '-m', 'fill'], start_new_session=True,
                       stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    try:
        process.wait(timeout=0.4)
        raise RuntimeError('swaybg encerrou antes de aplicar a imagem')
    except sp.TimeoutExpired:
        pass
    for pid in old.stdout.split():
        try:
            os.kill(int(pid), 15)
        except ProcessLookupError:
            pass
    if colors:
        template_dir = Path(__file__).resolve().parent / 'theme-templates'
        for source, dest in [('waybar.css', 'waybar/colors.css'), ('rofi.rasi', 'rofi/colors.rasi'), ('mako.conf', 'mako/config'), ('hypr.lua', 'hypr/lua/colors.lua')]:
            text = (template_dir / source).read_text()
            for key, value in colors.items():
                text = text.replace('@' + key + '@', value).replace('@' + key + '_rgb@', value[1:])
            atomic(CONFIG / dest, text)
    atomic(STATE / 'selection.json', json.dumps({'image': str(image), 'colors': colors}))
    for command in [('hyprctl', 'reload'), ('pkill', '-USR2', '-u', str(os.getuid()), '-x', 'waybar'), ('makoctl', 'reload')]:
        result = sp.run(command, capture_output=True, text=True)
        if result.returncode:
            print('Recarregamento pendente:', ' '.join(command), result.stderr.strip())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--restore', action='store_true')
    parser.add_argument('--image', type=Path)
    args = parser.parse_args()
    STATE.mkdir(parents=True, exist_ok=True)
    with (STATE / 'lock').open('w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return
        if args.restore:
            saved = STATE / 'selection.json'
            data = json.loads(saved.read_text()) if saved.exists() else {}
            image = Path(data.get('image', CONFIG / 'wallpapers' / DEFAULT))
            if not image.is_file():
                image = CONFIG / 'wallpapers' / DEFAULT
            apply(image, data.get('colors'))
        else:
            image = args.image.expanduser().resolve() if args.image else choose(CONFIG / 'wallpapers')
            if image is not None:
                if not image.is_file():
                    raise ValueError('Imagem não encontrada: ' + str(image))
                apply(image, palette(image))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, RuntimeError, sp.SubprocessError) as error:
        print('Wallpaper:', error)
        sp.run(['notify-send', 'Wallpaper', str(error)], check=False)
        raise SystemExit(1)
