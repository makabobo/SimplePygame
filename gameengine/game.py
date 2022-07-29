from .menu import *
from .camera import *
from .input import *
from .tilemap import *
import pygame


class Game:
    def __init__(self):
        self.map = None
        self.actors = []
        self.controller = Controller()
        self.menu = None
        self.debug = False

        self.screen = pygame.display.set_mode((480, 256), pygame.SCALED | pygame.RESIZABLE, vsync=1)
        self.draw_surface = pygame.Surface((480, 256))
        self.__clock = pygame.time.Clock()

    def load_map(self, path):
        self.map = Tilemap()
        self.map.load(path)

    def start(self):
        delta = 0.0
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.menu is None:
                        self.menu = MainMenu()
                    else:
                        self.menu = None

            self.controller.tick(delta)

            for a in self.actors:
                a.tick(delta)

            if self.menu:
                self.menu.tick(delta, self.controller)

            if self.map:
                self.map.tick()

            self.draw_surface.fill("black")

            if self.map:
                self.map.draw(self.draw_surface, pygame.Rect(0,0,480,256))

            for a in self.actors:
                a.draw(self.draw_surface)

            if self.menu is None:
                pass
            else:
                self.menu.draw(self.draw_surface)

            if self.debug:
                draw_text(f"FPS {self.__clock.get_fps():>3.1f}", 420, 3, "darkred")

            self.screen.blit(self.draw_surface, (0, 0))
            pygame.display.flip()
            delta = self.__clock.tick(60)





