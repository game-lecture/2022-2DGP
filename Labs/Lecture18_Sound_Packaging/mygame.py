import game_framework
import pico2d

import load_state

PIXEL_PER_METER = 100 / 3

pico2d.open_canvas(int(32 * PIXEL_PER_METER), int(24 * PIXEL_PER_METER))
game_framework.run(load_state)
pico2d.close_canvas()