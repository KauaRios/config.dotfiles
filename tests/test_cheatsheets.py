"""Integração da ajuda no terminal, sem iniciar aplicativos."""
from pathlib import Path
import shutil
import subprocess
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
local actions = {}
hl = { dsp = setmetatable({ exec_cmd = function(command) return command end }, { __index = callable }), bind = function(keys, action, flags)
    assert(type(flags.description) == "string" and #flags.description > 0, keys)
    count = count + 1
    seen[keys] = flags.description
    actions[keys] = action
end }
dofile(arg[1] .. "/hypr/lua/keybinds.lua")
assert(count >= 50, "Os loops de workspaces precisam ser expandidos")
assert(seen["SUPER + H"] == "Consultar atalhos")
assert(actions["SUPER + H"] == 'kitty -e lua "${XDG_CONFIG_HOME:-$HOME/.config}/hypr/scripts/cheat_sheet.lua"')
assert(seen["SUPER + 0"] == "Ir para workspace 10")
assert(seen["SUPER + SHIFT + 0"] == "Mover janela para workspace 10")
assert(seen["SUPER + mouse:272"] == "Arrastar janela")
'''
        subprocess.run(['lua', '-', str(ROOT)], input=harness, text=True,
                       check=True, capture_output=True, timeout=10)
