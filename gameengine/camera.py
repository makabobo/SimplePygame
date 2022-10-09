import pygame.gfxdraw
from .actor import *

class Camera(Actor, pygame.Rect):
    BORDER_WIDTH = 340
    BORDER_HEIGHT = 200

    def __init__(self, game):
        super().__init__(game)
        self.x = 0
        self.y = 0
        self.w = 480
        self.h = 256
        self.inner_cam = self.inflate(-self.BORDER_WIDTH, -self.BORDER_HEIGHT)

        # TODO: Überprüfung, ob Korridore disjunkt sein
        self.corridors = [pygame.Rect(0,48,960,256),
                          pygame.Rect(480,304,480,384),
                          pygame.Rect(960, 560, 480, 256),
                          pygame.Rect(480,688,480,256),
                          pygame.Rect(0, 304, 480, 640)
                          ]
        self.cur_corridor = self.corridors[0]
        self.follow_obj = None

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
            self.cur_corridor = in_corridor[0]
        self.clamp_ip(self.cur_corridor)
