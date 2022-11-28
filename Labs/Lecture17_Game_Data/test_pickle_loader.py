import pickle

class Npc:
    def __init__(self, name, x, y):
        self.name = name
        self.x, self.y = x, y

    def __repr__(self):
        return f'{self.name} {self.x} {self.y}'


with open('world.pickle', 'rb') as f:
    world = pickle.load(f)
    print(world)
