-----------------------
---- LOOK AND FEEL ----
-----------------------
hl.config({
    render = {
        -- Evita alternar automaticamente para HDR ao entrar em tela cheia.
        cm_auto_hdr = 0,
    },

    general = {
        gaps_in  = 5,
        gaps_out = 10,

        border_size = 2,

        col = {
            active_border   = { colors = {"rgba(ff334fff)", "rgba(b51632ff)"}, angle = 45 },
          inactive_border = "rgba(1a1a1aee)",
        },

        resize_on_border = false,
        allow_tearing    = false,
        layout           = "dwindle",
    },

    decoration = {
        rounding       = 10,
        rounding_power = 2,

        active_opacity    = 0.92,
        inactive_opacity  = 0.95,
        fullscreen_opacity = 1.0,

        shadow = {
            enabled      = true,
          range        = 4,
          render_power = 3,
          color        = "rgba(1a1a1aee)",
        },

        blur = {
            enabled  = true,
          size     = 3,
          passes   = 1,
          vibrancy = 0.1696,
        },
    },

})

require("lua.colors")
