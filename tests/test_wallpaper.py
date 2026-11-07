import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('wallpaper', Path(__file__).resolve().parents[1] / 'hypr/scripts/wallpaper.py')
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)

class WallpaperTests(unittest.TestCase):
    def test_cancel_does_not_select_image(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d, 'girl.jpg').touch()
            with patch.object(w.sp, 'run', return_value=subprocess.CompletedProcess([], 1, '', '')):
                self.assertIsNone(w.choose(Path(d)))

    def test_selection_preserves_spaces(self):
        with tempfile.TemporaryDirectory() as d:
            image = Path(d, 'anime girl.jpg')
            image.touch()
            with patch.object(w.sp, 'run', return_value=subprocess.CompletedProcess([], 0, '0\n', '')):
                self.assertEqual(w.choose(Path(d)), image)

    def test_invalid_color_rejected(self):
        colors = dict.fromkeys(('surface', 'on_surface', 'primary', 'secondary', 'outline'), '#123456')
        colors['primary'] = 'invalid'
        with patch.object(w, 'run', return_value=subprocess.CompletedProcess([], 0, json.dumps({'colors': {'dark': colors}}), '')):
            with self.assertRaises(ValueError):
                w.palette(Path('test.jpg'))

    def test_generation_failure_prevents_apply(self):
        with tempfile.TemporaryDirectory() as d:
            image = Path(d, 'image.jpg'); image.touch()
            with patch.object(w, 'STATE', Path(d)), patch('sys.argv', ['wallpaper', '--image', str(image)]), patch.object(w, 'palette', side_effect=ValueError('failed')), patch.object(w, 'apply') as apply:
                with self.assertRaises(ValueError):
                    w.main()
                apply.assert_not_called()

    def test_restore_does_not_require_matugen(self):
        with tempfile.TemporaryDirectory() as d:
            image = Path(d, 'image.jpg'); image.touch()
            Path(d, 'selection.json').write_text(json.dumps({'image': str(image), 'colors': None}))
            with patch.object(w, 'STATE', Path(d)), patch('sys.argv', ['wallpaper', '--restore']), patch.object(w, 'palette') as palette, patch.object(w, 'apply') as apply:
                w.main()
                palette.assert_not_called()
                apply.assert_called_once_with(image, None)
