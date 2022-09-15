from .animation import Animation
from .actor import Actor

import sys

class SimplePopup(Actor):
    def __init__(self, pos):
        super().__init__()
        filename = "./assets/wall_collision.png"
        try:
            self.anim = Animation(filename, width=8, xflip=False)
        except Exception as e:
            print(f"Fehler bei Laden von {filename}: '{str(e)}'")
            sys.exit()
        self.pos = pos
        self.restlife = 5 * 40

    def tick(self):
        self.restlife -= 1
        if self.restlife == 0:
            self.dirty = True

    def draw(self, surface, delta):
        self.anim.draw(surface, (self.pos[0]-4, self.pos[1]-4), delta)
