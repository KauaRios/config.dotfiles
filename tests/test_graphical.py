"""Integração opt-in com um compositor real dentro de uma janela Wayland."""
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]


def stop_process(process):
    """Encerra somente o grupo criado pelo teste, inclusive filhos."""
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.wait(timeout=5)


@unittest.skipUnless(os.environ.get('DOTFILES_TEST_GUI') == '1',
                     'Testes gráficos opcionais: execute python3 tests/run.py --gui.')
class GraphicalTests(unittest.TestCase):
    def setUp(self):
        for command in ('Hyprland', 'hyprctl', 'waybar', 'dbus-run-session'):
            if not shutil.which(command):
                self.skipTest(f'Dependência gráfica ausente: {command}')
        if not os.environ.get('WAYLAND_DISPLAY') or not os.environ.get('XDG_RUNTIME_DIR'):
            self.skipTest('Uma sessão Wayland acessível é necessária para o compositor em janela.')
        check = subprocess.run([sys.executable, '-c',
                                'import gi; gi.require_version("Gtk", "3.0")'],
                               capture_output=True, text=True, timeout=10)
        if check.returncode:
            self.skipTest('Instale PyGObject e GTK 3 para o aplicativo gráfico de teste.')
        # O socket IPC inclui o hash do Hyprland: manter o caminho < 108 bytes.
        self.temp = tempfile.TemporaryDirectory(prefix='dg', dir='/tmp')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        runtime = self.base / 'r'
        runtime.mkdir(mode=0o700)
        config = self.base / 'config'
        shutil.copytree(ROOT / 'hypr', config / 'hypr',
                        ignore=shutil.ignore_patterns('local.lua', '__pycache__'))
        entry = config / 'hypr/hyprland.lua'
        # Não executar serviços pessoais nem aplicar o perfil dos monitores físicos.
        entry.write_text('''
package.preload["lua.autostart"] = function() return true end
package.preload["lua.monitors"] = function() return true end
package.preload["lua.workspaces"] = function() return true end
''' + entry.read_text() + '''
hl.monitor({ output = "", mode = "preferred", position = "auto", scale = 1 })
hl.config({ animations = { enabled = false }, misc = {
    disable_hyprland_logo = true, disable_splash_rendering = true } })
''')
        parent = Path(os.environ['XDG_RUNTIME_DIR']) / os.environ['WAYLAND_DISPLAY']
        self.env = dict(os.environ, HOME=str(self.base), XDG_CONFIG_HOME=str(config),
                        XDG_RUNTIME_DIR=str(runtime), XDG_CACHE_HOME=str(self.base / 'cache'),
                        XDG_STATE_HOME=str(self.base / 'state'), XDG_DATA_HOME=str(self.base / 'data'),
                        WAYLAND_DISPLAY=str(parent), AQ_DRM_DEVICES='/dev/null',
                        LIBGL_ALWAYS_SOFTWARE='1', HYPRLAND_NO_CRASHREPORTER='1',
                        GSETTINGS_BACKEND='memory', NO_AT_BRIDGE='1')
        for key in ('DISPLAY', 'HYPRLAND_INSTANCE_SIGNATURE', 'DBUS_SESSION_BUS_ADDRESS'):
            self.env.pop(key, None)
        self.compositor = self.spawn('compositor', ['dbus-run-session', '--', 'Hyprland',
                                                   '--config', str(entry)])

        def connected():
            self.assertIsNone(self.compositor.poll(), self.logs('compositor'))
            sockets = list(runtime.glob('hypr/*/.socket.sock'))
            if not sockets:
                return False
            self.env['HYPRLAND_INSTANCE_SIGNATURE'] = sockets[0].parent.name
            result = self.ctl('monitors', check=False)
            if result.returncode:
                return False
            monitors = json.loads(result.stdout)
            return monitors

        monitors = self.until(connected, 'Compositor não ficou disponível')
        self.assertTrue(all(m['hardwareDetails']['backend'] == 'wayland' for m in monitors),
                        'O teste exige exclusivamente o backend Wayland aninhado')
        displays = [p for p in runtime.glob('wayland-*') if p.is_socket()]
        self.assertEqual(len(displays), 1)
        self.env['WAYLAND_DISPLAY'] = displays[0].name
        # Clientes não devem acessar nem ativar os serviços D-Bus pessoais.
        self.env['DBUS_SESSION_BUS_ADDRESS'] = f'unix:path={runtime}/no-session-bus'

    def spawn(self, name, command):
        log = (self.base / (name + '.log')).open('w')
        self.addCleanup(log.close)
        process = subprocess.Popen(command, env=self.env, cwd=self.base,
                                   stdout=log, stderr=log, start_new_session=True)
        self.addCleanup(stop_process, process)
        return process

    def logs(self, name):
        return (self.base / (name + '.log')).read_text(errors='replace')[-12000:]

    def ctl(self, *args, check=True):
        # Sempre exige o socket temporário; nunca deixa hyprctl escolher a sessão real.
        self.assertIn('HYPRLAND_INSTANCE_SIGNATURE', self.env)
        result = subprocess.run(['hyprctl', '-j', *args], env=self.env, capture_output=True,
                                text=True, timeout=5)
        if check:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def until(self, predicate, message):
        deadline = time.monotonic() + 12
        while time.monotonic() < deadline:
            value = predicate()
            if value:
                return value
            time.sleep(0.1)
        self.fail(message + '\n' + self.logs('compositor'))

    def dispatch(self, expression):
        result = self.ctl('dispatch', expression)
        self.assertEqual(result.stdout.strip(), 'ok', result.stdout)

    def test_window_float_fullscreen_and_workspace(self):
        client = self.spawn('client', [sys.executable, '-c', '''
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
GLib.set_prgname('dotfiles-graphical-test')
window = Gtk.Window(title='Dotfiles integration test')
window.set_default_size(320, 240)
window.connect('destroy', Gtk.main_quit)
window.show_all()
Gtk.main()
'''])
        def active():
            self.assertIsNone(client.poll(), self.logs('client'))
            window = json.loads(self.ctl('activewindow').stdout)
            return window if window.get('pid') == client.pid else False
        window = self.until(active, 'Janela de teste não recebeu foco')
        self.assertFalse(window['floating'])
        self.dispatch('hl.dsp.window.float({ action = "toggle" })')
        self.until(lambda: active() and active()['floating'], 'Janela não ficou flutuante')
        self.dispatch('hl.dsp.window.fullscreen({ mode = "fullscreen", action = "toggle" })')
        self.until(lambda: active() and active()['fullscreen'] == 2, 'Fullscreen não ativou')
        self.dispatch('hl.dsp.window.fullscreen({ mode = "fullscreen", action = "toggle" })')
        self.until(lambda: active() and active()['fullscreen'] == 0, 'Fullscreen não desativou')
        self.dispatch('hl.dsp.window.move({ workspace = "2" })')
        self.dispatch('hl.dsp.focus({ workspace = "2" })')
        self.until(lambda: json.loads(self.ctl('activeworkspace').stdout).get('id') == 2,
                   'Workspace 2 não recebeu foco')
        self.until(lambda: active() and active()['workspace']['id'] == 2,
                   'Janela não foi movida para o workspace 2')
        self.assertFalse(any(json.loads(self.ctl('configerrors').stdout)))

    def test_waybar_creates_layer_and_reserves_space(self):
        bar = self.spawn('waybar', ['dbus-run-session', '--', 'waybar', '-c', str(ROOT / 'waybar/config'),
                                    '-s', str(ROOT / 'waybar/style.css')])
        def mapped():
            self.assertIsNone(bar.poll(), self.logs('waybar'))
            layers = json.loads(self.ctl('layers').stdout)
            return layers if 'waybar' in json.dumps(layers).lower() else False
        self.until(mapped, 'Waybar não criou uma layer surface')
        self.until(lambda: any(m['reserved'][1] > 0 for m in
                               json.loads(self.ctl('monitors').stdout)),
                   'Waybar não reservou espaço no topo')
        self.assertNotIn('Theme parsing error', self.logs('waybar'))

    def test_waybar_rejects_invalid_css(self):
        css = self.base / 'invalid.css'
        css.write_text('* { dotfiles-invalid-property: true; }')
        bar = self.spawn('invalid-waybar', ['dbus-run-session', '--', 'waybar',
                                           '-c', str(ROOT / 'waybar/config'), '-s', str(css)])
        self.assertNotEqual(bar.wait(timeout=10), 0, self.logs('invalid-waybar'))
        self.assertIn('dotfiles-invalid-property', self.logs('invalid-waybar'))
