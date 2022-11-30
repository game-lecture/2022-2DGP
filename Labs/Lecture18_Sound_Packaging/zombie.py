import random
import math
import game_framework
import game_world

from BehaviorTree import BehaviorTree, Selector, Sequence, Leaf
from pico2d import *
import game_world

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10


animation_names = ['Attack', 'Dead', 'Idle', 'Walk']

class Zombie:
    images = None
    font = None

    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                Zombie.images[name] = [load_image("./zombiefiles/female/"+ name + " (%d)" % i + ".png") for i in range(1, 11)]

    def __init__(self, name='NONAME', x=0, y=0, size=1):
        self.name = name
        self.x, self.y = x * PIXEL_PER_METER, y * PIXEL_PER_METER
        self.size = size
        if Zombie.font is None:
            Zombie.font = load_font('ENCR10B.TTF', 16)
        self.load_images()
        self.dir = random.random()*2*math.pi # random moving direction
        self.speed = 0
        self.timer = 1.0 # change direction every 1 sec when wandering
        self.frame = 0
        self.build_behavior_tree()

    def __getstate__(self):
        state = {'x': self.x, 'y': self.y, 'dir': self.dir, 'name': self.name, 'size': self.size}
        return state

    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)

    def calculate_current_position(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(50, self.x, get_canvas_width() - 50)
        self.y = clamp(50, self.y, get_canvas_height() - 50)

    def find_random_location(self):
        self.tx, self.ty = random.randint(50, get_canvas_width()-50), random.randint(50, get_canvas_height() - 50)
        return BehaviorTree.SUCCESS

    def move_to(self, radius = 0.5):
        distance = (self.tx - self.x)**2 + (self.ty - self.y)**2
        self.dir = math.atan2(self.ty - self.y, self.tx - self.x)
        if distance < (PIXEL_PER_METER * radius)**2:
            self.speed = 0
            return BehaviorTree.SUCCESS
        else:
            self.speed = RUN_SPEED_PPS
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        find_random_location_node = Leaf('Find Random Location', self.find_random_location)
        move_to_node = Leaf('Move To', self.move_to)
        wander_sequence = Sequence('Wander', find_random_location_node, move_to_node)
        self.bt = BehaviorTree(wander_sequence)

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def update(self):
        self.bt.run()
        self.calculate_current_position()

    def draw(self):
        tw, th = int(100*self.size), int(100*self.size)
        Zombie.font.draw(self.x - 30, self.y + 50, self.name, (255, 255, 0))

        if math.cos(self.dir) < 0:
            if self.speed == 0:
                Zombie.images['Idle'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
            else:
                Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
        else:
            if self.speed == 0:
                Zombie.images['Idle'][int(self.frame)].draw(self.x, self.y, 100, 100)
            else:
                Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y, 100, 100)

    def handle_event(self, event):
        pass

    def handle_collision(self, other, group):
        if group == 'boy:zombie':
            game_world.remove_object(self)
        pass