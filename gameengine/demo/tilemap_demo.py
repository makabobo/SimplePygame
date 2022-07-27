from gameengine import *
from gameengine.tilemap import Tileset

from pygame import *

class MyActor(Actor):
    def __init__(self):
        self.tileset = Tileset()
        self.tileset.load("gameengine/test-tileset2.tsj")

    def draw(self, surface):
        draw.circle(surface, "red", (240,128), 50, 3)


actors.append(MyActor())
start()


