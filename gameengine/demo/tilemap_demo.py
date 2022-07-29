from gameengine import *

class MyActor(Actor):
    def __init__(self):
        super().__init__()
        pass

    def draw(self, surface):
        pass


game.load_map("./test-map.tmj")
game.actors.append(MyActor())
game.start()


