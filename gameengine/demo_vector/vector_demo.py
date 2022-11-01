from pygame import *
from gameengine import *
from gameengine.util import draw_text

class MyActor(Actor):
    def draw(self, sf, cam=None):
        # Center Offset

        co = Vector2(240,128)
        pygame.draw.line(sf, "gray", (240,0), (240,256), 1)
        pygame.draw.line(sf, "gray", (0,128), (480,128), 1)

        v1 = Vector2(50,50)
        v2 = Vector2(pygame.mouse.get_pos()-co)
        v3 = v1-v2

        pygame.draw.circle(sf, "red", v1+co, radius=5, width=1)
        draw_text(sf, f"v1 {str(v1)}", v1.x+240, v1.y+138, "red")

        pygame.draw.circle(sf, "blue", v2+co, radius=5, width=1)
        draw_text(sf, f"v2 {str(v2)}", v2.x+240, v2.y+138, "blue")

        pygame.draw.circle(sf, "green", v3+co, radius=5, width=1)
        draw_text(sf, f"v3=v1-v2 {str(v3)}", v3.x+240, v3.y+138, "green")

        try:
            v3.normalize_ip()
        except:
            v3 = Vector2(0,0)
        for i in range(int(v3.length()*12)):
            pygame.draw.circle(sf, "white", v2+v3*i+co, 1)

game.add_actor(MyActor(game))

game.debug=True
game.start()


