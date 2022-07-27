import gameengine as g
from pygame import *

class MyActor(g.Actor):
    def draw(self, surface):
        for l in range (0,100):
            for hue in range(0, 360, 5):
                c = Color("red")
                c.hsla = (hue, 100, l, 100)
                draw.circle(surface, c, (hue+40,10+(2*l)), 3)

g.actors.append(MyActor())
g.start()
