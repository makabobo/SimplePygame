from pygame.font import *
import pygame.draw
import ctypes
import sys
import logging

from .menu import *
from .camera import *
from .input import *
from .tilemap import *

logging.getLogger().setLevel("INFO")

pygame.init()
ctypes.windll.user32.SetProcessDPIAware()

screen = pygame.display.set_mode((480, 256), pygame.SCALED | pygame.RESIZABLE, vsync=1)

draw_surface = pygame.Surface((480, 256))
clock = pygame.time.Clock()
actors = []

#camera = Camera()
debug = False

map = Tilemap()
map.load("test-map.tmj")

# player = Player(map, 300, 190)


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
            menu.tick(delta, controller)

        if map:
            map.tick()

        draw_surface.fill("black")

        if map:
            map.draw(draw_surface, pygame.Rect(0,0,480,256))

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
