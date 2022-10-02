from .actor import *
from .util import *
import pygame



def draw_frame_times(surface, pos, frame_times):
    """
    Zeichnet einen Zeitverlauf für die Dauer eines Frames
    """
    height = 30
    pygame.draw.rect(surface, "darkblue", (pos[0], pos[1], 120, height), 1)
    pygame.draw.line(surface, "red", (pos[0]+1, pos[1] + height / 2), (pos[0]+118, pos[1] + height / 2), 1)
    for i in range(len(frame_times)):
        val = frame_times[i]/2
        pygame.draw.line(surface, "darkblue", (pos[0]+i,pos[1]+height), (pos[0]+i, pos[1]+height-val), 1)

class SimplePopup(Actor):
    def __init__(self, game, pos):
        super().__init__(game)
        self.mysprite = Sprite("gameengine/assets/wall_collision.png",4)
        self.pos = (pos[0]-3, pos[1]-3)

        self.restlife = 4*5
        self.anim = get_anim_iterator([0,1,2,3],5)

    def tick(self):
        self.restlife -= 1
        if self.restlife == 0:
            self.dirty = True

    def draw(self, surface, delta, camera=None):
        self.mysprite.frame_no = next(self.anim)
        self.mysprite.draw(surface, self.pos)



