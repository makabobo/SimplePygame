from gameengine.actor import *
from gameengine.util import *
import gameengine.util as util
from .tile import *
from random import randint


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
        self.mysprite = Sprite("gameengine/assets/wall_collision_white.png",4)
        self.pos = (pos[0]-3, pos[1]-3)

        self.restlife = 4*5
        self.anim = get_anim_iterator([0,1,2,3],5)

    def update(self):
        self.restlife -= 1
        if self.restlife == 0:
            self.dirty = True

    def draw(self, surface,camera=None):
        self.mysprite.frame_no = next(self.anim)
        self.mysprite.draw(surface, (self.pos[0]-camera.x, self.pos[1]-camera.y))
####################################################################################################
class Player(PhysicsBody):
    def __init__(self, game):
        super().__init__(0, 0, 12, 31, game)
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

        self.killed_listener = None
    def set_pos(self, pos):
        self.r.midbottom = pos

    def add_killed_listener(self, listener):
        self.killed_listener = listener

    def check_status(self):
        self.on_floor = self.check_on_floor()
        self.on_stair = self.check_on_stair()

    def kill(self):
        self.dirty = True
        if self.killed_listener:
            self.killed_listener(self.game)

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
            self.game.add_actor(SimplePopup(self.game, self.r.midbottom))

        # Von Treppe fallen lassen
        if self.game.controller.a == 1 and self.game.controller.down and self.on_stair:
            self.r.y += 1

        # Auf dem Boden/Treppe ist Beschleunigung nach unten = 0.0
        if self.game.controller.a == 0 and (self.on_stair or self.on_floor):
            self.ys = 0.0
            #self.game.add_actor(SimplePopup(self.game, self.r.midbottom))
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

####################################################################################################
class MoonEnemy(Actor):
    def __init__(self, game, rect):
        super().__init__(game)
        self.r = rect
        self.anim_updown = get_anim_iterator([0, 0, 0, 1, 2, 2, 2, 1, ], 7)
        self.anim_eye = get_anim_iterator([0,1,0,2,3,0,1,1,0,2,4,0,1,0,2,2,0,1,1,0,2,5,3,3],120)
        self.sprite = Sprite("gameengine/assets/spritesheet_enemy2.png", 6)

    def set_eye_direction(self):
        pass

    def draw(self, surface, camera=None):
        self.sprite.frame_no = next(self.anim_eye)
        self.sprite.draw(surface, self.r.move(-camera.x, -camera.y + next(self.anim_updown)))
        if self.game.debug:
            pygame.draw.rect(surface, "red", self.r.move(-camera.x, -camera.y), 1)

####################################################################################################
class Diamond(Actor):

    def __init__(self, game,rect):
        super().__init__(game)
        self.spr = Sprite("gameengine/assets/spritesheet_diamond.png", 1)
        self.snd = pygame.mixer.Sound("gameengine/assets/sound/sfx_3.wav")
        self.r = rect

    def update(self):
        if pls := self.game.get_actors_by_type("Player"):
            p = pls[0]
            if self.r.colliderect(p.r):
                self.game.add_actor(SimplePopup(self.game, self.r.center))
                self.snd.play()
                self.dirty = True

    def draw(self, surface, camera=None):
        self.spr.draw(surface, self.r.move(-camera.x, -camera.y))
        if self.game.debug:
            pygame.draw.rect(surface, "red", self.r.move(-camera.x, -camera.y), 1)

####################################################################################################
class MovingPlatform(Actor):
    def __init__(self, game, rect):
        super().__init__(game)
        self.r = rect
        self.sprite = Sprite("gameengine/assets/spritesheet_platform1.png", 2)
        self.anim = get_anim_iterator([0,1],2)
        self.moves = get_anim_iterator(144*[-1]+20*[0]+144*[1]+20*[0],1)
        for x in range(random.randint(0,50)):
            self.r.move_ip(next(self.moves),0)

    def update(self):
        dx = next(self.moves)

        self.r.move_ip(dx,0)
        for pe in self.game.get_actors_by_type("Player"): # TODO Verbesserung: Nicht nur Player berücks.
            if not pe.r.colliderect(self.r) and pe.r.move(0, 1).colliderect(self.r):
                pe.move2(dx, 0)

    def draw(self, surface, camera=None):
        self.sprite.frame_no = next(self.anim)
        self.sprite.draw(surface, self.r.move(-camera.x, -camera.y))
        if self.game.debug:
            pygame.draw.rect(surface, "red", self.r.move(-camera.x, -camera.y), 1)
