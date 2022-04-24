import pygame
import sys
from math import *
from basecode import *


clock = pygame.time.Clock()



map = Tilemap()
map.load("./img/test_map.json")

player = Player(map, 300, 190)
physics_elements.append(player)

moving_platforms.append(MovingPlatform(190, 260, 64, 8, map, 190, 320))
moving_blocks.append(MovingBlock(130, 270, 30, 30, map, 130, 200))

moving_platforms.append(MovingPlatform(480, 260, 64, 8, map, 480, 650))
moving_blocks.append(MovingBlock(650, 240, 64, 8, map, 480, 600))

camera.follow(player)

debug = True
degree = 0

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key==pygame.K_q):
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key==pygame.K_p:
            degree += 2
        if event.type == pygame.KEYDOWN and event.key == pygame.K_o:
            degree -= 2

    # Tick ###########
    controller.tick()
    map.tick()
    for mp in moving_platforms+moving_blocks:
        mp.tick()
    for t in triggers:
        t.tick()
    player.tick()
    camera.tick()

    # Draw ###########
    draw_surface.fill(map.backgroundcolor)
    map.draw()
    for scene in moving_platforms+moving_blocks:
        scene.draw()

    for t in triggers:
        t.draw()

    player.draw()

    if debug:
        draw_debug()


    degree+=0.03
    rot = sin(degree)*3

    piprint(f"FPS {clock.get_fps():>3.1f}", 420,3, "darkred")
    piprint(f"Degree: {rot:3.1f}", 10, 10)
    sf = pygame.transform.rotozoom(draw_surface, rot, 2.0)
    screen.blit(sf,(-((sf.get_width()-480)/2),-((sf.get_height()-256)/2)))

    pygame.display.flip()
    clock.tick_busy_loop(160)
