#!/usr/bin/env python3
"""Mantém um componente por instância Hyprland, sem sobreviver à sessão."""
import fcntl
import os
from pathlib import Path
import subprocess
import sys
import time


def supervise(command, alive, delay=3):
    while alive():
        result = subprocess.run(command, check=False)
        print(f'{command[0]} encerrou com código {result.returncode}', flush=True)
        if alive():
            time.sleep(delay)


def main():
    name = sys.argv[1]
    if name not in ('waybar', 'mako', 'swaybg'):
        raise SystemExit('Componente inválido')
    runtime = Path(os.environ['XDG_RUNTIME_DIR'])
    instance = os.environ['HYPRLAND_INSTANCE_SIGNATURE']
    socket = runtime / 'hypr' / instance / '.socket.sock'
    lockpath = runtime / f'dotfiles-{instance}-{name}.lock'
    with lockpath.open('w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return
        config = Path(os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config')))
        command = [name]
        if name == 'swaybg':
            command += ['-i', str(config / 'wallpapers/cool-japanese-samurai-backiee-4K.jpg'), '-m', 'fill']
        def alive():
            if not socket.exists():
                return False
            try:
                return subprocess.run(['hyprctl', 'version'], stdout=subprocess.DEVNULL,
                                      stderr=subprocess.DEVNULL, timeout=5).returncode == 0
            except subprocess.TimeoutExpired:
                return False
        supervise(command, alive)


if __name__ == '__main__':
    main()
