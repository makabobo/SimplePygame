import pygame
from .actor import *


# class Camera(Actor):
#
#     def __init__(self, game):
#         super().__init__(game)
#         self.follow_obj = None
#         self.x = 0
#         self.y = 0
#         self.border_width = 100
#         self.r = pygame.Rect(0, 0, 480, 256)
#
#     def follow(self, fobj):
#         self.follow_obj = fobj
#
#     def get_rect(self):
#         return pygame.Rect(self.x, self.y, 480, 256)
#
#     def get_screen_pos(self, pos):
#         return pos[0]-self.x, pos[1]-self.y
#
#     def update(self):



class Camera(Actor):
    smoothiness = 10

    def __init__(self, game):
        super().__init__(game)

        self._xf = 0.0
        self._yf = 0.0
        self.x = 0
        self.y = 0
        self.w = 480
        self.h = 256
        self.obj = None
        self.smooth_follow = True

    def get_offset(self):
        return -self.x, -self.y

    def follow(self, fobj):
        self.obj = fobj
        self._xf = self.obj.r.centerx - 480 / 2
        self._yf = self.obj.r.centery - 256 / 2
        self.f2i()

    def f2i(self):
        self.x = int(self._xf)
        self.y = int(self._yf)

    def update(self):
        if self.obj:
            fox = self.obj.r.centerx - 480 / 2
            foy = self.obj.r.centery - 256 / 1.7
            if self.smooth_follow:
                diff = abs(self._xf - fox)
                if fox < self._xf:
                    self._xf = self._xf - diff / Camera.smoothiness
                else:
                    self._xf = self._xf + diff / Camera.smoothiness

                diff = abs(self._yf - foy)
                if foy < self._yf:
                    self._yf = self._yf - diff / Camera.smoothiness
                else:
                    self._yf = self._yf + diff / Camera.smoothiness
            else:
                self._xf = fox
                self._yf = foy
        else:
            pass
        self.f2i()
