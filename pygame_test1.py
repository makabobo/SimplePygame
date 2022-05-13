import pygame
import pygame.draw
import ctypes
import sys

ctypes.windll.user32.SetProcessDPIAware()
pygame.init()

screen = pygame.display.set_mode((480, 256), pygame.SCALED | pygame.RESIZABLE, vsync=1)
draw_surface = pygame.Surface((480,256))

clock = pygame.time.Clock()

cfuture_img = pygame.image.load("./img_tests/cfuture.png")
test_img1 = pygame.image.load("./img_tests/testimg_index_transparency.png").convert_alpha()
test_img2 = pygame.image.load("./img_tests/testimg_rgb_transparency.png").convert_alpha()

x = 0.0
testno = 1

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            testno += 1
            if testno>2:
                testno=1

    if testno==1:
        cfuture_img.set_alpha(255)
        x += 0.5
        x %= 200

        draw_surface.fill("white")
        draw_surface.blit(cfuture_img, (0, 0))
        draw_surface.blit(test_img1, (50+x, 50), None, pygame.BLEND_ALPHA_SDL2)
        draw_surface.blit(test_img2, (50+x, 50+x))

    if testno==2:
        draw_surface.fill("black")
        cfuture_img.set_alpha(10)
        for x in range(5):
            for y in range(5):
                draw_surface.blit(cfuture_img, (-3+x,-3+y))

#        draw_surface.blit(cfuture_img, (0, 0))

    screen.blit(draw_surface, (0, 0))
    pygame.display.flip()
    delta = clock.tick_busy_loop(60)
