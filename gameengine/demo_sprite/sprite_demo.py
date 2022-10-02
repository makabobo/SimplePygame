from gameengine import *
from gameengine.actor import Actor
from pygame import *
from gameengine.util import draw_text


def fade_func(start, stop, step):
    while 1:
        for i in range(start, stop, step):
            yield i
        for i in range(stop, start, -step):
            yield i


def get_anim_iterator(array, frames):
    while 1:
        for a in array:
            for f in range(frames):
                yield a

############################################################
class Sprite(Actor):
    """
    Sprite, das aus mehreren Frames bestehen kann.
    Eigenschaften:
      - texture  = Ursprungsbild mit verschiedenen Frames
      - pos      = Position des Sprites (immer linksoben)
      - frame_no = Aktuelles Frame
      - flip     = Horizontal gespiegelt anzeigen?
      - alpha    = Alpha-Wert 0-255 (0=durchsichtig 255=100%Deckung)
    """
    def __init__(self, g):
        super().__init__(game)
        self.texture = None
        self.pos = Vector2(0, 0) # links oben, wird für surface.blit genutzt
        self.frame_no = None
        self.flip = False
        self.alpha = 255

        self.__frames = []
        self.__frames_flipped = []

    def load_image(self, img_path:str, framecount:int = 1):
        self.texture = pygame.image.load(img_path)
        if framecount <= 1:
            self.__frames.append(self.texture)
        else:
            if self.texture.get_width() % framecount != 0:
                print("Fehler bei Texture-Verarbeitung..")
                exit()
            width = self.texture.get_width() / framecount
            for i in range(framecount):
                frame = pygame.Surface((width, self.texture.get_height()), pygame.SRCALPHA)
                frame.blit(self.texture, (0, 0), pygame.Rect(i * width, 0, width, self.texture.get_height()))
                self.__frames.append(frame)
                frame_flipped = pygame.transform.flip(frame, True, False)
                self.__frames_flipped.append(frame_flipped)

    def draw(self, surface, delta, camera=None):
        self.__frames[self.frame_no].set_alpha(self.alpha)
        surface.blit(self.__frames[self.frame_no], self.pos)


############################################################
class MySprite(Sprite):
    def __init__(self,g):
        super().__init__(g)
        self.fader = fade_func(50,255,1)
        self.animator = get_anim_iterator([0,1,2,1],10)

    def tick(self):
        self.alpha = next(self.fader)
        self.frame_no = next(self.animator)

    def draw(self, surface, delta, camera=None):
        draw_text(surface, f"fade_val = {self.alpha}", 10, 30, color="white")
        super().draw(surface, delta)

sp = MySprite(game)

sp.load_image("./gameengine/assets/player.png", framecount=6)
sp.pos = Vector2(20,10)
game.actors.append(sp)
game.start()

