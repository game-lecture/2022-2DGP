import pickle

data = [1,2,3,4,5]

with open('data.pickle', 'wb') as f:
    pickle.dump(data, f)

with open('data.pickle', 'rb') as f:
    read_data = pickle.load(f)

print(read_data)


class Npc:
    def __init__(self, name, x, y):
        self.name = name
        self.x, self.y = x, y

    def __repr__(self):
        return f'{self.name} {self.x} {self.y}'

yuri = Npc('Yuri', 100, 200)
jia = Npc('Jia', 200, 300)

with open('npc.pickle', 'wb') as f:
    pickle.dump(yuri, f)
    pickle.dump(jia, f)


with open('npc.pickle', 'rb') as f:
    y = pickle.load(f)
    j = pickle.load(f)

print(y)
print(j)

world = {'yuri': yuri, 'Jia': jia}
with open('world.pickle', 'wb') as f:
    pickle.dump(world, f)


print(world)
