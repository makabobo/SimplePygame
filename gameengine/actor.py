import pygame
from .tile import Tile
from .animation import Animation
from .util import *
from pygame import Vector2


class Sprite:
    """
    Sprite, das aus mehreren Frames bestehen kann.
    Eigenschaften:
      - texture  = Ursprungsbild mit verschiedenen Frames
      - frame_no = Aktuelles Frame
      - flip     = Horizontal gespiegelt anzeigen?
      - alpha    = Alpha-Wert 0-255 (0=durchsichtig 255=100%Deckung)
    """
    def __init__(self, img_path:str, framecount:int = 1):
        self.texture = None
        self.frame_no = 0
        self.flip = False
        self.alpha = 255
        self.width = 0
        self.height = 0

        self.__frames = []
        self.__frames_flipped = []
        self.texture = pygame.image.load(img_path)
        if framecount <= 1:
            self.__frames.append(self.texture)
        else:
            if self.texture.get_width() % framecount != 0:
                print("Fehler bei Texture-Verarbeitung..")
                exit()
            self.width = self.texture.get_width() / framecount
            self.height = self.texture.get_height()
            for i in range(framecount):
                frame = pygame.Surface((self.width, self.texture.get_height()), pygame.SRCALPHA)
                frame.blit(self.texture, (0, 0), pygame.Rect(i * self.width, 0, self.width, self.texture.get_height()))
                self.__frames.append(frame)
                frame_flipped = pygame.transform.flip(frame, True, False)
                self.__frames_flipped.append(frame_flipped)

    def draw(self, surface, pos):
        if not self.flip:
            self.__frames[self.frame_no].set_alpha(self.alpha)
            surface.blit(self.__frames[self.frame_no], pos)
        else:
            self.__frames_flipped[self.frame_no].set_alpha(self.alpha)
            surface.blit(self.__frames_flipped[self.frame_no], pos)


class Actor:

    def __init__(self, game):
        self.dirty = False
        self.game = game

    def tick(self):
        pass

    def draw(self, surface, delta, camera=None):
        pass


class PhysicsBody(Actor):
    def __init__(self, x, y, w, h, game):
        super().__init__(game)
        self.r = pygame.Rect(x, y, w, h)
        self.xa = 0.0  # Acceleration
        self.ya = 0.4
        self.xs = 0.0  # speed
        self.ys = 0.0

    def move_soft(self, xd, yd, ignore_stairs=False):
        blocked = False
        if xd:
            if not self.move2(xd, 0):
                blocked = True
                self.xs = 0.0
        if yd:
            if not self.move2(0, yd):
                blocked = True
                self.ys = 0.0
        return not blocked

    def move2(self, xd, yd):
        if xd != 0 and yd != 0:
            raise Exception("Move2 kann pro Aufruf nur 1 Achse bewegen")
        tr = self.r.move(xd, yd)  # tr=target_rect
        blocked = False
        if xd != 0 or yd != 0:

            collision_rects = []
            if self.game.map:
                collision_rects = self.game.map.get_collision_tiles(tr, Tile.WALL)
            #collision_rects += ([w.r for w in moving_blocks if w.r.colliderect(tr)])

            for collider in collision_rects:

                blocked = True
                # Kollision rechts?
                if xd > 0:
                    if tr.right > collider.left:
                        tr.right = collider.left
                # Kollision links?
                if xd < 0:
                    if tr.left < collider.right:
                        tr.left = collider.right
                # Kollision Boden?
                if yd > 0:
                    if tr.bottom > collider.top:
                        tr.bottom = collider.top
                # Kollision mit Decke?
                if yd < 0:
                    if tr.top < collider.bottom:
                        tr.top = collider.bottom


            # Variante mit beweglichen Platformen
            # if yd > 0:
            #     for stair_tile in self.map.get_collision_tiles(tr, Tile.STAIR) + [x.r for x in moving_platforms]:
            #         if tr.colliderect(stair_tile) and tr.bottom - yd-1 <= stair_tile.top:
            #             tr.bottom = stair_tile.top

            # Wenn Bewegung nach unten?
            if yd > 0:
                for stair_tile in self.game.map.get_collision_tiles(tr, Tile.STAIR):
                    if tr.colliderect(stair_tile) and tr.bottom - yd <= stair_tile.top:
                        tr.bottom = stair_tile.top
        self.r = tr
        return not blocked

    # moving_blocks
    # moving_platforms: Bewegliche Treppe/Platform
    # physics objects: Soft-Objekt (Player)



    # def move_hard(self, xd, yd) -> None:
    #     """ hard_move: moves by force, colliding elements were moved or squashed"""
    #     rect_dest = self.r.move(xd, yd)
    #     for pe in physics_elements:
    #         # Kollidierende Objekte verschieben
    #         if pe.r.colliderect(rect_dest):
    #             if not pe.move2(xd, yd):
    #                 vp.shake()  # Zerquetscht
    #         # Darauf stehende Objekte verschieben
    #         if not pe.r.colliderect(rect_dest) and pe.r.move(0, 1).colliderect(rect_dest):
    #             pe.move2(xd, yd)
    #     self.r = rect_dest

    def check_on_floor(self):
        """ detects ground """
        # "Bodenplatte des Players berechnen
        rg = self.r.move(0,1)
        collision_rects = self.game.map.get_collision_tiles(rg, Tile.WALL)
        # collision_rects += ([w.r for w in moving_platforms if w.r.colliderect(tr)])
        for cr in collision_rects:
            if test_rect_lying_on_rect(self.r, cr):
                return True
        return False

    def check_on_stair(self):
        """ detects ground """
        rg = self.r.move(0,1)
        collision_rects = self.game.map.get_collision_tiles(rg, Tile.STAIR)
        # collision_rects += ([w.r for w in moving_platforms if w.r.colliderect(tr)])
        # collision_rects += ([w.r for w in moving_blocks if w.r.colliderect(tr)])
        for cr in collision_rects:
            if test_rect_lying_on_rect(self.r, cr):
                return True
        return False

    def tick(self):
        # Schwerkraft simulieren
        if not self.check_on_floor() and not self.check_on_stair():
            self.ys += self.ya
        if self.ys > 7.0:
            self.ys = 7.0

        self.move_soft(int(self.xs), int(self.ys))

    def collides_with(self, other) -> bool:
        return self.r.colliderect(other.r)

    def stands_on(self, other) -> bool:
        pass


class Player(PhysicsBody):
    def __init__(self, x, y, game):
        super().__init__(x, y, 12, 34, game)
        self.playersprite = Sprite("gameengine/assets/player.png", 6)

        self.walk_anim = get_anim_iterator([0,1,2,1],10)
        self.stand_anim = get_anim_iterator([3,4],20)
        self.jump_anim = get_anim_iterator([5],60)

        self.current_anim = self.stand_anim

        self.on_floor = self.check_on_floor()
        self.on_stair = self.check_on_stair()

    def check_status(self):
        self.on_floor = self.check_on_floor()
        self.on_stair = self.check_on_stair()

    def tick(self):
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
        super().tick()

    def draw(self, surface, delta, camera=None):
        if self.game.debug:
            pygame.draw.rect(surface, "red", self.r.move(-camera.x, -camera.y), 1)

        self.game.debug_msg = f"ys={self.ys:0.5f}" #, pos={self.x},{self.y}"

        if self.ys != 0.0:
            self.current_anim = self.jump_anim
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
