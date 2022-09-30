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


class NewSprite(Actor):
    def __init__(self, g):
        super().__init__(game)
        self.image = None
        self.pos = Vector2(0, 50)
        self.h_frames = 1
        self.frame_no = None
        self.frames = []
        self.frames_flipped = []
        self.flip = False
        self.alpha = 255
        self.fader = fade_func(50,255,1)
        self.animator = get_anim_iterator([0,1,2,1],10)

    def load_image(self, img_path:str, framecount:int = 1):
        self.image = pygame.image.load(img_path)
        if framecount <= 1:
            self.frames.append(self.image)
        else:
            if self.image.get_width() % framecount != 0:
                print("Fehler bei Texture-Verarbeitung..")
                exit()
            width = self.image.get_width() / framecount
            for i in range(framecount):
                frame = pygame.Surface((width, self.image.get_height()), pygame.SRCALPHA)
                frame.blit(self.image, (0, 0), pygame.Rect(i * width, 0, width, self.image.get_height()))
                self.frames.append(frame)
                frame_flipped = pygame.transform.flip(frame, True, False)
                self.frames_flipped.append(frame_flipped)

    def tick(self):
        self.alpha = next(self.fader)
        self.frame_no = next(self.animator)

    def draw(self, surface, delta, camera=None):
        surface.fill("gray")
        draw_text(surface, f"fade_val = {self.alpha}", 10, 30, color="white")
        self.frames[self.frame_no].set_alpha(self.alpha)
        surface.blit(self.frames[self.frame_no], self.pos)


sp = NewSprite(game)

sp.load_image("./gameengine/assets/player.png", framecount=6)
sp.pos = Vector2(20,10)
game.actors.append(sp)
game.start()

