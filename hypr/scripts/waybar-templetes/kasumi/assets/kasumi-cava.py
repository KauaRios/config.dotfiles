#!/usr/bin/env python3
"""Converte quatro bandas do CAVA em barras para o módulo custom da Waybar."""
import json
from pathlib import Path
import signal
import subprocess

LEVELS = '▁▂▃▄▅▆▇█'


def frame(line):
    values = [int(value) for value in line.strip().split(';') if value]
    if len(values) != 4 or any(value < 0 or value > 7 for value in values):
        raise ValueError('Quadro CAVA inválido')
    return ''.join(LEVELS[value] for value in values)


def emit(text, tooltip, state):
    print(json.dumps({'text': text, 'tooltip': tooltip, 'class': state}), flush=True)


def main():
    def stop(signum, current_frame):
        raise SystemExit(0)
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    try:
        process = subprocess.Popen(
            ['cava', '-p', str(Path(__file__).with_name('kasumi-cava.conf'))],
            stdout=subprocess.PIPE, text=True,
        )
    except FileNotFoundError:
        emit('!', 'Instale cava para ativar o visualizador de áudio.', 'error')
        return
    try:
        for line in process.stdout:
            try:
                bars = frame(line)
            except ValueError:
                continue
            emit(bars, 'Áudio da saída padrão', 'silent' if bars == '▁▁▁▁' else 'playing')
        if process.wait() != 0:
            emit('!', 'CAVA falhou. Confira a saída de áudio e o log da Waybar.', 'error')
    except BrokenPipeError:
        pass
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        process.stdout.close()


if __name__ == '__main__':
    main()
