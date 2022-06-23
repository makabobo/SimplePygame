import pygame
import sys
from math import *
from base import *


clock = pygame.time.Clock()

#moving_platforms.append(MovingPlatform(190, 260, 64, 8, map, 190, 320))
#moving_blocks.append(MovingBlock(130, 134, 30, 30, map, 134, 300))

#moving_platforms.append(MovingPlatform(480, 260, 64, 8, map, 480, 650))
#moving_blocks.append(MovingBlock(650, 240, 64, 8, map, 240, 300))

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


    # Tick ###########
    controller.tick()
    if menu:
        menu.tick()
    else:
        map.tick()
        for _ in base.moving_platforms + moving_blocks + triggers:
            _.tick()
        base.player.tick(delta)
        camera.tick()
        vp.tick(delta)

    # Draw ###########
    draw_surface.fill(map.backgroundcolor)
    map.draw()
    for _ in base.moving_platforms + moving_blocks + triggers:
        _.draw()
    if menu is None:
        base.player.draw(delta)
    else:
        base.player.draw(0)
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

