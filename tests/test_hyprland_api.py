"""Validação da configuração pelo próprio Hyprland, sem iniciar o compositor."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class HyprlandApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.binary = shutil.which('Hyprland')
        if not cls.binary:
            raise unittest.SkipTest('Instale Hyprland para validar a API real.')
        help_result = subprocess.run([cls.binary, '--help'], capture_output=True,
                                     text=True, timeout=10)
        if help_result.returncode:
            raise RuntimeError(help_result.stdout + help_result.stderr)
        if '--verify-config' not in help_result.stdout + help_result.stderr:
            raise unittest.SkipTest('Esta versão do Hyprland não oferece --verify-config.')

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='hyprland api test ')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        config = self.base / 'config'
        # Ajustes pessoais não fazem parte da configuração base versionada.
        shutil.copytree(ROOT / 'hypr', config / 'hypr',
                        ignore=shutil.ignore_patterns('local.lua', '__pycache__'))
        self.config = config / 'hypr/hyprland.lua'
        runtime = self.base / 'runtime'
        runtime.mkdir(mode=0o700)
        self.env = dict(os.environ, HOME=str(self.base), XDG_CONFIG_HOME=str(config),
                        XDG_STATE_HOME=str(self.base / 'state'),
                        XDG_CACHE_HOME=str(self.base / 'cache'),
                        XDG_DATA_HOME=str(self.base / 'data'), XDG_RUNTIME_DIR=str(runtime))
        for key in ('WAYLAND_DISPLAY', 'DISPLAY', 'HYPRLAND_INSTANCE_SIGNATURE',
                    'DBUS_SESSION_BUS_ADDRESS'):
            self.env.pop(key, None)

    def verify(self, extra=''):
        with self.config.open('a') as config:
            config.write('\n' + extra + '\n')
        result = subprocess.run([self.binary, '--verify-config', '--config', str(self.config)],
                                env=self.env, cwd=self.base, capture_output=True,
                                text=True, timeout=20)
        return result, result.stdout + result.stderr

    def test_repository_config_matches_installed_api(self):
        result, output = self.verify()
        self.assertEqual(result.returncode, 0, output)
        self.assertIn('config ok', output.lower(), output)

    def test_unknown_option_is_rejected(self):
        result, output = self.verify(
            'hl.config({ general = { dotfiles_test_invalid_option = true } })')
        self.assertNotEqual(result.returncode, 0, output)
        self.assertIn('general.dotfiles_test_invalid_option', output, output)
        self.assertIn('unknown config key', output.lower(), output)

    def test_unknown_lua_api_call_is_rejected(self):
        result, output = self.verify('hl.dotfiles_test_missing_function()')
        self.assertNotEqual(result.returncode, 0, output)
        self.assertIn('dotfiles_test_missing_function', output, output)
        self.assertIn('nil', output.lower(), output)
