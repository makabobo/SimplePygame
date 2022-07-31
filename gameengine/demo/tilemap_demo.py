from gameengine import *


class MyActor(Actor):

    def __init__(self):
        super().__init__()
        self.x = 0

    def tick(self, game):
        self.x += 1
        self.x %= 480

    def draw(self, surface, delta):
        pygame.draw.circle(surface, "red", (self.x,100), 15, 2)

game.load_map("./assets/test-map.tmj")
game.actors.append(MyActor())
game.start()





