from gameengine.actor import Actor
from gameengine.util import *


COLOR_BORDER    = pygame.Color("#414141")
COLOR_BLACK     = pygame.Color("#000000")
COLOR_RED_LIGHT = pygame.Color("#ffbfbf")
COLOR_RED_MID   = pygame.Color("#c20000")
COLOR_RED_DARK  = pygame.Color("#980000")

class PlayStat(Actor):
    def __init__(self, game):
        super().__init__(game)
        # Stats for the player
        self.lives = 3
        self.health = 100

        # For Drawing
        self.x = 200
        self.y = 10

        self.anim = get_anim_iterator([100,80,60,40,20,10,5,1], 30)

    def update(self):
        self.health = next(self.anim)

    def draw(self, sf, camera=None):
        # Gray Border

        w = self.health/100*76
        pygame.draw.rect(sf, COLOR_BORDER, (self.x,self.y,80,12),1)
        pygame.draw.rect(sf, COLOR_BLACK, (self.x+1,self.y+1,w+2,10),1)
        pygame.draw.rect(sf, COLOR_RED_MID, (self.x+2, self.y+2, w, 8), 1)
        pygame.draw.rect(sf, COLOR_RED_DARK, (self.x+3, self.y + 3, w-2, 6), 0)
        pygame.draw.rect(sf, COLOR_RED_LIGHT, (self.x + 3, self.y + 3, w-2, 1), 0)