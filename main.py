import pygame
import sys
from math import *
from basecode import *


clock = pygame.time.Clock()


scenes = []

map = Tilemap()
map.load("./img/test_map.json")


pl = Player(map, 32,208)
scenes.append(map)
camera.follow(pl)

debug = True

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key==pygame.K_q):
            sys.exit()
    #Tick
    controller.tick()
    for scene in scenes:
        scene.tick()
    pl.tick()
    camera.tick()

    # Draw
    screen.fill(map.backgroundcolor)
    for scene in scenes:
        scene.draw()
    pl.draw()

    if debug:
        draw_debug()

    clock.tick_busy_loop(60)
    pygame.display.flip()
