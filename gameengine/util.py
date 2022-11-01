import pygame

from pygame.font import *
import random


#font = Font("./gameengine/assets/font/m3x6.ttf", 15, bold=False, italic=False)
#font = Font("./gameengine/assets/font/m5x7.ttf", 15, bold=False, italic=False)
font = Font("./gameengine/assets/font/pixelmix.ttf", 8, bold=False, italic=False)
print_map = {}

def draw_text(draw_surface, text, x, y, color="white"):
    global font
    global print_map

    if (text, color) in print_map.keys():
        draw_surface.blit(print_map[(text, color)], (x, y))
    else:
        s = font.render(text, False, color)
        print_map[(text, color)] = s
        draw_surface.blit(s, (x, y))


def test_rect_lying_on_rect(r1:pygame.Rect, r2:pygame.Rect) -> bool:
    """ Testet ob r1 auf r2 aufliegt, d.h., dass die untere Kante von r1
        die obere Kante von r2 mit mind. 1 Pixel berührt.
        Wird benötigt um zu prüfen ob ein Actor auf einem Boden steht/läuft
    """
    return r1.y+r1.h == r2.y and not (r1.x+r1.w <= r2.x or r2.x+r2.w <= r1.x)


def random_color():
    return random.choice(palettecolors)

def get_anim_iterator(array, duration):
    while 1:
        for element in array:
            for x in range(duration):
                yield element

def delimit(x, begin, end):
    if x < begin:
        return begin
    elif x > end:
        return end
    else:
        return x
def rainbow():
    retval = []
    for hue in range(0,360,10):
        c = pygame.Color("black")
        c.hsla = (hue,100,100,100)
        retval.append(c)

    return retval


palettecolors = ["black", "darkblue", "darkred", "darkgreen",
               "brown", "darkgrey", "lightgrey", "white",
               "red", "orange", "yellow", "green",
               "blue", "grey", "pink", "lightpink"]

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

