from gameengine import *
from gameengine.util import *
from gameengine.actor import *

game.load_map("gameengine/assets/test-map.tmj")
class Timer:

    def __init__(self):
        self.flist = []

    class TimerStep:
        def __init__(self, func, frames):
            self.func = func
            self.frames = frames

    def add_step(self, func, frames=0):
        if frames == 0:
            frames = -1
        self.flist.append(self.TimerStep(func, frames))

    def wait(self):
        pass

    def update(self):

        while self.flist:

            # Nächster Eintrag mit -1 (Direkt-Ausführung mit 0 Ticks)
            if self.flist[0].frames == -1:
                self.flist[0].func()
                del self.flist[0]
                continue

            # Nächster Eintrag vollständig ausgeführt?
            if self.flist[0].frames == 0:
                del self.flist[0]
                continue

            # Nächster Step mit frames >= 1
            if self.flist[0].frames >= 1:
                self.flist[0].func()
                self.flist[0].frames -= 1
                return

class TimerNew:

    def __init__(self):
        self.steps = []
        self.cur_step = 0

    class TimerStep:
        def __init__(self, func, frames):
            self.func = func
            self.frames = frames

    def add_step(self, func, frames):
        self.steps.append(self.TimerStep(func, frames))

    def wait(self):
        pass

    def update(self):
        if not self.steps:
            return




class ShortMessageTop(Actor):

    def __init__(self, g, msg):
        super().__init__(g)
        self.msg = msg
        self.y = -10
        self.script = Timer()
        self.script.add_step(self.down, frames=60)
        self.script.add_step(self.wait, frames=30)
        self.script.add_step(self.up,  frames=60)
        self.script.add_step(self.end, frames=0)

    def wait(self):
        pass

    def up(self):
        self.y -= 1

    def down(self):
        self.y += 1

    def end(self):
        print("Dirty...")
        self.dirty = True

    def update(self):
        self.script.update()

    def draw(self, surface, camera=None):
        draw_text(surface, self.msg, 220, self.y, "red")

p = ShortMessageTop(game, "10 Punkte")
game.actors.append(p)
game.start()


