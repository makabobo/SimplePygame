import pygame
from .tile import Tile
from .animation import Animation
from .util import test_rect_lying_on_rect


class Actor:

    def __init__(self, game):
        self.dirty = False
        self.game = game

    def tick(self):
        pass

    def draw(self, surface, delta, camera=None):
        pass

class SpriteActor(Actor):
    def __init__(self, x, y, w, h, tilemap, game):
        super().__init__(game)
        self.r = pygame.Rect(x, y, w, h)
        self.tilemap = tilemap
        self.xa = 0.0  # Acceleration
        self.ya = 0.4
        self.xs = 0.0  # speed
        self.ys = 0.0

    @property
    def x(self):
        return self.r.x

    @property
    def y(self):
        return self.r.y

    @property
    def w(self):
        return self.r.w

    @property
    def h(self):
        return self.r.h

    @property
    def centerx(self):
        return self.r.centerx

    @property
    def centery(self):
        return self.r.centery


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
            if self.tilemap:
                collision_rects = self.tilemap.get_collision_tiles(tr, Tile.WALL)
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
            #     for stair_tile in self.tilemap.get_collision_tiles(tr, Tile.STAIR) + [x.r for x in moving_platforms]:
            #         if tr.colliderect(stair_tile) and tr.bottom - yd-1 <= stair_tile.top:
            #             tr.bottom = stair_tile.top

            if yd > 0:
                for stair_tile in self.tilemap.get_collision_tiles(tr, Tile.STAIR):
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

    def on_floor(self):
        """ detects ground """
        # "Bodenplatte des Players berechnen
        rg = self.r.move(0,1)
        collision_rects = self.tilemap.get_collision_tiles(rg, Tile.WALL)
        # collision_rects += ([w.r for w in moving_platforms if w.r.colliderect(tr)])
        for cr in collision_rects:
            if test_rect_lying_on_rect(self.r, cr):
                return True
        return False

    def on_stair(self):
        """ detects ground """
        rg = self.r.move(0,1)
        collision_rects = self.tilemap.get_collision_tiles(rg, Tile.STAIR)
        # collision_rects += ([w.r for w in moving_platforms if w.r.colliderect(tr)])
        # collision_rects += ([w.r for w in moving_blocks if w.r.colliderect(tr)])
        for cr in collision_rects:
            if test_rect_lying_on_rect(self.r, cr):
                return True
        return False

    def tick(self):
        # Schwerkraft simulieren
        if not self.on_floor():
            self.ys += self.ya
        if self.ys > 7.0:
            self.ys = 7.0

        self.move_soft(self.xs, self.ys)

    def draw(self):
        pass

    def collides_with(self, other) -> bool:
        return self.r.colliderect(other.r)

    def stands_on(self, other) -> bool:
        pass


class Player(SpriteActor):
    def __init__(self, tilemap, x, y, game):
        super().__init__(x, y, 28, 40, tilemap, game)
        self.anim_right = Animation("./assets/player.png", 24, False)
        self.anim_left  = Animation("./assets/player.png", 24, True)

    def tick(self):
        on_floor = self.on_floor()  # wird mehrmals benötigt
        on_stair = self.on_stair()  # wird mehrmals benötigt

        self.game.debug_msg = f"on-floor={on_floor}" #, pos={self.x},{self.y}"

        if self.game.controller.left:
            self.xs = -2
        elif self.game.controller.right:
            self.xs = 2
        else:
            self.xs = 0
        # Springen
        if self.game.controller.a == 1 and not self.game.controller.down and (on_stair or on_floor):
            self.ys = -6.7


        # Von Treppe fallen lassen
        if self.game.controller.a == 1 and self.game.controller.down and on_stair:
            self.r.y += 1

        if self.game.controller.a == 0 and (on_stair or on_floor) and self.ys >= 0:
            self.ys = 0.0
        super().tick()

    def draw(self, surface, delta, camera=None):
        #pygame.draw.rect(draw_surface, "red", self.r.move(-camera.x, -camera.y), 1, 7)
        if self.game.debug:
            pygame.draw.rect(surface, "red", self.r.move(-camera.x, -camera.y), 1)

        self.anim_left.draw(surface, self.r.move(-camera.x, -camera.y-10), delta)
