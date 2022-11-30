import json


import random
import json
import pickle
import os

from pico2d import *
import game_framework
import game_world

import server

import play_state

from boy import Boy
from zombie import Zombie
from ground import Ground
from ball import Ball

menu = None

def enter():
    global menu
    menu = load_image('menu.png')
    hide_cursor()
    hide_lattice()

def exit():
    global menu
    del menu

def pause():
    pass

def resume():
    pass


def create_new_world():
    server.boy = Boy()
    game_world.add_object(server.boy, 1)
    game_world.add_collision_pairs(server.boy, None, 'boy:zombie')
    game_world.add_collision_pairs(server.boy, None, 'boy:ball')

    ground = Ground()
    game_world.add_object(ground, 0)

    balls = [Ball() for i in range(50)]
    game_world.add_objects(balls, 1)
    game_world.add_collision_pairs(None, balls, 'boy:ball')
    game_world.add_collision_pairs(None, balls, 'zombie:ball')


    # load json object data
    with open('zombie_data.json', 'r') as f:
        zombie_data_list = json.load(f)
        zombies = [Zombie(o['name'], o['x'], o['y'], o['size']) for o in zombie_data_list]
        game_world.add_objects(zombies, 1)
        game_world.add_collision_pairs(None, zombies, 'boy:zombie')
        game_world.add_collision_pairs(zombies, None, 'zombie:ball')





def load_saved_world():
    game_world.load()
    for o in game_world.all_objects():
        if isinstance(o, Boy):
            server.boy = o
            break
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_n:
            create_new_world()
            game_framework.change_state(play_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_l:
            load_saved_world()
            game_framework.change_state(play_state)

def update():
    pass

def draw():
    clear_canvas()
    menu.draw(get_canvas_width()//2, get_canvas_height()//2)
    update_canvas()






