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
        """Executável falso confere -p e envia quadros; o adaptador gera JSON real."""
        with tempfile.TemporaryDirectory() as folder:
            executable = Path(folder) / 'cava'
            executable.write_text('#!/bin/sh\n[ "$1" = "-p" ] && [ -f "$2" ] || exit 1\nprintf "0;0;0;0;\\n0;2;4;7;\\n"\n')
            executable.chmod(0o755)
            result = subprocess.run([os.sys.executable, str(MODEL / 'assets/pacman-cava.py')],
                                    env={**os.environ, 'PATH': folder}, capture_output=True,
                                    text=True, check=True, timeout=5)
            frames = [json.loads(line) for line in result.stdout.splitlines()]
            self.assertEqual([f['text'] for f in frames], ['▁▁▁▁', '▁▃▅█'])
            self.assertEqual([f['class'] for f in frames], ['silent', 'playing'])
