import pygame
import sys
from math import *
from basecode import *


clock = pygame.time.Clock()


map = Tilemap()
map.load("./img/test_map.json")


player = Player(map, 300, 190)
physics_elements.append(player)

moving_platforms.append(MovingPlatform(190, 260, 64, 8, 190, 320))
moving_blocks.append(MovingBlock(130, 270, 30, 30, 130, 200))



moving_platforms.append(MovingPlatform(480, 260, 64, 8, 480, 650))
moving_blocks.append(MovingBlock(650, 240, 64, 8, 480, 600))



camera.follow(player)

debug = True

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key==pygame.K_q):
            sys.exit()
    # Tick ###########
    controller.tick()
    map.tick()
    for mp in moving_platforms+moving_blocks:
        mp.tick()
    player.tick()
    camera.tick()

    # Draw ###########
    screen.fill(map.backgroundcolor)
    map.draw()
    for scene in moving_platforms+moving_blocks:
        scene.draw()
    player.draw()

    if debug:
        draw_debug()

    piprint(message, 10, 240)
    messagecounter += 1
    if messagecounter >= 100:
        messagecounter = 0
        message = ""

    piprint(f"FPS {clock.get_fps():>3.1f}", 420,3, "darkred")
    clock.tick_busy_loop(60)
    pygame.display.flip()
