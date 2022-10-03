import sys

from gameengine import *
from gameengine.prefab import *

game.load_map("gameengine/assets/map_crater1.tmj")
game.triggers = []

def update():
    for t in game.triggers:
        if p.r.colliderect(t.r):
            p.kill()


game.update_func = update
ps = game.map.get_objects("PLAYERSTART")
assert len(ps) == 1, "Kein PLAYERSTART gefunden."

startpos = ps[0].r.topleft
p = Player(game)
p.set_pos(startpos)

for obj in game.map.get_objects("DEADZONE"):
    tr = TriggerRect(game, obj.r)
    game.actors.append(tr)
    game.triggers.append(tr)

game.actors.append(p)
game.camera.follow(p)
game.start()






