import pygame
from .menu import *
from .input import *
from .tile import *
from .prefab import *
from .camera import Camera


class Game:
    def __init__(self):
        self.map = None
        self.actors = []
        self.controller = Controller()
        self.menu = None
        self.debug = False
        self.debug_msg = ""
        self.camera = Camera(self)
        self.update_func = None

        self.screen = pygame.display.set_mode((480, 256), pygame.SCALED | pygame.RESIZABLE, vsync=1)
#        self.screen = pygame.display.set_mode((480, 256), pygame.RESIZABLE, vsync=1)
        self.draw_surface = pygame.Surface((480, 256))
        self.__clock = pygame.time.Clock()
        self.update_times = 120*[0]

    def load_map(self, path):
        self.map = Tilemap(self)
        self.map.load(path)

    def start(self):
        while 1:
            time_before_update = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.menu is None:
                        self.menu = MainMenu(self)
                    else:
                        self.menu = None
            #########
            # TICK
            #########

            # Controller muss als erstes tick() erhalten
            self.controller.tick()

            if self.menu:
                self.menu.update()
            else:
                for a in self.actors:
                    a.update()

                self.camera.update()

                # Delete "old/dirty" Actors
                self.actors = [a for a in self.actors if a.dirty is False]

                if self.map:
                    self.map.update()
                if self.update_func:
                    self.update_func()

            #########
            # DRAW
            #########
            self.draw_surface.fill("black")

            if self.map:
                self.map.draw(self.draw_surface, self.camera)

            for a in self.actors:
                a.draw(self.draw_surface, self.camera)

            if self.menu:
                self.menu.draw(self.draw_surface)

            if self.debug:
                draw_text(self.draw_surface, f"FPS {self.__clock.get_fps():>3.1f}", 420, 3, "darkred")
                pygame.draw.rect(self.draw_surface, "black", (0,0,200,11), 0)
                draw_text(self.draw_surface, self.debug_msg, 10, 1, "white")

                del self.update_times[0]
                self.update_times.append((pygame.time.get_ticks()-time_before_update))
                draw_frame_times(self.draw_surface, self.update_times)

            self.screen.blit(self.draw_surface, (0, 0))
            pygame.display.flip()

            self.__clock.tick(60)





