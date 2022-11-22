import random
import json
import os

from pico2d import *
import game_framework
import game_world

import server

from boy import Boy
from ground import Ground
from ball import Ball
from zombie import Zombie
from ball import Ball

name = "DrillState"



def collide(a, b):
    # fill here
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def enter():

    ground = Ground()
    game_world.add_object(ground, 0)

    ball_list = [Ball() for i in range(30)]
    game_world.add_objects(ball_list, 1)

    zombie_list = [Zombie()]
    game_world.add_objects(zombie_list, 1)

    server.boy = Boy()
    game_world.add_object(server.boy, 1)

    game_world.add_collision_pairs(zombie_list, ball_list, 'zombie:ball')
    game_world.add_collision_pairs(server.boy, zombie_list, 'boy:zombie')
    game_world.add_collision_pairs(server.boy, ball_list, 'boy:ball')






def exit():
    game_world.clear()

def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            server.boy.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()

    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            print('COLLISION ', group)
            a.handle_collision(b, group)
            b.handle_collision(a, group)

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()






