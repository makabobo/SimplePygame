import gamebase as g


class MyActor(g.Actor):

    def __init__(self):
        super().__init__()
        self.x = 100
        self.y = 100
        self.time = 0.0

    def walk_up(self):
        self.x -= 1

    def walk_down(self):
        self.x += 1

    def tick(self, delta):
        self.time += delta

        if self.time < 3000:
            self.walk_down()

        elif 3000 <= self.time < 6000:
            self.walk_up()
        else:
            self.time = 0.0

    def draw(self):
        g.draw_text("HELLO!", self.x, self.y)

g.actors.append(MyActor())
g.start()
