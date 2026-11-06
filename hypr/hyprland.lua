local root = (os.getenv("XDG_CONFIG_HOME") or (os.getenv("HOME") .. "/.config")) .. "/hypr/"
package.path = root .. "?.lua;" .. package.path
require("lua.programs")
require("lua.monitors")
require("lua.variables")
require("lua.autostart")
require("lua.appearance")
require("lua.animations")
require("lua.layouts")
require("lua.misc")
require("lua.input")
require("lua.keybinds")
require("lua.workspaces")
require("lua.window-rules")

local f = io.open(root .. "local.lua", "r")
if f then f:close(); dofile(root .. "local.lua") end
