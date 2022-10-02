import pygame
from .actor import *


class Camera(Actor):

    def __init__(self, game):
        super().__init__(game)
        self.follow_obj = None
        self.x = 0
        self.y = 0
        self.w = 480
        self.h = 256
        self.border_width = 100
        self.r = pygame.Rect(0, 0, 480, 256)

    def follow(self, fobj):
        self.follow_obj = fobj

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def get_screen_pos(self, pos):
        return pos[0]-self.x, pos[1]-self.y

    def update(self):
        if self.follow_obj:
            # follow_obj zu weit links?
            if self.follow_obj.r.centerx - self.x < self.border_width:
                self.x = self.follow_obj.r.centerx - self.border_width
            # follow_obj zu weit rechts?
            if self.x + self.w - self.follow_obj.r.centerx < self.border_width:
                self.x = self.follow_obj.r.centerx + self.border_width - self.w

            self.y = 48
            # if self.follow_obj.r.centery - self.y < self.border_width:
            #     self.y = self.follow_obj.r.centery - self.border_width
            # if self.y + self.h - self.follow_obj.r.centery < self.border_width:
            #     self.y = self.follow_obj.r.centery + self.border_width - self.h

            #self.y = self.follow_obj.r.centery-128
