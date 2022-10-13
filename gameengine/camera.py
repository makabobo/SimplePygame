import pygame.gfxdraw
from .actor import *

class Camera(Actor, pygame.Rect):
    BORDER_WIDTH = 340
    BORDER_HEIGHT = 150

    def __init__(self, game):
        super().__init__(game)
        self.x = 0
        self.y = 0
        self.w = 480
        self.h = 256
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
        if not self.follow_obj:
            return
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
                # Bildschirm-Wechsel-Event erzeugen
                pass
            self.cur_corridor = in_corridor[0]
        if self.cur_corridor:
            self.clamp_ip(self.cur_corridor)

