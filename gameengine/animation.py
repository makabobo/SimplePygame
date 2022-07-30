import math
import pygame


class Animation:
    def __init__(self, imgpath, width, xflip=False, repeat=True):
        if imgpath == "":
            return
        img = pygame.image.load(imgpath)
        img_count = int(math.floor(img.get_width() / width))

        self.images = []
        self.repeat = repeat
        self.actual_index = 0
        self.width = width
        self.timer = 0
        self.height = img.get_height()
        self.end = False
        for i in range(img_count):
            anim_img = pygame.Surface((width, img.get_height()), pygame.SRCALPHA)
            anim_img.blit(img, (0, 0), pygame.Rect(i * width, 0, width, img.get_height()))
            if xflip:
                anim_img = pygame.transform.flip(anim_img, True, False)
            self.images.append(anim_img)

    def draw(self, surface, pos, delta):
        self.timer += delta
        if self.timer > 100:
            self.timer = 0
            self.actual_index += 1
            if self.actual_index == len(self.images):
                self.actual_index = 0
        surface.blit(self.images[self.actual_index], pos)