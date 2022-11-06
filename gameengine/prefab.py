import pygame.gfxdraw

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

        x,y = self.r.center
        create_player_explosion(self.game, x, y)
        if self.killed_listener:
            self.killed_listener(self.game)
    def collided_top(self):
        x, y = self.r.midtop
        create_fragments(self.game, x, y)

    def collided_bottom(self):
        pass
        #self.game.add_actor(gameengine.prefab.SimplePopup(self.game, self.r.midbottom))

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
            #self.game.add_actor(SimplePopup(self.game, self.r.midbottom))

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
    MAX_SPEED = 2.0
    AWARE_RADIUS=150

    def __init__(self, game, rect):
        super().__init__(game)
        self.r = rect
        self.anim_updown = get_anim_iterator([0, 0, 0, 1, 2, 2, 2, 1, ], 7)
        self.anim_eye = get_anim_iterator([0,1,0,2,3,0,1,1,0,2,4,0,1,0,2,2,0,1,1,0,2,5,3,3],120)
        self.sprite = Sprite("gameengine/assets/spritesheet_enemy2.png", 6)

        self.pos = Vector2(rect.centerx, rect.centery)
        self.pos_start = self.pos.copy()
        self.v   = Vector2(0,0)


    def update(self):
        self.pos += self.v
        self.r.center = self.pos

        if pls := self.game.get_actors_by_type("Player"):
            p = pls[0] # Only 1 Player can exist
            v = Vector2(self.r.center)
            vp = Vector2(p.r.center)

            # Distance to Player
            d = (vp - v).length()
            # Am I near to the Player (100px)?
            if d < self.AWARE_RADIUS:
                direction = vp-v
                if direction.length() > 0.0:
                    direction.normalize_ip()
                    self.v = self.v+(direction*0.06)
            else:
                # brake if player far away
                self.v *= 0.97
            if d < 20:
                p.kill()
                self.pos = self.pos_start.copy()
                self.v.scale_to_length(0.0)
        else:
            # brake if player not existent
            self.v *= 0.99
        # Speed limit
        if self.v.length() > MoonEnemy.MAX_SPEED:
            self.v.scale_to_length(MoonEnemy.MAX_SPEED)


    def draw(self, surface, camera=None):
        self.sprite.frame_no = next(self.anim_eye)
        self.sprite.draw(surface, self.r.move(-camera.x, -camera.y + next(self.anim_updown)))
        if self.game.debug:
            draw_text(surface, f"v={self.v.length():3.3f}",self.pos.x-camera.x-20, self.pos.y-camera.y+25, "red")
            center = self.r.move(-camera.x,-camera.y).center
            #pygame.draw.circle(surface, "yellow", center,self.AWARE_RADIUS, 1)
            pygame.gfxdraw.filled_circle(surface, center[0], center[1], self.AWARE_RADIUS, (255,0,255,40))

####################################################################################################
class Diamond(Actor):

    def __init__(self, game,rect):
        super().__init__(game)
        self.spr = Sprite("gameengine/assets/spritesheet_diamond.png", 1)
        self.snd = pygame.mixer.Sound("gameengine/assets/sound/sfx_3.wav")
        self.r = rect

    def update(self):
        if pls := self.game.get_actors_by_type("Player"):
            p = pls[0] # Only 1 Player can exist
            if self.r.colliderect(p.r):
                self.game.add_actor(SimplePopup(self.game, self.r.center))
                #self.snd.play()
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
        self.sf_old = pygame.surface.Surface((480,256))

    def draw(self, surface, camera=None):
        #self.sf_old = surface
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
        temp = surface.copy()
        self.sf_old.set_alpha(50)
        surface.blit(self.sf_old, (1,1))
        surface.blit(self.sf_old, (-1,-1))
        self.sf_old = temp

####################################################################################################

class ElectricityEffect(Actor):
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
        self.script.add_step(self.down, frames=10)
        self.script.add_step(self.wait, frames=280)
        self.script.add_step(self.up,  frames=10)
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

def create_fragments(game, x: int, y: int):
    for a in range(randint(1,3)):
        game.add_actor(PhysicsParticle(
            game,
            pos=Vector2(x, y),
            angle=Vector2(0, 1).rotate(randint(-90, 90)),
            speed=randint(0, 50),
            color=pygame.Color("gray"),
            size = 1,
            maxlife= 100

        ))

def create_player_explosion(game, x: int, y: int):
    for a in range(120):
        game.add_actor(PhysicsParticle(
            game,
            pos=Vector2(x, y),
            angle=Vector2(0, -1).rotate(randint(-30,30)),
            speed=randint(35, 380),
            color=pygame.Color("white"),
            size=3,
            maxlife=250 + randint(0, 50)
        ))


class PhysicsParticle(Actor):
    """
    A Physics Particle has a collision point instead of a rect and
    is used for Shrapnells, Dirt, Bubbles etc.
    Collision is used for WALL-Tiles, Stairs etc.
    """
    DELTA = 1 / 60

    def __init__(self, game, pos: Vector2, angle: Vector2, speed: float, color: pygame.Color, size: int, maxlife:int):
        super().__init__(game)
        self.pos = pos
        self.vel = angle * speed
        self.acc = Vector2(0, 5.50)  # Gravity
        self.color = color
        self.size = size
        self.maxlife = maxlife

    def update(self):
        self.maxlife -= 1
        if self.maxlife <= 0:
            self.dirty = True
        self.vel += self.acc
        self.move(self.vel * self.DELTA)

    def move(self, vec: Vector2):
        self.move2(vec.x, 0)
        self.move2(0, vec.y)

    def move2(self, x, y):
        assert(not(x and y), "move2 only x or y set")
        if x != 0.0 or y != 0.0:
            # new pos
            npos = self.pos+Vector2(x,y)
            # cr Collision-Rect
            cr = self.game.map.get_collision_tile_at_point(npos,Tile.WALL)
            if cr:
                if x > 0:
                    npos.x = cr.left-1
                    self.vel.x = -self.vel.x*0.3
                elif x < 0:
                    npos.x = cr.right+1
                    self.vel.x = -self.vel.x*0.3
                elif y > 0:
                    npos.y = cr.top-0.5 # -0.5 so that pixels don't start swinging
                    self.vel.y = -self.vel.y*0.4
                    self.vel.x *= 0.6 # Reibung
                elif y < 0:
                    npos.y = cr.bottom+1
                    self.vel.y = -self.vel.y
            self.pos = npos

    def draw(self, sf, cam=None):
        pos = self.pos.x-cam.x, self.pos.y-cam.y
        pygame.gfxdraw.filled_circle(sf, int(pos[0]),int(pos[1]), self.size+1,(255,255,255,20))
        pygame.gfxdraw.filled_circle(sf, int(pos[0]),int(pos[1]), self.size+3,(255,255,255,10))
        pygame.gfxdraw.filled_circle(sf, int(pos[0]),int(pos[1]), self.size+6,(255,255,255,10))
        if self.size == 1:
            pygame.draw.line(sf, self.color, pos, pos, 1)
        else:
            pygame.draw.circle(sf, self.color, pos, radius=self.size-1, width=0)


