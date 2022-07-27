import pygame

class Controller:
    def __init__(self):
        self.a = 0
        self.b = 0
        self.menu = 0
        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0

    def tick(self, delta):
        if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_RETURN]:
            self.a += 1
        else:
            self.a = 0

        if pygame.key.get_pressed()[pygame.K_s]:
            self.b += 1
        else:
            self.b = 0

        if pygame.key.get_pressed()[pygame.K_UP]:
            self.up += 1
        else:
            self.up = 0

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.down += 1
        else:
            self.down = 0

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.left += 1
        else:
            self.left = 0

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.right += 1
        else:
            self.right = 0
