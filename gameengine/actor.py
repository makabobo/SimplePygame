import pygame


class Actor:

    def __init__(self):
        self.alpha = 100
        self.rotation = 0
        self.scale = 1.0

    def tick(self, timedelta):
        pass

    def draw(self, surface):
        pass