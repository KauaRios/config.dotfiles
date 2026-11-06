-- Teclado, mouse, touchpad e gestos
hl.config({
    input = {
        kb_layout  = "br",
        kb_variant = "",
        kb_model   = "",
        kb_options = "",
        kb_rules   = "",

        follow_mouse = 1,
        sensitivity  = -0.7,

        touchpad = {
            natural_scroll = false,
            --desabilita cursor Ao digitar
            disable_while_typing = true,

        },
    },
})

-- Gesto de 3 dedos para trocar workspace
hl.gesture({
    fingers   = 3,
    direction = "horizontal",
    action    = "workspace",
})
