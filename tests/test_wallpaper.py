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
            with patch.object(w.sp, 'run', return_value=subprocess.CompletedProcess([], 0, 'anime girl.jpg\n', '')):
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

    def test_real_matugen_without_terminal(self):
        import shutil
        if not shutil.which('matugen'):
            self.skipTest('Matugen não instalado')
        root = Path(__file__).resolve().parents[1]
        images = list((root / 'wallpapers').glob('*.jpg')) + list((root / 'wallpapers').glob('*.jpeg'))
        self.assertTrue(images)
        for image in images:
            with self.subTest(image=image.name):
                colors = w.palette(image)
                self.assertEqual(set(colors), {'surface', 'on_surface', 'primary', 'secondary', 'outline'})
                for color in colors.values():
                    self.assertRegex(color, r'^#[0-9a-fA-F]{6}$')

    def test_matugen_error_preserves_diagnostic(self):
        with patch.object(w, 'run', side_effect=subprocess.CalledProcessError(1, 'matugen', stderr='source color missing')):
            with self.assertRaisesRegex(RuntimeError, 'source color missing'):
                w.palette(Path('test.jpg'))

    def test_current_json_format(self):
        colors = {key: {'dark': {'color': '#123456'}} for key in ('surface', 'on_surface', 'primary', 'secondary', 'outline')}
        with patch.object(w, 'run', return_value=subprocess.CompletedProcess([], 0, json.dumps({'colors': colors}), '')):
            self.assertEqual(w.palette(Path('test.jpg'))['primary'], '#123456')

    def test_wofi_rejects_unknown_selection(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d, 'girl.jpg').touch()
            with patch.object(w.sp, 'run', return_value=subprocess.CompletedProcess([], 0, '../other.jpg\n', '')):
                with self.assertRaises(ValueError):
                    w.choose(Path(d))

    def test_wofi_css_parses(self):
        try:
            import gi
            gi.require_version('Gtk', '3.0')
            from gi.repository import Gtk
        except (ImportError, ValueError):
            self.skipTest('GTK 3 indisponível')
        Gtk.CssProvider().load_from_path(str(Path(__file__).resolve().parents[1] / 'wofi/style.css'))
