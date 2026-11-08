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

    def test_gallery_sends_thumbnail_paths_and_keeps_index_selection(self):
        """Miniaturas usam caminho absoluto; nomes repetidos em subpastas continuam distintos."""
        with tempfile.TemporaryDirectory(prefix='gallery test ') as d:
            folder = Path(d)
            (folder / 'a').mkdir(); (folder / 'b').mkdir()
            first = folder / 'a/foto bonita.jpg'; second = folder / 'b/foto bonita.jpg'
            first.touch(); second.touch()
            with patch.object(w.sp, 'run', return_value=subprocess.CompletedProcess([], 0, '1\n', '')) as run:
                self.assertEqual(w.choose(folder), second.resolve())
            command = run.call_args.args[0]
            self.assertIn('-show-icons', command)
            self.assertIn(str(w.CONFIG / 'rofi/wallpapers.rasi'), command)
            self.assertEqual(run.call_args.kwargs['input'],
                             'a/foto bonita.jpg\0icon\x1fthumbnail://' + str(first.resolve()) + '\n' +
                             'b/foto bonita.jpg\0icon\x1fthumbnail://' + str(second.resolve()))

    def test_gallery_ignores_control_characters_in_names(self):
        """Nomes não podem injetar outra linha ou campo no protocolo do Rofi."""
        with tempfile.TemporaryDirectory() as d:
            folder = Path(d)
            good = folder / 'safe.jpg'; good.touch()
            (folder / 'bad\x1fname.jpg').touch()
            (folder / 'bad\nname.jpg').touch()
            with patch.object(w.sp, 'run', return_value=subprocess.CompletedProcess([], 0, '0\n', '')) as run:
                self.assertEqual(w.choose(folder), good.resolve())
            self.assertEqual(run.call_args.kwargs['input'], 'safe.jpg\0icon\x1fthumbnail://' + str(good.resolve()))

    def test_gallery_theme_parses(self):
        """O Rofi real valida o tema; não abre a galeria nem comprova renderização das imagens."""
        import shutil
        if not shutil.which('rofi'):
            self.skipTest('Rofi não instalado')
        theme = Path(__file__).resolve().parents[1] / 'rofi/wallpapers.rasi'
        subprocess.run(['rofi', '-no-config', '-theme', str(theme), '-dump-theme'],
                       check=True, capture_output=True, text=True, timeout=10)
