import pygame
from actor import *

debug = True

class TriggerRect(Actor):
    def __init__(self, name, x, y, w, h):
        self.name = name
        self.r = pygame.Rect(x, y, w, h)

    def tick(self):
        pass

    def draw(self):
        pass
        # if debug:
        #     pygame.draw.rect(draw_surface, "yellow", self.r.move(-camera.x, -camera.y), 1, 1)
            #draw_text(self.name, self.r.x - camera.x + 2, self.r.y - camera.y + 2, "gray")



class TriggerPoint(Actor):
    def __init__(self, name, x, y):
        self.name = name
        self.p = [x, y]

    def draw(self):
        pass
        # if debug:
        #     pygame.draw.circle(draw_surface, "yellow", (self.p[0] - camera.x, self.p[1] - camera.y), 1)
        #     ((self.name, self.p[0] - camera.x, self.p[1] - camera.y, "gray"))
