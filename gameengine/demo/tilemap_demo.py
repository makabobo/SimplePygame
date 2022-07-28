from gameengine import *
from gameengine.tilemap import Tilemap

from pygame import *

class MyActor(Actor):
    def __init__(self):
        pass

    def draw(self, surface):
        draw.circle(surface, "red", (240,128), 50, 3)


actors.append(MyActor())
start()


