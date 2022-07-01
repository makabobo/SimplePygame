import gamebase as g
from pygame import *

class MyActor(g.Actor):
    def draw(self, surface):
        for hue in range(0, 360, 10):
            c = Color("black")
            c.hsla = (hue, 100, 50, 100)
            draw.circle(surface, c, (hue+40,100), 3)

g.actors.append(MyActor())
g.start()
