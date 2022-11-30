from pico2d import *

class Ground:
    def __init__(self):
        self.image = load_image('TUK_GROUND.png')
        # fill here

    def __getstate__(self):
        state = {}
        return state

    def __setstate__(self, state):
        self.__init__()

    def update(self):
        pass

    def draw(self):
        self.image.draw(1280 // 2, 1024 // 2)

