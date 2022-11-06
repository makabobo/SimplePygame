import pygame
from .tile import Tile
from .util import *
import gameengine
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

        self.texture.convert_alpha()
        if framecount <= 1:
            self.__frames.append(self.texture)
        else:
            if self.texture.get_width() % framecount != 0:
                print("Sprite: Fehler bei Texture-Verarbeitung..")
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

    def update(self):
        pass

    def draw(self, surface, camera=None):
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

    def collided_top(self):
        pass

    def collided_bottom(self):
        pass

    def move2(self, xd, yd):
        if xd != 0 and yd != 0:
            raise Exception("Move2 kann pro Aufruf nur 1 Achse bewegen")
        tr = self.r.move(xd, yd)  # tr=target_rect
        blocked = False
        if xd != 0 or yd != 0:

            collision_rects = []
            if self.game.map:
                collision_rects = self.game.map.get_collision_tiles_at_rect(tr, Tile.WALL)
             #   collision_rects += ([w.r for w in moving_blocks if w.r.colliderect(tr)])

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
                        self.collided_bottom()
                # Kollision mit Decke?
                if yd < 0:
                    if tr.top < collider.bottom:
                        tr.top = collider.bottom
                        self.collided_top()

            # Berücks. von Tile.STAIR und beweglichen Platformen
            #
            # Der Unterschied zu Tile.WALL ist, dass sich nur die oberste "Pixel-Zeile"
            # als "Mauer" verhält.
            if yd > 0:
                for stair_tile in self.game.map.get_collision_tiles_at_rect(tr, Tile.STAIR) + [mp.r for mp in self.game.get_actors_by_type("MovingPlatform")]:
                    if tr.colliderect(stair_tile) and tr.bottom - yd <= stair_tile.top:
                        tr.bottom = stair_tile.top
                        self.collided_bottom()

            # Wenn Bewegung nach unten?
            # if yd > 0:
            #     for stair_tile in self.game.map.get_collision_tiles(tr, Tile.STAIR):
            #         if tr.colliderect(stair_tile) and tr.bottom - yd <= stair_tile.top:
            #             tr.bottom = stair_tile.top
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
        collision_rects = self.game.map.get_collision_tiles_at_rect(rg, Tile.WALL)
        #collision_rects += ([w.r for w in moving_platforms if w.r.colliderect(tr)])
        for cr in collision_rects:
            if test_rect_lying_on_rect(self.r, cr):
                return True
        return False

    def check_on_stair(self):
        """ detects ground """
        rg = self.r.move(0,1)
        collision_rects = self.game.map.get_collision_tiles_at_rect(rg, Tile.STAIR)
        collision_rects += ([mp.r for mp in self.game.get_actors_by_type("MovingPlatform") if mp.r.colliderect(rg)])
        # collision_rects += ([w.r for w in moving_blocks if w.r.colliderect(tr)])
        for cr in collision_rects:
            if test_rect_lying_on_rect(self.r, cr):
                return True
        return False

    def update(self):
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

