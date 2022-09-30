class A:

    def __init__(self):
        self.x = 5

    def __get__(self, instance, owner):
        return self.x


class B:
    def __init__(self):
        self.y = 6

    a = A()


b = B()
print(b.a)

