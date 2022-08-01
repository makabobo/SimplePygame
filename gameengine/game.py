from .menu import *
from .input import *
from .tile import *
from .prefab import SimplePopup
import pygame
from .actor import Player


class Game:
    def __init__(self):
        self.map = None
        self.actors = []
        self.controller = Controller()
        self.menu = None
        self.debug = False
        self.debug_msg = ""


        self.screen = pygame.display.set_mode((480, 256), pygame.SCALED | pygame.RESIZABLE, vsync=1)
        self.draw_surface = pygame.Surface((480, 256))
        self.__clock = pygame.time.Clock()

    def load_map(self, path):
        self.map = Tilemap()
        self.map.load(path)

    def start(self):
        delta = 0.0
        self.actors.append(Player(self.map, 327,190))
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.menu is None:
                        self.menu = MainMenu(self)
                    else:
                        self.menu = None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.actors.append(SimplePopup(event.pos))

            #########
            # TICK
            #########

            # Controller muss als erstes tick() erhalten
            self.controller.tick()

            for a in self.actors:
                a.tick(self)

            # Delete "old/dirty" Actors
            self.actors = [a for a in self.actors if a.dirty is False]

            if self.menu:
                self.menu.tick(self)

            if self.map:
                self.map.tick(self)

            #########
            # DRAW
            #########
            self.draw_surface.fill("black")

            if self.map:
                self.map.draw(self.draw_surface, delta, pygame.Rect(0,0,480,256), self.debug)

            for a in self.actors:
                a.draw(self.draw_surface, delta)

            if self.menu:
                self.menu.draw(self.draw_surface, delta)

            if self.debug:
                draw_text(self.draw_surface, f"FPS {self.__clock.get_fps():>3.1f}", 420, 3, "darkred")
                pygame.draw.rect(self.draw_surface, "black", (0,0,200,30), 0)
                draw_text(self.draw_surface, self.debug_msg, 10, 10, "white")

            self.screen.blit(self.draw_surface, (0, 0))
            pygame.display.flip()
            delta = self.__clock.tick(60)





