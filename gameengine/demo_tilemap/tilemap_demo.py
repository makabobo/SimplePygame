import sys

from gameengine import *
from gameengine.prefab import *

startpos = None

def update():
    for t in game.triggers:
        if p.r.colliderect(t.r):
            p.set_pos(startpos)


# Map laden
game.load_map("gameengine/assets/test-map.tmj")

# Trigger aus Object-Layer lesen
game.triggers = []
for obj in game.map.get_objects("GameObjects", "DEADZONE"):
    tr = TriggerRect(game, obj.r)
    game.actors.append(tr)
    game.triggers.append(tr)


for obj in game.map.get_objects("GameObjects", "ENEMY1"):
    me = MoonEnemy(game, obj.r.move(0,-obj.r.height))
    game.actors.append(me)
    #game.triggers.append(tr)


# Start-Position aus Object-Layer lesen und setzen
ps = game.map.get_objects("GameObjects", "PLAYERSTART")
assert len(ps) == 1, "Kein PLAYERSTART gefunden."
startpos = ps[0].r.topleft
p = Player(game)
p.set_pos(startpos)

# Import Camera-Corridors from Object-Layer
for cam in game.map.get_objects("Camera"):
    assert cam.type == "Rect", "Camera-Object Layer enthält Object welches nicht vom Typ 'Rect' ist"
    game.camera.add_corridor(cam.r)

game.actors.append(p)
game.camera.follow(p)
game.update_func = update
game.start()


