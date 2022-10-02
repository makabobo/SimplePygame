from gameengine import *
from pygame import *


def get_linear_steps(start:Vector2, end:Vector2, no_of_steps:int):
    """
    Gibt ein Array von Vektoren zurück, die auf einer Linie
    von start bis end liegen.
    Die Punkte zwischen start und end werden linear interpoliert.
    no_of_steps ist die Anzahl der Punkte inkl. start und end.
    """
    points = []
    for s in range(no_of_steps):
        t = s/(no_of_steps - 1)
        points.append(start*(1-t)+(end*t))
    return points


def walk():
    intervals = 60*[0] + 2*[0,1,0,0] +3*[1,0,0] + 3*[1,0] + 2*[1,1,0]
    for i in intervals:
        yield i
    while 1:
        yield 1

class A(Actor):

    def __init__(self, game):
        super().__init__(game)
        self.x = 10
        self.walk = walk()

    def update(self):
        self.x += next(self.walk)
        if self.x > 140:
            self.x = 10
            self.walk = walk()

    def draw(self, surface, delta, camera=None):
        p1 = Vector2(240, 50)
        p2 = Vector2(self.x,150)
        draw.circle(surface, "red", p1, 8, True)
        draw.circle(surface, "red", p2, 8, True)
        for p in get_linear_steps(p1, p2, 15):
            draw.line(surface, "yellow", p, p, 1)


a = A(game)
game.actors.append(a)
game.start()
