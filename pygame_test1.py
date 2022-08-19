import pygame
import pygame.draw
import ctypes
import sys
import math

ctypes.windll.user32.SetProcessDPIAware()
pygame.init()

screen = pygame.display.set_mode((480, 256), pygame.SCALED | pygame.RESIZABLE, vsync=1)
draw_surface = pygame.Surface((480,256))

clock = pygame.time.Clock()

cfuture_img = pygame.image.load("./img_tests/cfuture.png")
test_img1 = pygame.image.load("./img_tests/testimg_index_transparency.png").convert_alpha()
test_img2 = pygame.image.load("./img_tests/testimg_rgb_transparency.png").convert_alpha()
test_img3 = pygame.image.load("./img_tests/indexed-colors.png")
#test_img3 = pygame.image.load("./img/player.png")

test_img3.set_palette_at(3, (0,0,255,50))


x = 0.0
testno = 1
degree = 0
counter = 0

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
        degree += 0.3
        counter += 1
        if counter >= 3:
            counter = 0
            #test_img3.scroll(1,2)
            #palette = [palette[1:16]]+[palette[0]]
            #test_img3.set_palette(palette)

        draw_surface.blit(test_img1, (50+x, 50), None, pygame.BLEND_ALPHA_SDL2)
        draw_surface.blit(test_img2, (50+x, 50+x))



        draw_surface.fill("#552222")
        draw_surface.blit(cfuture_img, (0, 0))
        sf = pygame.transform.rotozoom(test_img3, degree, 4 )
        #sf = pygame.transform.rotate(test_img3, degree)
        sf.set_alpha(210)
        x = 256 - (sf.get_width()/2)
        y = 128 - (sf.get_height()/2)

        draw_surface.blit(sf, (x,y))



    if testno==2:
        draw_surface.fill("black")
        cfuture_img.set_alpha(10)
        for x in range(0,5):
            for y in range(0,5):
                draw_surface.blit(cfuture_img, (-3+x,-3+y))

#        draw_surface.blit(cfuture_img, (0, 0))

    screen.blit(draw_surface, (0, 0))
    pygame.display.flip()
    delta = clock.tick_busy_loop(60)
