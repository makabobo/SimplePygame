import pygame

from pygame.font import *
import random

font = Font("./gameengine/assets/pixelmix.ttf", 8, bold=False, italic=False)
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
    """ Testet ob r1 auf r2 aufliegt, d.h., dass die untere Kante von r1
        die obere Kante von r2 mit mind. 1 Pixel berührt.
        Wird benötigt um zu prüfen ob ein Actor auf einem Boden steht/läuft
    """
    return r1.y+r1.h == r2.y and not (r1.x+r1.w <= r2.x or r2.x+r2.w <= r1.x)


def random_color():
    return random.choice(palettecolors)


def distance(p1, p2):
    pass

def random_direction():
    pass

def random_speed():
    pass

def color_gradient(start, end):
    pass

def rainbow():
    retval = []
    for hue in range(0,360,10):
        c = pygame.Color("black")
        c.hsla = (hue,100,100,100)
        retval.append(c)

    return retval


palettecolors = ["black", "darkblue", "darkred", "darkgreen",
               "brown", "darkgrey", "lightgrey", "white",
               "red", "orange", "yellow", "green",
               "blue", "grey", "pink", "lightpink"]
