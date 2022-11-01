from gameengine import *
from gameengine.util import *
from gameengine.actor import *

game.load_map("gameengine/assets/tilemap/test-map.tmj")

class TimedCallbackList:

    def __init__(self):
        self.steps = []
        self.cur_step = 0
        self.cur_step_count = 0

    class TimerStep:
        def __init__(self, func, count):
            self.func = func
            self.count = count

    def add_step(self, func, frames):
        self.steps.append(self.TimerStep(func, frames))

    def wait(self):
        pass

    def update(self):
        if not self.steps:
            return
        while True:
            ts = self.steps[self.cur_step]
            ts.func()
            self.cur_step_count += 1
            if self.cur_step_count >= ts.count:
                self.cur_step += 1
                self.cur_step_count = 0
                if self.cur_step >= len(self.steps):
                    self.cur_step = 0
                if ts.count > 0:
                    return
            else:
                return

class ShortMessageTop(Actor):

    def __init__(self, g):
        super().__init__(g)
        self.y = 70
        self.script = TimedCallbackList()
        self.script.add_step(self.down, frames=30)
        self.script.add_step(self.wait, frames=30)
        self.script.add_step(self.up,  frames=30)
        self.script.add_step(self.end, frames=0)

    def wait(self):
        pass

    def up(self):
        self.y -= 1

    def down(self):
        self.y += 1

    def end(self):
        self.dirty = True

    def update(self):
        self.script.update()

    def draw(self, surface, camera=None):
        draw_text(surface, "YOU DIED", 220, self.y, "red")

p = ShortMessageTop(game)
game.actors.append(p)
game.start()


