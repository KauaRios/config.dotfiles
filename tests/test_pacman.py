"""Pacman: cópia/renderização dos assets e CAVA simulado, sem alterar a sessão."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from test_waybar_templates import w

MODEL = Path(__file__).resolve().parents[1] / 'hypr/scripts/waybar-templetes/pacman'


class PacmanTests(unittest.TestCase):
    def test_template_copy_preserves_colors_and_loads_icon(self):
        """O Pac-Man e seu CSS funcionam fora do repo sem sobrescrever a paleta ativa."""
        try:
            import gi
            gi.require_version('Gtk', '3.0')
            gi.require_version('Rsvg', '2.0')
            from gi.repository import Gtk, Rsvg
        except (ImportError, ValueError):
            self.skipTest('GTK/Rsvg indisponíveis')
        with tempfile.TemporaryDirectory() as folder:
            dest = Path(folder) / 'active'; dest.mkdir()
            (dest / 'config').write_text('{}')
            (dest / 'style.css').write_text('')
            palette = (MODEL / 'colors.css').read_text()
            (dest / 'colors.css').write_text(palette)
            w.aplicar_template(MODEL, dest, Path(folder) / 'backup')
            self.assertEqual((dest / 'colors.css').read_text(), palette)
            Gtk.CssProvider().load_from_path(str(dest / 'style.css'))
            icon = Rsvg.Handle.new_from_file(str(dest / 'assets/pacman-active-symbolic.svg')).get_pixbuf()
            self.assertTrue(icon.get_has_alpha())
            self.assertEqual(icon.get_width(), 32)
            data = json.loads((dest / 'config').read_text())
            self.assertIn('mpris', data['group/music']['modules'])
            self.assertIn('temperature', data['modules-right'])

    def test_audio_stream_uses_existing_config(self):
        """Confere espelhamento, queda suave, silêncio e rejeição de quadros inválidos."""
        import configparser
        config = configparser.ConfigParser()
        config.read(MODEL / 'assets/pacman-cava.conf')
        self.assertEqual(config.getint('general', 'bars'), 6)
        with tempfile.TemporaryDirectory() as folder:
            executable = Path(folder) / 'cava'
            samples = ['0;0;0;0;0;0;', '0;1;2;3;5;7;', 'erro', '-1;0;0;0;0;0;', '1;2;']
            samples += ['0;0;0;0;0;0;'] * 7
            executable.write_text('#!/bin/sh\n[ "$1" = "-p" ] && [ -f "$2" ] || exit 1\n' +
                                  "printf '%s\\n' '" + "' '".join(samples) + "'\n")
            executable.chmod(0o755)
            result = subprocess.run([os.sys.executable, str(MODEL / 'assets/pacman-cava.py')],
                                    env={**os.environ, 'PATH': folder}, capture_output=True,
                                    text=True, check=True, timeout=5)
            frames = [json.loads(line) for line in result.stdout.splitlines()]
            self.assertEqual(len(frames), 9)  # Os três quadros inválidos foram ignorados.
            self.assertEqual(frames[0]['text'], '·' * 12)
            self.assertEqual(frames[1]['text'], '█▆▄▃▂▁▁▂▃▄▆█')
            self.assertEqual(frames[2]['text'], '▇▅▃▂▁▁▁▁▂▃▅▇')
            self.assertEqual(frames[2]['class'], 'playing')
            self.assertEqual(frames[-1]['text'], '·' * 12)
            self.assertEqual(frames[-1]['class'], 'silent')