####################################################################################################

class WaterEffect(Actor):
    def __init__(self, game):
        super().__init__(game)
        self.offset = 0
        self.slower = util.get_anim_iterator([0,1],1)

    def draw(self, surface, camera=None):
        if next(self.slower):
            self.offset += 1
            self.offset %= 80
        # Bad coding here, maybe too slow
        anim = util.get_anim_iterator([0,1,2,2,1,0,-1,-2,-2,-1], 8)
        for _ in range(self.offset):
            next(anim)
        for y in range(256):
            surface.set_clip(pygame.Rect(0, y, 480, 1))
            surface.scroll(next(anim),0)
        surface.set_clip(None)
        for _ in range(self.offset):
            next(anim)
        for x in range(0,480,1):
            surface.set_clip(pygame.Rect(x, 0, 1, 256))
            surface.scroll(0, next(anim))
        surface.set_clip(None)

####################################################################################################

class DistortionEffect(Actor):
    def __init__(self, game):
        super().__init__(game)
        self.dox = True
        self.doy = True
        self.step= 1
        self.intense=3

    def draw(self, surface, camera=None):
        if self.doy:
            for y in range(0, 256, self.step):
                surface.set_clip(pygame.Rect(0, y, 480, self.step))
                surface.scroll(randint(0,self.intense),0)
        if self.dox:
            for x in range(0, 480, self.step):
                surface.set_clip(pygame.Rect(x, 0, self.step, 256))
                surface.scroll(0,randint(0,self.intense))
        surface.set_clip(None)

####################################################################################################

class GameOverSquence(Actor):

    def __init__(self, g):
        super().__init__(g)
        self.y = 80
        self.script = TimedCallbackList()
        self.script.add_step(self.down, frames=30)
        self.script.add_step(self.wait, frames=90)
        self.script.add_step(self.up,  frames=30)
        self.script.add_step(self.end, frames=0)

        self.finished_listener = None

    def add_finished_listener(self, listener):
        self.finished_listener = listener

    def wait(self):
        pass

    def up(self):
        self.y -= 1
    def down(self):
        self.y += 1

    def end(self):
        if self.finished_listener:
            self.finished_listener(self.game)
        self.dirty = True

    def update(self):
        self.script.update()

    def draw(self, surface, camera=None):
        draw_text(surface, "YOU DIED, IDIOT", 200, self.y, "red")

####################################################################################################

class FlyingFragmentCreator(Actor):
    def __init__(self, game):
        super().__init__(game)
        self.counter = 0

    def update(self):
        self.counter += 1
        self.counter %= 132


        if self.counter == 1:
            for a in range(10):
                self.game.add_actor(FlyingFragment(
                    self.game,
                    pos=Vector2(730,570),
                    angle = Vector2(-1,0).rotate(randint(0,360)),
                    speed = 130,
                    color = pygame.Color("red")
                ))

    def draw(self, sf, cam=None):
        if self.game.debug:
            pygame.draw.circle(sf, "red", (730-cam.x,570-cam.y),radius=10, width=1)

class FlyingFragment(Actor):
    def __init__(self, game, pos: Vector2, angle: Vector2, speed: int, color: pygame.Color):
        super().__init__(game)
        self.pos = pos
        self.vel = angle * speed
        self.accel = Vector2(0,4.0)  # Gravity
        self.color = color
        self.maxlife = 200

    def update(self):
        self.maxlife -= 1
        if self.maxlife <= 0:
            self.dirty = True
        delta = 1/60
        self.vel += self.accel
        self.pos += self.vel * delta

    def draw(self, sf, cam=None):
        pygame.draw.circle(sf, "#805050", (self.pos.x-cam.x,self.pos.y-cam.y),radius=3, width=0)
