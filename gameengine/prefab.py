from .actor import *
from .util import *
import pygame
from .tile import *


def draw_frame_times(surface, frame_times):
    """
    Zeichnet einen Zeitverlauf für die Dauer eines Frames
    """
    height = 30
    x = 350
    y = 00
    maxi = max(frame_times)
    for i in range(len(frame_times)):
        val = frame_times[i]
        if val == maxi:
            color = "red" if val >= 16 else "green"
            pygame.draw.line(surface, color, (x+i,y+height), (x+i, y+height-val), 1)
        else:
            pygame.draw.line(surface, "darkgray", (x + i, y + height), (x + i, y + height - val), 1)
    pygame.draw.line(surface, "red", (x+1, y + height / 2), (x+118, y + height / 2), 1)
    maxi = max(frame_times)
    draw_text(surface, f"max={maxi}ms", x+80,30)


class SimplePopup(Actor):
    def __init__(self, game, pos):
        super().__init__(game)
        self.mysprite = Sprite("gameengine/assets/wall_collision.png",4)
        self.pos = (pos[0]-3, pos[1]-3)

        self.restlife = 4*5
        self.anim = get_anim_iterator([0,1,2,3],5)

    def update(self):
        self.restlife -= 1
        if self.restlife == 0:
            self.dirty = True

    def draw(self, surface,camera=None):
        self.mysprite.frame_no = next(self.anim)
        self.mysprite.draw(surface, self.pos)

class Player(PhysicsBody):
    def __init__(self, game):
        super().__init__(0, 0, 12, 34, game)
        self.playersprite = Sprite("gameengine/assets/player.png", 12)

        self.walk_anim = get_anim_iterator([0,1,2,1],4)
        self.stand_anim = get_anim_iterator([3,4],20)
        self.jump_anim_up = get_anim_iterator([5],60)
        self.jump_anim_down = get_anim_iterator([6],60)
        self.die_anim = get_anim_iterator([7,8,9,10,11],20)


        self.current_anim = self.stand_anim

        self.is_dead = False

        self.on_floor = self.check_on_floor()
        self.on_stair = self.check_on_stair()
    def set_pos(self, pos):
        self.r.midbottom = pos

    def check_status(self):
        self.on_floor = self.check_on_floor()
        self.on_stair = self.check_on_stair()

    def kill(self):
        self.is_dead = True

    def update(self):
        if self.is_dead:
            return
        self.check_status()

        if self.game.controller.left:
            self.xs = -2
        elif self.game.controller.right:
            self.xs = 2
        else:
            self.xs = 0
        # Springen von Boden oder Treppe
        if self.game.controller.a == 1 and not self.game.controller.down and (self.on_stair or self.on_floor):
            self.ys = -6.7

        # Von Treppe fallen lassen
        if self.game.controller.a == 1 and self.game.controller.down and self.on_stair:
            self.r.y += 1

        # Auf dem Boden/Treppe ist Beschleunigung nach unten = 0.0
        if self.game.controller.a == 0 and (self.on_stair or self.on_floor):
            self.ys = 0.0
        super().update()

    def draw(self, surface, camera=None):
        if self.game.debug:
            pygame.draw.rect(surface, "red", self.r.move(-camera.x, -camera.y), 1)

        #self.game.debug_msg = f"ys={self.ys:0.5f}" #, pos={self.x},{self.y}"

        if self.is_dead:
            self.current_anim = self.die_anim
        else:
            if self.ys != 0.0:
                self.current_anim = self.jump_anim_up if self.ys < 0 else self.jump_anim_down

            else:
                if self.xs > 0.0:
                    self.current_anim = self.walk_anim
                    self.playersprite.flip = False
                elif self.xs < 0.0:
                    self.current_anim = self.walk_anim
                    self.playersprite.flip = True
                else:
                    self.current_anim = self.stand_anim

        self.playersprite.frame_no = next(self.current_anim)

        rect = pygame.Rect(0,0, self.playersprite.width, self.playersprite.height)
        rect.midbottom = self.r.midbottom
        rect.move_ip(-camera.x, -camera.y)
        if self.game.debug:
            pygame.draw.rect(surface, "yellow", rect, 1)
        self.playersprite.draw(surface, rect)

class TriggerRect(Actor):
    def __init__(self,game, rect):
        super().__init__(game)
        self.r = rect

    def draw(self, surface, camera=None):
        if self.game.debug:
            pygame.draw.rect(surface, "red", self.r.move(-camera.x, -camera.y), 1)


class MoonEnemy(Actor):
    def __init__(self, game, rect):
        super().__init__(game)
        self.r = rect
        self.anim = get_anim_iterator([0,0,0,1,2,2,2,1,],7)
        self.sprite = Sprite("gameengine/assets/spritesheet_enemy2.png", 6)

    def draw(self, surface, camera=None):
        self.sprite.draw(surface, self.r.move(-camera.x,-camera.y+next(self.anim)))
        if self.game.debug:
            pygame.draw.rect(surface, "red", self.r.move(-camera.x, -camera.y), 1)


