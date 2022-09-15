from pygame import Vector2

from gameengine import *
from gameengine.util import *
from gameengine.helper import *

game.load_map("gameengine/assets/test-map.tmj")

class Script(Actor):
    def __init__(self, g):
        super().__init__(g)
        self.flist = []
        self.frame_counter = 0

    def add_step(self, f, frames=1):
        self.flist.append((f, frames))

    def wait(self):
        pass

    def tick(self):
        if self.flist and self.frame_counter > 0:
            self.flist[0][0]()
            self.frame_counter -= 1
            if self.frame_counter == 0:
                del self.flist[0]
                if len(self.flist)==0:
                    self.dirty = True
        if self.frame_counter == 0 and self.flist:
            self.frame_counter = self.flist[0][1]


class ShortMessageTop(Script):

    def __init__(self, g, msg):
        super().__init__(g)
        self.msg = msg
        self.y = -10
        self.add_step(self.wait, frames=20)
        self.add_step(self.down, frames=20)
        self.add_step(self.wait, frames=50)
        self.add_step(self.down, frames=5)
        self.add_step(self.wait, frames=50)
        self.add_step(self.up, frames=30)
        self.add_step(self.wait, frames=10)

    def up(self):
        self.y -= 2

    def down(self):
        self.y += 2

    def draw(self, surface, delta, camera=None):
        draw_text(surface, self.msg, 220, self.y, random_color())


p = ShortMessageTop(game, "10 Punkte")
game.actors.append(p)
game.start()


