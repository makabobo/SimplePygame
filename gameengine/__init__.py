import ctypes
import pygame.draw

pygame.init()
ctypes.windll.user32.SetProcessDPIAware()

from .menu import *
from .camera import *
from .input import *
from .tile import *
from .game import Game
from .animation import *

logging.getLogger().setLevel("INFO")

game = Game()


