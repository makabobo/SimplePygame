from gameengine import *


game.load_map("./assets/test-map.tmj")

p = Player(game.map, 327, 190, game)
game.actors.append(p)
game.camera.follow(p)
game.start()






