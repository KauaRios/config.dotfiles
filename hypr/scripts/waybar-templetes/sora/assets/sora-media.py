#!/usr/bin/env python3
"""Título do player, com estado vazio estável e texto escapado para o Waybar."""
import html
import json
import subprocess


def current_media():
    try:
        result = subprocess.run(['playerctl', 'metadata', '--format', '{{title}}'],
                                capture_output=True, text=True, timeout=2)
        title = result.stdout.strip() if result.returncode == 0 else ''
    except (OSError, subprocess.TimeoutExpired):
        title = ''
    if not title:
        return {'text': '▪ Nothing playing right now', 'tooltip': 'Clique direito: abrir Spotify', 'class': 'idle'}
    short = title if len(title) <= 27 else title[:26] + '…'
    return {'text': '▪ ' + html.escape(short), 'tooltip': html.escape(title), 'class': 'playing'}


if __name__ == '__main__':
    print(json.dumps(current_media()))
