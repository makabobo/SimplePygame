from gameengine import *


class MyActor(Actor):

    def draw(self, surface):
        pygame.draw.circle(surface, "red", (200,200), 50, 2)

game.load_map("./test-map.tmj")
game.actors.append(MyActor())
game.start()





