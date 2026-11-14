"""Valida os novos modelos sem abrir a barra ou tocar na configuração ativa."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / 'hypr/scripts/waybar-templetes'

class NewWaybarTests(unittest.TestCase):
    def test_configs_and_palette_links(self):
        """Módulos exibidos têm configuração e a paleta aponta para a Waybar compartilhada."""
        for name in ('graphite', 'sora'):
            with self.subTest(model=name):
                folder = ROOT / name
                data = json.loads((folder / 'config').read_text())
                modules = sum((data[k] for k in ('modules-left', 'modules-center', 'modules-right')), [])
                for module in modules:
                    self.assertIn(module, data)
                    if module.startswith('group/'):
                        for child in data[module]['modules']:
                            self.assertIn(child, data)
                self.assertEqual((folder / 'colors.css').resolve(), ROOT.parents[2] / 'waybar/colors.css')

    def test_css_accepted_by_gtk(self):
        """GTK analisa também o import de cores; não avalia o resultado visual."""
        try:
            import gi
            gi.require_version('Gtk', '3.0')
            from gi.repository import Gtk
        except (ImportError, ValueError):
            self.skipTest('GTK/PyGObject indisponível')
        for name in ('graphite', 'sora'):
            with self.subTest(model=name):
                Gtk.CssProvider().load_from_path(str(ROOT / name / 'style.css'))

    def test_spectrum_accepts_twenty_bands_and_rejects_bad_frames(self):
        """Confere silêncio, pico e quadros truncados/inválidos sem acessar áudio real."""
        spec = importlib.util.spec_from_file_location('spectrum', ROOT / 'graphite/assets/graphite-spectrum.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.frame('0;' * 20), '▁' * 20)
        self.assertEqual(module.frame('7;' * 20), '█' * 20)
        for bad in ('0;' * 19, '8;' * 20, '-1;' * 20, 'x;' * 20):
            with self.assertRaises(ValueError):
                module.frame(bad)

    def test_sora_icons_survive_template_copy(self):
        """Carrega os SVG reais e valida CSS/assets após copiar para outro diretório."""
        import tempfile
        import re
        from test_waybar_templates import w
        try:
            import gi
            gi.require_version('Gtk', '3.0')
            gi.require_version('Rsvg', '2.0')
            from gi.repository import Gtk, Rsvg
        except (ImportError, ValueError):
            self.skipTest('GTK/PyGObject indisponível')
        with tempfile.TemporaryDirectory() as folder:
            active = Path(folder) / 'active'
            active.mkdir()
            (active / 'config').write_text('{}')
            (active / 'style.css').write_text('')
            palette = (ROOT / 'sora/colors.css').read_text()
            (active / 'colors.css').write_text(palette)
            w.aplicar_template(ROOT / 'sora', active, Path(folder) / 'backup')
            style = (active / 'style.css').read_text()
            icons = re.findall(r'url\("([^\"]+)"\)', style)
            self.assertTrue(icons)
            for filename in icons:
                with self.subTest(icon=filename):
                    icon = Rsvg.Handle.new_from_file(str(active / filename)).get_pixbuf()
                    self.assertGreater(icon.get_width(), 0)
                    self.assertTrue(icon.get_has_alpha())
            Gtk.CssProvider().load_from_path(str(active / 'style.css'))
            self.assertEqual((active / 'colors.css').read_text(), palette)
