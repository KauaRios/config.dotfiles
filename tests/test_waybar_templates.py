import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('waybar_picker', Path(__file__).resolve().parents[1] / 'hypr/scripts/waybar.py')
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)

class WaybarTemplateTests(unittest.TestCase):
    def test_cancel(self):
        with patch.object(w.subprocess, 'run', return_value=subprocess.CompletedProcess([], 1, '', '')):
            self.assertIsNone(w.escolher_template(['orbit']))

    def test_unknown_selection(self):
        with patch.object(w.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '../bad\n', '')):
            with self.assertRaises(ValueError):
                w.escolher_template(['orbit'])

    def test_copy_preserves_palette_and_original_backup(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); source = root/'model'; dest = root/'active'; backup = root/'backup'
            source.mkdir(); dest.mkdir()
            (source/'config').write_text('{}'); (source/'style.css').write_text('new')
            (dest/'config').write_text('{"height": 26}'); (dest/'style.css').write_text('old')
            (dest/'colors.css').write_text('palette')
            w.aplicar_template(source, dest, backup)
            w.aplicar_template(source, dest, backup)
            self.assertEqual((dest/'colors.css').read_text(), 'palette')
            self.assertEqual((source/'style.css').read_text(), 'new')
            w.aplicar_template(backup, dest, backup)
            self.assertEqual((dest/'style.css').read_text(), 'old')

    def test_invalid_json_does_not_modify_destination(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); source=root/'model'; dest=root/'active'
            source.mkdir(); dest.mkdir()
            (source/'config').write_text('invalid'); (source/'style.css').write_text('new')
            with self.assertRaises(ValueError):
                w.aplicar_template(source, dest, root/'backup')
            self.assertEqual(list(dest.iterdir()), [])
