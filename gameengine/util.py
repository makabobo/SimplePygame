import pygame

from pygame.font import *

font = Font("assets/mago3.ttf", 16, bold=False, italic=False)
print_map = {}

def draw_text(draw_surface, text, x, y, color="white"):
    global font
    global print_map

    if (text, color) in print_map.keys():
        draw_surface.blit(print_map[(text, color)], (x, y))
    else:
        s = font.render(text, False, color)
        print_map[(text, color)] = s
        draw_surface.blit(s, (x, y))


def test_rect_lying_on_rect(r1:pygame.Rect, r2:pygame.Rect) -> bool:
    """ Testet ob top_rect auf bottom_rect aufliegt, d.h.
         - die untere Kante von top_rect berührt die obere Kante von bottom_rect
        Wird benötigt um zu prüfen ob ein Actor auf einem Boden steht/läuft
    """
    return r1.y+r1.h == r2.y and not (r1.x+r1.w <= r2.x or r2.x+r2.w <= r1.x)


