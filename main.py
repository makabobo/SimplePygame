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
moving_blocks.append(MovingBlock(130, 134, 30, 30, map, 134, 300))

moving_platforms.append(MovingPlatform(480, 260, 64, 8, map, 480, 650))
moving_blocks.append(MovingBlock(650, 240, 64, 8, map, 240, 300))

camera.follow(player)

menu = None

debug = True
degree = 0
delta = 0
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
            vp.fade_in()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_o:
            vp.fade_out()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if menu == None:
                menu = MainMenu()
            else:
                menu = None


    # Tick ###########
    controller.tick()
    if menu:
        menu.tick()
    else:
        map.tick()
        for _ in moving_platforms + moving_blocks + triggers:
            _.tick()
        player.tick(delta)
        camera.tick()
        vp.tick(delta)

    # Draw ###########
    draw_surface.fill(map.backgroundcolor)
    map.draw()
    for _ in moving_platforms+moving_blocks + triggers:
        _.draw()
    if menu is None:
        player.draw(delta)
    else:
        player.draw(0)
        menu.draw()



    piprint(f"FPS {clock.get_fps():>3.1f}", 420,3, "darkred")

    # After-Effects (Skalierung, Alpha oder Rotation)?
    if vp.alpha != 255 or vp.scale != 1.0 or vp.rotation_degree != 0.0:
        screen.fill(vp.bg_color)
        if vp.scale != 1.0 or vp.rotation_degree != 0.0:
            sf = pygame.transform.rotozoom(draw_surface, vp.rotation_degree, vp.scale)
        else:
            sf = draw_surface.copy()
        sf.set_alpha(vp.alpha)
        # Surface zentrieren
        screen.blit(sf, (-((sf.get_width() - 480) / 2), -((sf.get_height() - 256) / 2)))
    else:
        screen.blit(draw_surface,(0,0))

    pygame.display.flip()
    delta = clock.tick_busy_loop(60)

