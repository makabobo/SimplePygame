from pygame.font import *
import pygame.draw
import ctypes
import sys
import logging

pygame.init()
ctypes.windll.user32.SetProcessDPIAware()


from .menu import *
from .camera import *
from .input import *
from .tilemap import *
from .game import Game

logging.getLogger().setLevel("INFO")

game = Game()


