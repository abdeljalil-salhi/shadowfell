from pygame import init, font, display, draw

init()
font = font.Font(None, 30)


def debug(info, y=10, x=10) -> None:
    display_surface = display.get_surface()
    debug_surf = font.render(str(info), True, "White")
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    draw.rect(display_surface, "Black", debug_rect)
    display_surface.blit(debug_surf, debug_rect)
