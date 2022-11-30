import random
from pico2d import *
import game_world
import game_framework

class Ball:
    image = None
    eat_sound = None

    def __init__(self):
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y = random.randint(0, get_canvas_width()-1), random.randint(0, get_canvas_height()-1)

        # fill here


    def __getstate__(self):
        state = {'x': self.x, 'y': self.y}
        return state

    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)



    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass

    def handle_collision(self, other, grou):
        # fill here
        game_world.remove_object(self)
