import pygame.time

import gameengine.util
from gameengine import *
from pygame import *
from random import random, randint

X = 0
Y = 1
XS = 2
YS = 3
LIFE = 4
COLOR = 5


class ParticleSystem(Actor):

    def __init__(self, game):
        super().__init__(game)
        self.particles = []
        self.dummy = 0

    def update(self):
        # New Particle
        for x in range(11):
            self.particles.append([10, 100,
                                   #[float(pygame.mouse.get_pos()[0]), float(pygame.mouse.get_pos()[1]), # Position
                                   30*random(), 5*random()-8.5,  # SPEED
                                   100,
                                   gameengine.util.random_color()
                                   ])

        # Particle update
        for p in self.particles:
            spd = 0.17
            p[YS]     += (0.92*spd)
            p[Y]      += p[YS]*spd
            p[LIFE]   -= 1
            p[X]      += p[XS]*spd
            p[XS]     *= 0.999
            if p[LIFE] == 0:
                self.particles.remove(p)
        self.game.debug_msg=f"# of particles: {len(self.particles)}"

    def draw(self, sf, camera = None):
        for p in self.particles:
            c = pygame.Color("black")
            c.hsva = (210,100,p[LIFE]/2,100)
            draw.circle(sf, c, (p[X], p[Y]), 2, False)


a = ParticleSystem(game)
game.actors.append(a)
game.debug=True
game.start()
