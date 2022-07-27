from pygame.font import *
import pygame.draw
import ctypes
import sys
import logging

from .menu import *
from .camera import *
from .input import *

logging.getLogger().setLevel("INFO")

pygame.init()
ctypes.windll.user32.SetProcessDPIAware()


screen = pygame.display.set_mode((480, 256), pygame.SCALED | pygame.RESIZABLE, vsync=1)

draw_surface = pygame.Surface((480, 256))
clock = pygame.time.Clock()
actors = []

triggers = []
camera = Camera()
debug = False

# map = Tilemap()
# player = Player(map, 300, 190)

font = Font("mago3.ttf", 16, bold=False, italic=False)
print_map = {}
def draw_text(text, x, y, color="white"):
    global font
    global print_map

    if (text, color) in print_map.keys():
        draw_surface.blit(print_map[(text, color)], (x, y))
    else:
        s = font.render(text, False, color)
        print_map[(text, color)] = s
        draw_surface.blit(s, (x, y))

controller = Controller()
menu = None

def start():
    delta = 0.0
    global menu
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if menu == None:
                    menu = MainMenu()
                else:
                    menu = None

        controller.tick(delta)

        for a in actors:
            a.tick(delta)

        if menu:
            menu.tick(delta)

        draw_surface.fill("black")
        for a in actors:
            a.draw(draw_surface)

        if menu is None:
            pass
        else:
            menu.draw(draw_surface)

        if debug:
            draw_text(f"FPS {clock.get_fps():>3.1f}", 420, 3, "darkred")

        screen.blit(draw_surface, (0, 0))
        pygame.display.flip()
        delta = clock.tick(60)
