import sys
import gameengine.util as util
from random import randint
from gameengine import *
from gameengine.prefab import *

startpos = None

def update():
    p = game.get_actors_by_type("Player")
    if p:
        p=p[0]
    for t in game.get_actors_by_type("TriggerRect"):
        if p:
            if p.r.colliderect(t.r):
                p.kill()
                p=None

# Map laden
game.load_map("gameengine/assets/tilemap/test-map.tmj")

# Trigger aus Object-Layer lesen
for obj in game.map.get_objects("GameObjects", "DEADZONE"):
    tr = TriggerRect(game, obj.r)
    game.add_actor(tr)

for obj in game.map.get_objects("GameObjects", "MOONENEMY"):
    me = MoonEnemy(game, obj.r.move(0,-obj.r.height))
    game.add_actor(me)

for obj in game.map.get_objects("GameObjects", "DIAMOND"):
    dia = Diamond(game, obj.r.move(0,-obj.r.height))
    game.add_actor(dia)


for obj in game.map.get_objects("GameObjects", "MOVINGPLATFORM"):
    mp = MovingPlatform(game, obj.r.move(0,-obj.r.height))
    game.add_actor(mp)

# Import Camera-Corridors from Object-Layer
for cam in game.map.get_objects("Camera"):
    assert cam.type == "Rect", "Camera-Object Layer enthält Object welches nicht vom Typ 'Rect' ist"
    game.camera.add_corridor(cam.r)




def insert_new_player(game):
    ps = game.map.get_objects("GameObjects", "PLAYERSTART")
    assert len(ps) == 1, "Kein PLAYERSTART gefunden."
    startpos = ps[0].r.topleft
    p = Player(game)
    game.add_actor(p)
    p.add_killed_listener(on_player_killed)
    p.set_pos(startpos)
    game.camera.follow(p)

def on_player_killed(game):
    seq = GameOverSquence(game)
    seq.add_finished_listener(on_gameover_finish)
    game.add_actor(seq)

def on_gameover_finish(game):
    insert_new_player(game)



#game.post_process = WaterEffect(game)
#game.post_process = ElectricityEffect(game)

insert_new_player(game)

game.update_func = update
game.start()


