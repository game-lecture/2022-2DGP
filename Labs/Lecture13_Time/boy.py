from pico2d import *
import game_world
from ball import Ball

#1 : 이벤트 정의
RD, LD, RU, LU, TIMER, SPACE = range(6)
event_name = ['RD', 'LD', 'RU', 'LU', 'TIMER', 'SPACE']

key_event_table = {
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU
}


#2 : 상태의 정의
class IDLE:
    @staticmethod
    def enter(self,event):
        print('ENTER IDLE')
        self.dir = 0
        self.timer = 1000

    @staticmethod
    def exit(self, event):
        print('EXIT IDLE')
        if event == SPACE:
            self.fire_ball()

    @staticmethod
    def do(self):
        self.frame = (self.frame + 1) % 8
        self.timer -= 1
        if self.timer == 0:
            self.add_event(TIMER)


    @staticmethod
    def draw(self):
        if self.face_dir == 1:
            self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)


class RUN:
    def enter(self, event):
        print('ENTER RUN')
        if event == RD:
            self.dir += 1
        elif event == LD:
            self.dir -= 1
        elif event == RU:
            self.dir -= 1
        elif event == LU:
            self.dir += 1

    def exit(self, event):
        print('EXIT RUN')
        self.face_dir = self.dir
        if event == SPACE:
            self.fire_ball()

    def do(self):
        self.frame = (self.frame + 1) % 8
        self.x += self.dir
        self.x = clamp(0, self.x, 1600)

    def draw(self):
        if self.dir == -1:
            self.image.clip_draw(self.frame*100, 0, 100, 100, self.x, self.y)
        elif self.dir == 1:
            self.image.clip_draw(self.frame*100, 100, 100, 100, self.x, self.y)


class SLEEP:

    def enter(self, event):
        print('ENTER SLEEP')
        self.frame = 0

    def exit(self, event):
        pass

    def do(self):
        self.frame = (self.frame + 1) % 8

    def draw(self):
        if self.face_dir == -1:
            self.image.clip_composite_draw(self.frame * 100, 200, 100, 100,
                                          -3.141592 / 2, '', self.x + 25, self.y - 25, 100, 100)
        else:
            self.image.clip_composite_draw(self.frame * 100, 300, 100, 100,
                                          3.141592 / 2, '', self.x - 25, self.y - 25, 100, 100)


#3. 상태 변환 구현

next_state = {
    IDLE:  {RU: RUN,  LU: RUN,  RD: RUN,  LD: RUN, TIMER: SLEEP, SPACE: IDLE},
    RUN:   {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE, SPACE: RUN},
    SLEEP: {RU: RUN, LU: RUN, RD: RUN, LD: RUN, SPACE: IDLE}
}




class Boy:

    def __init__(self):
        self.x, self.y = 100, 70
        self.frame = 0
        self.dir, self.face_dir = 0, 1
        self.image = load_image('animation_sheet.png')

        self.timer = 100

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)

    def update(self):
        self.cur_state.do(self)

        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                self.cur_state = next_state[self.cur_state][event]
            except KeyError:
                print(f'ERROR: State {self.cur_state.__name__}    Event {event_name[event]}')
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def fire_ball(self):
        print('FIRE BALL')
        ball = Ball(self.x, self.y, self.face_dir*2)
        game_world.add_object(ball, 1)
