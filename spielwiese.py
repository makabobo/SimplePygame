from dataclasses import dataclass

@dataclass()
class MK:
    x: int = 4
    y: int = 2

    def sum(self, val:int = 3) -> int:
        return self.x+self.y+val

mk = MK(5,6)

print(mk.sum(4))



