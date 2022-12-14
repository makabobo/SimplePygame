import pygame
from .menu import *
from .input import *
from .prefab import *
from .camera import Camera
from .playstats import PlayStat

SCREENFACTOR = 1

class Game:
    def __init__(self):
        self.map = None
        self.actors = []
        self.controller = Controller()
        self.menu = None
        self.debug = False
        self.debug_msg = ""
        self.camera = Camera(self)
        self.playstat = PlayStat(self)
        self.update_func = None
        self.post_process = None

        self.scaled_display = True
        self.screen = pygame.display.set_mode((480, 256), pygame.SCALED | pygame.RESIZABLE, vsync=1)
        self.draw_surface = pygame.Surface((480, 256))

        self.bg = pygame.image.load("gameengine/assets/img_tests/test_bg.png")
        self.bg = self.bg.convert_alpha()


        pygame.mixer.init()
#        sound_select1 = pygame.mixer.Sound(".gameengine/assets/sounds/sfx_3.wav")
        #sound_select2 = pygame.mixer.Sound(".gameengine/assets/sounds/sfx_7.wav")

        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

        self.__clock = pygame.time.Clock()
        self.update_times = 120*[0]

    def set_scaled_display(self, scaled):
        if scaled:
            self.scaled_display = scaled
            self.screen = pygame.display.set_mode((480, 256), pygame.SCALED | pygame.RESIZABLE, vsync=1)
            self.draw_surface = pygame.Surface((480, 256))
        else:
            self.scaled_display = scaled
            self.screen = pygame.display.set_mode((480*SCREENFACTOR, 256*SCREENFACTOR), pygame.RESIZABLE, vsync=1)
            self.draw_surface = pygame.Surface((480, 256))

    def load_map(self, path):
        self.map = Tilemap(self)
        self.map.load(path)

    def start(self):
        time_before_update = 0

        while 1:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.menu is None:
                        self.menu = MainMenu(self)
                    else:
                        self.menu = None
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
                    pass
            #########
            # UPDATE
            #########

            # Controller muss als erstes tick() erhalten
            self.controller.update()

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

                self.playstat.update()

            #########
            # DRAW
            #########
            #self.draw_surface.fill("black")
            pygame.gfxdraw.textured_polygon(self.draw_surface,
                                            [(0,0),(480,0),(480,256),(0,256)],
                                            self.bg,
                                            int(-self.camera.x*0.4),
                                            0)

            if self.map:
                self.map.draw(self.draw_surface, self.camera)

            for a in self.actors:
                a.draw(self.draw_surface, self.camera)

            if self.post_process:
                self.post_process.draw(self.draw_surface, self.camera)

            self.playstat.draw(self.draw_surface, self.camera)

            if self.menu:
                self.menu.draw(self.draw_surface)

            ################################################################################################
            if self.debug:
                self.camera.draw(self.draw_surface)
                # FPS
                draw_text(self.draw_surface, f"FPS {self.__clock.get_fps():>3.1f}", 420, 3, "darkred")

                # Debug Message
                pygame.draw.rect(self.draw_surface, "black", (0,0,200,11), 0)
                draw_text(self.draw_surface, self.debug_msg, 10, 1, "white")

                # Times history
                draw_frame_times(self.draw_surface, self.update_times)

                # Actors count
                self.debug_msg = f"Anzahl Actors = {len(self.actors)}"
                draw_text(self.draw_surface, f"Maus={self.camera.to_map_pos(pygame.mouse.get_pos())}", 10,20)
            ################################################################################################

            if self.scaled_display:
                self.screen.blit(self.draw_surface, (0, 0))
            else:
                s = pygame.transform.scale(self.draw_surface, (480 * SCREENFACTOR, 256 * SCREENFACTOR))
                self.screen.blit(s, (0,0))

            self.update_times.append((pygame.time.get_ticks() - time_before_update))
            del self.update_times[0]

            pygame.display.flip() # waits for vertical retrace (if vsync=1)
            self.__clock.tick(60)
            time_before_update = pygame.time.get_ticks()

    def on_camera_changed(self):
        pass

    def add_actor(self, a):
        self.actors.append(a)

    def get_actors_by_type(self, name: str):
        return [a for a in self.actors if type(a).__name__ == name]

    def remove_actor(self, a):
        self.actors.remove(a)
        pass



