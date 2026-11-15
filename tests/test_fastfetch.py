"""Cores geradas e compatibilidade da configuração com o Fastfetch instalado."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from test_wallpaper import w


class FastfetchTests(unittest.TestCase):
    def test_wallpaper_palette_updates_config_and_preserves_text_logo(self):
        """Duas paletas atualizam a máscara e os blocos, preservando o logo textual."""
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(w, 'CONFIG', Path(folder)):
                for primary in ('#123456', '#abcdef'):
                    colors = dict(surface='#101010', on_surface='#eeeeee', primary=primary,
                                  secondary='#fedcba', outline='#888888')
                    w.apply_colors(colors)
                    path = Path(folder, 'fastfetch/config.jsonc')
                    text = path.read_text()
                    config = json.loads(text)
                    self.assertEqual(config['logo']['color']['1'], primary)
                    self.assertEqual(config['display']['color']['output'], '#eeeeee')
                    self.assertIn('ronin.txt', config['logo']['source'])
                    self.assertEqual(config['logo']['type'], 'file')
                    ansi = ';'.join(str(int(primary[i:i+2], 16)) for i in (1, 3, 5))
                    self.assertIn('38;2;' + ansi, text)
                    self.assertNotIn('@primary', text)
                if shutil.which('fastfetch'):
                    result = subprocess.run(['fastfetch', '--config', str(path), '--logo', 'none',
                                             '--pipe', 'true'], capture_output=True, text=True, timeout=20,
                                             env={**os.environ, 'GSETTINGS_BACKEND': 'memory'})
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn('SYSTEM', result.stdout)
                    self.assertIn('SOFTWARE', result.stdout)
                    self.assertIn('HARDWARE', result.stdout)
