#!/usr/bin/env python3
"""Espectro espelhado: graves no centro, agudos nas pontas e queda suave."""
import json
from pathlib import Path
import signal
import subprocess

LEVELS = '▁▂▃▄▅▆▇█'


def frame(line, previous):
    """Lê seis bandas e devolve o desenho e as alturas para o próximo quadro."""
    values = [int(value) for value in line.strip().split(';') if value]
    if len(values) != 6 or any(value < 0 or value > 7 for value in values):
        raise ValueError('Quadro CAVA inválido')
    # Sobe com a batida e desce no máximo um nível por quadro (24 fps).
    levels = [max(value, old - 1) for value, old in zip(values, previous)]
    if not any(levels):
        return '·' * 12, levels
    # O CAVA entrega graves primeiro: espelhar coloca os graves no centro.
    mirrored = list(reversed(levels)) + levels
    return ''.join(LEVELS[value] for value in mirrored), levels


def emit(text, tooltip, state):
    print(json.dumps({'text': text, 'tooltip': tooltip, 'class': state}), flush=True)


def main():
    def stop(signum, current_frame):
        raise SystemExit(0)
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    try:
        process = subprocess.Popen(
            ['cava', '-p', str(Path(__file__).with_name('pacman-cava.conf'))],
            stdout=subprocess.PIPE, text=True,
        )
    except FileNotFoundError:
        emit('!', 'Instale cava para ativar o visualizador de áudio.', 'error')
        return
    try:
        previous = [0] * 6
        for line in process.stdout:
            try:
                bars, previous = frame(line, previous)
            except ValueError:
                continue
            emit(bars, 'Espectro espelhado · graves ao centro',
                 'playing' if any(previous) else 'silent')
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
