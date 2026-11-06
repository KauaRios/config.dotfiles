"""Testes locais: nenhum pacote é instalado e a .config real não é utilizada."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = ('hypr', 'waybar', 'rofi', 'wofi', 'mako', 'wallpapers', 'qt6ct')


class ConfigTests(unittest.TestCase):
    def test_empty_xdg_config_uses_home(self):
        lua = shutil.which('lua')
        if not lua:
            self.skipTest('Instale lua para verificar os caminhos.')
        harness = '''
require = function() end
io.open = function(path)
    assert(path == os.getenv("HOME") .. "/.config/hypr/local.lua", path)
end
dofile(arg[1])
assert(package.path:find(os.getenv("HOME") .. "/.config/hypr/?.lua;", 1, true) == 1)
'''
        subprocess.run([lua, '-', str(ROOT / 'hypr/hyprland.lua')],
                       input=harness, text=True, capture_output=True, check=True,
                       env=dict(os.environ, HOME='/tmp/dotfiles-test-home', XDG_CONFIG_HOME=''),
                       timeout=10)

    def test_autostart_waits_for_hyprland_start(self):
        lua = shutil.which('lua')
        if not lua:
            self.skipTest('Instale lua para verificar o evento de inicialização.')
        harness = '''
local callback
local commands = {}
hl = {
    on = function(event, fn)
        assert(event == "hyprland.start")
        callback = fn
    end,
    exec_cmd = function(command) table.insert(commands, command) end,
}
dofile(arg[1])
assert(#commands == 0, "Aplicativos iniciados antes do evento")
assert(callback, "Evento de inicialização ausente")
callback()
local bar, wallpaper = false, false
for _, command in ipairs(commands) do
    bar = bar or command == "waybar"
    wallpaper = wallpaper or command:match("^swaybg ") ~= nil
    if command:match("^pgrep ") then print(command) end
end
assert(bar and wallpaper, "Barra ou wallpaper ausente")
'''
        result = subprocess.run([lua, '-', str(ROOT / 'hypr/lua/autostart.lua')],
                                input=harness, text=True, capture_output=True, check=True, timeout=10)
        self.assertTrue(result.stdout.strip(), 'Verificação do mako ausente')
        # Simula um usuário diferente: não depende de UID exportado pelo shell.
        shell = '''
id() { printf '12345\\n'; }
pgrep() { [ "$1" = -u ] && [ "$2" = 12345 ] && [ "$3" = -x ] && [ "$4" = mako ]; }
mako() { exit 99; }
'''
        subprocess.run(['/bin/sh', '-c', shell + result.stdout],
                       check=True, capture_output=True, timeout=10)

    def test_rofi_theme_parses(self):
        if not shutil.which('rofi'):
            self.skipTest('Instale rofi para verificar o tema.')
        subprocess.run(['rofi', '-dump-theme', '-config', str(ROOT / 'rofi/config.rasi')],
                       check=True, capture_output=True, timeout=10)

    def test_bash_syntax(self):
        for script in ROOT.rglob('*.sh'):
            if '.git' not in script.parts:
                with self.subTest(script=script.relative_to(ROOT)):
                    subprocess.run(['bash', '-n', str(script)], check=True, capture_output=True)

    def test_waybar_modules_have_configuration(self):
        config = json.loads((ROOT / 'waybar/config').read_text())
        for side in ('left', 'center', 'right'):
            for module in config[f'modules-{side}']:
                self.assertIn(module, config)

    def test_lua_module_references_exist(self):
        for script in (ROOT / 'hypr').rglob('*.lua'):
            for name in re.findall(r'require\("(lua\.[^"]+)"\)', script.read_text()):
                self.assertTrue((ROOT / 'hypr' / (name.replace('.', '/') + '.lua')).is_file(), name)

    def test_lua_syntax(self):
        compiler = next((shutil.which(name) for name in ('luac', 'luac5.4', 'luac5.5')
                         if shutil.which(name)), None)
        if not compiler:
            self.skipTest('Instale lua (luac) para verificar a sintaxe Lua.')
        for script in (ROOT / 'hypr').rglob('*.lua'):
            with self.subTest(script=script.relative_to(ROOT)):
                subprocess.run([compiler, '-p', str(script)], check=True, capture_output=True)


class HyprlandSessionTests(unittest.TestCase):
    def test_configerrors(self):
        if not os.environ.get('HYPRLAND_INSTANCE_SIGNATURE') or not shutil.which('hyprctl'):
            self.skipTest('Sessão Hyprland ou hyprctl indisponível.')
        result = subprocess.run(['hyprctl', 'configerrors'], capture_output=True, text=True, timeout=10)
        if result.returncode:
            self.skipTest('Não foi possível acessar a sessão Hyprland: ' +
                          (result.stderr.strip() or result.stdout.strip() or 'erro desconhecido'))
        self.assertIn(result.stdout.strip().lower(), ('ok', ''), result.stdout)


@unittest.skipIf(os.geteuid() == 0, 'Execute sem sudo: o instalador rejeita root.')
class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='dotfiles test ')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.config = self.base / 'home/.config'
        self.config.mkdir(parents=True)
        # Copiar permite testar nome/caminho arbitrário e mover a origem sem tocar no repo.
        self.repo = self.base / 'projects/config.dotfiles'
        self.repo.mkdir(parents=True)
        shutil.copy2(ROOT / 'install.sh', self.repo / 'install.sh')
        for folder in FOLDERS:
            (self.repo / folder).mkdir()
        self.env = dict(os.environ, HOME=str(self.config.parent), XDG_CONFIG_HOME=str(self.config))

    def install(self, *args, ok=True):
        result = subprocess.run(['bash', str(self.repo / 'install.sh'), *args],
                                env=self.env, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode == 0, ok, result.stdout + result.stderr)
        return result

    def test_links_and_kde_preserved(self):
        kde = self.config / 'kdeglobals'
        kde.write_bytes(b'[General]\nColorScheme=BreezeDark\n')
        self.install()
        self.assertEqual(kde.read_bytes(), b'[General]\nColorScheme=BreezeDark\n')
        self.assertFalse(self.config.is_symlink())
        for folder in FOLDERS:
            self.assertTrue((self.config / folder).is_symlink())
            self.assertEqual((self.config / folder).resolve(), self.repo / folder)

    def test_existing_config_backed_up(self):
        (self.config / 'hypr').mkdir()
        (self.config / 'hypr/old.conf').write_text('keep me')
        self.install()
        backups = list(self.config.glob('dot-backup.*'))
        self.assertEqual(len(backups), 1)
        self.assertEqual((backups[0] / 'hypr/old.conf').read_text(), 'keep me')

    def test_second_install_keeps_same_links_without_backup(self):
        self.install()
        before = {f: (self.config / f).lstat().st_ino for f in FOLDERS}
        self.install()
        self.assertEqual(before, {f: (self.config / f).lstat().st_ino for f in FOLDERS})
        self.assertEqual(list(self.config.glob('dot-backup.*')), [])

    def test_dry_run_does_not_change_existing_config(self):
        (self.config / 'hypr').mkdir()
        (self.config / 'hypr/old.conf').write_text('keep')
        self.install('--dry-run')
        self.assertFalse((self.config / 'hypr').is_symlink())
        self.assertEqual((self.config / 'hypr/old.conf').read_text(), 'keep')
        self.assertEqual(sorted(x.name for x in self.config.iterdir()), ['hypr'])

    def test_dry_run_does_not_create_config(self):
        self.config.rmdir()
        self.install('--dry-run')
        self.assertFalse(self.config.exists())

    def test_broken_symlink_is_backed_up(self):
        missing = self.base / 'missing'
        (self.config / 'hypr').symlink_to(missing)
        self.install()
        backup = next(self.config.glob('dot-backup.*/hypr'))
        self.assertTrue(backup.is_symlink())
        self.assertEqual(backup.readlink(), missing)
        self.assertEqual((self.config / 'hypr').resolve(), self.repo / 'hypr')

    def test_moving_repo_then_reinstall_updates_links(self):
        self.install()
        moved = self.base / 'renamed dots'
        self.repo.rename(moved)
        self.repo = moved
        self.install()
        for folder in FOLDERS:
            self.assertEqual((self.config / folder).resolve(), moved / folder)

    def test_invalid_argument_does_not_write(self):
        self.install('--invalid', ok=False)
        self.assertEqual(list(self.config.iterdir()), [])

    def test_extra_arguments_do_not_write(self):
        for args in (('--dry-run', '--invalid'), ('', '--invalid')):
            with self.subTest(args=args):
                self.install(*args, ok=False)
                self.assertEqual(list(self.config.iterdir()), [])

    def test_relative_config_is_rejected(self):
        self.env['XDG_CONFIG_HOME'] = 'relative'
        self.install(ok=False)
        self.assertEqual(list(self.config.iterdir()), [])

    def test_repo_inside_destination_is_rejected(self):
        self.env['XDG_CONFIG_HOME'] = str(self.repo.parent)
        self.install(ok=False)
        self.assertTrue((self.repo / 'hypr').is_dir())
        self.assertFalse((self.repo / 'hypr').is_symlink())

    def test_missing_source_stops_before_writing(self):
        (self.repo / 'rofi').rmdir()
        self.install(ok=False)
        self.assertEqual(list(self.config.iterdir()), [])


class ScreenshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='screenshot test ')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.clipboard = self.base / 'clipboard'
        self.clipboard.write_text('previous')
        self.bin = self.base / 'bin'
        self.bin.mkdir()
        self.captures = self.base / 'captures'
        self.captures.mkdir()
        # Doubles substituem as três ferramentas: não capturam tela nem acessam clipboard.
        commands = {
            'slurp': '[[ $TEST_MODE != cancel ]] || exit 1\n[[ $TEST_MODE != empty ]] || exit 0\necho "0,0 100x100"',
            'grim': '[[ $TEST_MODE != fail ]] || exit 1\nprintf PNG > "$3"',
            'wl-copy': 'cat > "$TEST_CLIPBOARD"',
        }
        for name, body in commands.items():
            script = self.bin / name
            script.write_text('#!/bin/bash\nset -eu\n' + body + '\n')
            script.chmod(0o755)

    def capture(self, mode):
        env = dict(os.environ, PATH=str(self.bin) + ':' + os.environ['PATH'],
                   TMPDIR=str(self.captures), TEST_MODE=mode, TEST_CLIPBOARD=str(self.clipboard))
        return subprocess.run(['bash', str(ROOT / 'hypr/scripts/screenshot.sh')],
                              env=env, capture_output=True, timeout=10)

    def test_cancellation_preserves_clipboard(self):
        self.assertEqual(self.capture('cancel').returncode, 0)
        self.assertEqual(self.clipboard.read_text(), 'previous')
        self.assertEqual(list(self.captures.iterdir()), [])

    def test_empty_selection_preserves_clipboard(self):
        self.assertEqual(self.capture('empty').returncode, 0)
        self.assertEqual(self.clipboard.read_text(), 'previous')

    def test_capture_failure_preserves_clipboard_and_cleans_file(self):
        self.assertNotEqual(self.capture('fail').returncode, 0)
        self.assertEqual(self.clipboard.read_text(), 'previous')
        self.assertEqual(list(self.captures.iterdir()), [])

    def test_success_copies_image_and_cleans_file(self):
        self.assertEqual(self.capture('success').returncode, 0)
        self.assertEqual(self.clipboard.read_text(), 'PNG')
        self.assertEqual(list(self.captures.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
