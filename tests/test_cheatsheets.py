"""Integração da ajuda, sem iniciar aplicativos nem avaliar Lua no Rust."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CheatsheetTests(unittest.TestCase):
    def test_live_bindings_have_descriptions_including_workspace_loops(self):
        if not shutil.which('lua'):
            self.skipTest('Instale Lua para conferir as binds.')
        harness = r'''
package.path = arg[1] .. "/hypr/?.lua;" .. package.path
local callable = {}
setmetatable(callable, {
    __index = function() return callable end,
    __call = function() return {} end,
})
local count = 0
local seen = {}
hl = { dsp = callable, bind = function(keys, action, flags)
    assert(type(flags.description) == "string" and #flags.description > 0, keys)
    count = count + 1
    seen[keys] = flags.description
end }
dofile(arg[1] .. "/hypr/lua/keybinds.lua")
assert(count >= 50, "Os loops de workspaces precisam ser expandidos")
assert(seen["SUPER + H"] == "Consultar atalhos")
assert(seen["SUPER + 0"] == "Ir para workspace 10")
assert(seen["SUPER + SHIFT + 0"] == "Mover janela para workspace 10")
assert(seen["SUPER + mouse:272"] == "Arrastar janela")
'''
        subprocess.run(['lua', '-', str(ROOT)], input=harness, text=True,
                       check=True, capture_output=True, timeout=10)

    def test_launcher_resolves_symlink_and_passes_section(self):
        with tempfile.TemporaryDirectory(prefix='dot help ') as folder:
            base = Path(folder)
            repo = base / 'repo with spaces'
            scripts = repo / 'hypr/scripts'
            scripts.mkdir(parents=True)
            shutil.copy2(ROOT / 'hypr/scripts/cheatsheet.sh', scripts / 'cheatsheet.sh')
            binary = repo / 'hyprland-cheatsheets/target/release/hyprland-cheatsheets'
            binary.parent.mkdir(parents=True)
            binary.write_text('#!/bin/sh\nprintf "%s\\n" "$@"\n')
            binary.chmod(0o755)
            config = base / 'hypr-link'
            config.symlink_to(repo / 'hypr', target_is_directory=True)
            result = subprocess.run(['bash', str(config / 'scripts/cheatsheet.sh')],
                                    capture_output=True, text=True, timeout=10, check=True)
            self.assertEqual(result.stdout.splitlines(), ['--section', 'hyprland'])
