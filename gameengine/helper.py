""""Enthält unabhängige Funktionen, die für pygame-Spiele nützlich sein können"""
import pygame
import random

def random_color():
    return random.choice(palettecolors)


def distance(p1, p2):
    pass

def random_direction():
    pass

def random_speed():
    pass

def color_gradient(start, end):
    pass

def rainbow():
    retval = []
    for hue in range(0,360,10):
        c = pygame.Color("black")
        c.hsla = (hue,100,100,100)
        retval.append(c)
    return retval


palettecolors = ["black", "darkblue", "darkred", "darkgreen",
               "brown", "darkgrey", "lightgrey", "white",
               "red", "orange", "yellow", "green",
               "blue", "grey", "pink", "lightpink"]

if __name__ == "__main__":
    print(rainbow())