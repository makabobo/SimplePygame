import sys

from .actor import *
from .util import *

class Menu(Actor):
    def __init__(self, name, game):
        super().__init__()
        self.name = name
        self.game = game
        self.pos = 0
        self.items = []
        pass

    def tick(self, game):
        # Clicked
        if game.controller.a == 1:
            # sound_select2.play()
            self.clicked(self.items[self.pos])
        # Up
        if game.controller.down == 1:
            self.pos += 1
            # sound_select1.play()
        if self.pos >= len(self.items):
            self.pos = 0
        # Down
        if game.controller.up == 1:
            self.pos -= 1
            # sound_select1.play()
        if self.pos == -1:
            self.pos = len(self.items) - 1

    def draw(self, surface, delta):
        x = 160
        y = 110
        yd = 15
        pygame.draw.rect(surface, "black", pygame.Rect(140, 80, 200, 100), 0)
        pygame.draw.rect(surface, "darkgray", pygame.Rect(140, 80, 200, 100), 2)
        num = 0
        draw_text(surface, self.name, x + 44, 80 + 5, "darkgray")
        for item in self.items:
            if num == self.pos:
                # Ausgewählter Menüpunkt
                draw_text(surface, ">", x + 2, y, "white")
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
        super().__init__("Main Menu", game)
        self.items = [["TOGGLE FULLSCREEN", ""], ["DEBUG", "off"], ["EXIT", ""]]

    def clicked(self, item):
        if item[0] == "TOGGLE FULLSCREEN":
            pygame.display.toggle_fullscreen()
        if item[0] == "DEBUG":
            if self.game.debug:
                self.game.debug = False
                self.items[1][1] = "off"
            else:
                self.game.debug = True
                self.items[1][1] = "on"
        if item[0] == "EXIT":
            sys.exit()

