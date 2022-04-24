from dataclasses import dataclass



class Collider:
    def collide(self, a):
        print(f"collide {a}")

class Node2D:
    def get_rect(self):
        print("get_rect")



class MC(Collider, Node2D):
    def __init__(self):
        pass


m = MC()
m.get_rect()
m.collide(1)







