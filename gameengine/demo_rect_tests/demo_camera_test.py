import gameengine.util
from gameengine import *
import pygame



class MyCamera(Actor, pygame.Rect):
    BORDER_WIDTH = 40
    BORDER_HEIGHT = 15

    def __init__(self, game):
        super().__init__(game)
        self.x = 100
        self.y = 200
        self.w = 80
        self.h = 48
        self.inner_cam = self.inflate(-self.BORDER_WIDTH, -self.BORDER_HEIGHT)

        # TODO: Überprüfung, ob Korridore disjunkt sein
        self.corridors = []
        self.cur_corridor = None
        self.follow_obj = None

    def add_corridor(self, corridor:pygame.Rect):
        self.corridors.append(corridor)

    def follow(self, fobj):
        self.follow_obj = fobj

    def to_screen_pos(self, map_pos):
        """
        Wandelt eine Map-Koordinete (x,y) in eine Screen-Koordinate um
        """
        return map_pos[0]-self.x, map_pos[1]-self.y

    def to_map_pos(self, screen_pos):
        """
        Wandelt eine Screen-Koordinete (x,y) in eine Map-Koordinate um
        """
        return screen_pos[0]+self.x, screen_pos[1]+self.y

    def update(self):
        x, y = self.follow_obj.r.center
        if not self.inner_cam.collidepoint(x, y):
            # inner_rect so verschieben, dass x,y innerhalb ist.
            if x < self.inner_cam.left:
                self.inner_cam.left = x
            if x > self.inner_cam.right:
                self.inner_cam.right = x
            if y < self.inner_cam.top:
                self.inner_cam.top = y
            if y > self.inner_cam.bottom:
                self.inner_cam.bottom = y

        self.center = self.inner_cam.center

        in_corridor = [x for x in self.corridors if x.collidepoint(self.follow_obj.r.center) is True]
        if in_corridor:
            if self.cur_corridor != in_corridor[0]:
                print("Bildschirm Wechsel")
                # Bildschirm-Wechsel-Event erzeugen
                pass
            self.cur_corridor = in_corridor[0]

        if self.cur_corridor:
            self.clamp_ip(self.cur_corridor)

    def draw(self, surface, camera=None):
        pygame.draw.rect(surface, "red", self.corridors[0], 1)
        pygame.draw.rect(surface, "white", self.corridors[1], 1)
        pygame.draw.rect(surface, "blue", self, 1)
        pygame.draw.rect(surface, "green", self.inner_cam, 1)


####################################################################################
class PlayerDummy(Actor):
    def __init__(self, game):
        super().__init__(game)

    def update(self):
        self.r = pygame.Rect(pygame.mouse.get_pos(), (5,5))

    def draw(self, surface, camera=None):
        pygame.draw.rect(surface, "orange", self.r, 1)

g = Game()
cam = MyCamera(g)
cam.add_corridor(pygame.Rect(100,20,300,78))
cam.add_corridor(pygame.Rect(320,98,80,110))

p = PlayerDummy(g)
cam.follow(p)
g.camera.follow(p)
g.actors.append(p)
g.actors.append(cam)
g.start()
