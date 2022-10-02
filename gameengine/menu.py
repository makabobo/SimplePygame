import sys

from .actor import *
from .util import *


class Menu(Actor):
    def __init__(self, name, game):
        super().__init__(game)
        self.name = name
        self.pos = 0
        self.items = []
        self.selection_bar = Sprite("./gameengine/assets/menu_selection_bar1.png")
        self.background_top = Sprite("./gameengine/assets/menu_top.png")
        self.background_bottom = Sprite("./gameengine/assets/menu_bottom.png")

        # Animator for the Selection-Bar (Fade in/out)
        self.fader = get_anim_iterator([30,80,130,180,230,255,230,180,130,80],6)

        # Animator for ">" Char (Moving left/right)
        self.arrow_animator = get_anim_iterator([0,0,0,0,0,0,0,0,1,2,3,4,4,4,4,3,2,1], 2)

    def update(self):
        # Clicked
        if self.game.controller.a == 1:
            # sound_select2.play()
            self.clicked(self.items[self.pos])
        # Up
        if self.game.controller.down == 1:
            self.pos += 1
            # sound_select1.play()
        if self.pos >= len(self.items):
            self.pos = 0
        # Down
        if self.game.controller.up == 1:
            self.pos -= 1
            # sound_select1.play()
        if self.pos == -1:
            self.pos = len(self.items) - 1

    def draw(self, surface, camera=None):
        x = 160
        y = 110
        yd = 15

        self.selection_bar.alpha = next(self.fader)

        pygame.draw.rect(surface, "black",    pygame.Rect(140, 80, 200, 100), 0)
        self.background_top.draw(surface, (142,80))
        self.background_bottom.draw(surface, (142,160))
        pygame.draw.rect(surface, "black", pygame.Rect(140, 80, 200, 100), 2)

        draw_text(surface, self.name, x + 44, 80 + 5, "darkgray")

        num = 0
        for item in self.items:
            if num == self.pos:
                self.selection_bar.draw(surface, (142, y-3))
                # Ausgewählter Menüpunkt
                draw_text(surface, ">", x-10 +next(self.arrow_animator), y, "white")
                draw_text(surface, item[0], x + 10, y, "white")
                draw_text(surface, item[1], x + 140, y, "white")
            else:
                # Nicht ausgewählte Menüpunkte
                draw_text(surface, item[0], x + 10, y, "red")
                draw_text(surface, item[1], x + 140, y, "red")
            y += yd
            num += 1

    def clicked(self, item):
        pass

class MainMenu(Menu):
    def __init__(self, game):
        super().__init__("MAIN MENU", game)
        self.items = [["TOGGLE FULLSCREEN", ""], ["DEBUG", "OFF"], ["EXIT", ""]]

    def clicked(self, item):
        if item[0] == "TOGGLE FULLSCREEN":
            pygame.display.toggle_fullscreen()
        if item[0] == "DEBUG":
            if self.game.debug:
                self.game.debug = False
                self.items[1][1] = "OFF"
            else:
                self.game.debug = True
                self.items[1][1] = "ON"
        if item[0] == "EXIT":
            sys.exit()

