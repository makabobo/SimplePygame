import gamebase as g
import pygame as pyg
from gamehelper import *


class MyActor(g.Actor):
    def draw(self):
        for hue in range(0, 360, 10):
            c = pygame.Color("black")
            c.hsla = (hue, 100, 50, 100)
            pyg.draw.circle(g.draw_surface, c, (hue+40,100), 3)


g.actors.append(MyActor())
g.start()
