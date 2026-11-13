"""Conversão e execução do visualizador, sem capturar áudio da sessão."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'hypr/scripts/waybar-templetes/kasumi/assets/kasumi-cava.py'
spec = importlib.util.spec_from_file_location('kasumi_cava', SCRIPT)
cava = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cava)


class KasumiCavaTests(unittest.TestCase):
    def test_silence_and_changing_amplitudes(self):
        """Silêncio e amplitudes diferentes produzem alturas correspondentes."""
        self.assertEqual(cava.frame('0;0;0;0;\n'), '▁▁▁▁')
        self.assertEqual(cava.frame('0;2;4;7;\n'), '▁▃▅█')

    def test_invalid_frames_are_rejected(self):
        """Valores fora da escala ou quadros incompletos não viram barras falsas."""
        for line in ('1;2;', '0;0;0;8;', '-1;0;0;0;', 'erro'):
            with self.subTest(line=line), self.assertRaises(ValueError):
                cava.frame(line)

    def test_cava_stream_becomes_waybar_json(self):
        """Um executável CAVA simulado envia silêncio e som pelo pipe real."""
        with tempfile.TemporaryDirectory() as folder:
            executable = Path(folder) / 'cava'
            executable.write_text('#!/bin/sh\nprintf "0;0;0;0;\\n0;2;4;7;\\n"\n')
            executable.chmod(0o755)
            result = subprocess.run(
                [os.sys.executable, str(SCRIPT)],
                env={**os.environ, 'PATH': folder}, capture_output=True,
                text=True, check=True, timeout=5,
            )
            frames = [json.loads(line) for line in result.stdout.splitlines()]
            self.assertEqual([f['text'] for f in frames], ['▁▁▁▁', '▁▃▅█'])
            self.assertEqual([f['class'] for f in frames], ['silent', 'playing'])

    def test_missing_cava_has_visible_diagnostic(self):
        """Dependência ausente mostra aviso em vez de simular animação."""
        with tempfile.TemporaryDirectory() as folder:
            result = subprocess.run([os.sys.executable, str(SCRIPT)],
                                    env={**os.environ, 'PATH': folder},
                                    capture_output=True, text=True, check=True, timeout=5)
            self.assertEqual(json.loads(result.stdout)['class'], 'error')
