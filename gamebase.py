from pygame.font import *
import pygame.draw
import ctypes
import sys
from random import randint

pygame.init()
ctypes.windll.user32.SetProcessDPIAware()
font = Font("mago3.ttf", 16, bold=False, italic=False)

screen = pygame.display.set_mode((480, 256), pygame.SCALED | pygame.RESIZABLE, vsync=1)
draw_surface = pygame.Surface((480, 256))
clock = pygame.time.Clock()

actors = []

print_map = {}

def draw_text(text, x, y, color="white"):
    global font
    global print_map

    if (text, color) in print_map.keys():
        draw_surface.blit(print_map[(text, color)], (x, y))
    else:
        s = font.render(text, False, color)
        print_map[(text, color)] = s
        draw_surface.blit(s, (x, y))


class Actor:
    def tick(self, timedelta):
        pass

    def draw(self):
        pass

class Controller:
    def __init__(self):
        self.a = 0
        self.b = 0
        self.menu = 0
        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0

    def tick(self, delta):
        if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_RETURN]:
            self.a += 1
        else:
            self.a = 0

        if pygame.key.get_pressed()[pygame.K_s]:
            self.b += 1
        else:
            self.b = 0

        if pygame.key.get_pressed()[pygame.K_UP]:
            self.up += 1
        else:
            self.up = 0

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.down += 1
        else:
            self.down = 0

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.left += 1
        else:
            self.left = 0

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.right += 1
        else:
            self.right = 0

class Menu(Actor):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.pos = 0
        self.items = []
        pass

    def tick(self, delta):
        # Clicked
        if controller.a == 1:
            #sound_select2.play()
            self.clicked(self.items[self.pos])
        # Up
        if controller.down == 1:
            self.pos += 1
            #sound_select1.play()
        if self.pos >= len(self.items):
            self.pos = 0
        # Down
        if controller.up == 1:
            self.pos -= 1
            #sound_select1.play()
        if self.pos == -1:
            self.pos = len(self.items) - 1

    def draw(self):
        x = 160
        y = 110
        yd = 15
        pygame.draw.rect(draw_surface, "darkgray", pygame.Rect(140,80, 200,100),2)
        num = 0
        draw_text(self.name, x+44, 80+5, "darkgray")
        for item in self.items:
            if num == self.pos:
                # Ausgewählter Menüpunkt
                draw_text(">", x + 2, y, "white")
                draw_text(item[0], x + 10, y, "white")
                draw_text(item[1], x + 140, y, "white")
            else:
                # Nicht ausgewählte Menüpunkte
                draw_text(item[0], x + 10, y, "red")
                draw_text(item[1], x + 140, y, "red")
            y += yd
            num += 1

    def clicked(self, item):
        pass

debug = False

class MainMenu(Menu):
    def __init__(self):
        super().__init__("Main Menu")
        self.items = [["TOGGLE FULLSCREEN",""], ["DEBUG","off"], ["EXIT",""]]

    def clicked(self, item):
        global debug, draw_surface
        if item[0] == "TOGGLE FULLSCREEN":
            pygame.display.toggle_fullscreen()
        if item[0] == "DEBUG":
            if debug:
                debug = False
                self.items[1][1] = "off"
            else:
                debug = True
                self.items[1][1] = "on"
        if item[0] == "EXIT":
            sys.exit()


controller = Controller()
menu = None


def start():
    delta = 0.0
    global menu
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if menu == None:
                    menu = MainMenu()
                else:
                    menu = None

        controller.tick(delta)

        for _ in actors:
            _.tick(delta)

        if menu:
            menu.tick(delta)

        draw_surface.fill("black")
        for _ in actors:
            _.draw()

        if menu is None:
            pass
        else:
            menu.draw()

        draw_text(f"FPS {clock.get_fps():>3.1f}", 420, 3, "darkred")

        screen.blit(draw_surface, (0, 0))
        pygame.display.flip()
        delta = clock.tick(60)

