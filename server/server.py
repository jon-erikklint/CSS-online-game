from model import Game, Player, new_game, update_world
from game_time import frame_time, set_frame
from network import *
from transport import network_update

width, height = 640, 640
game = new_game(3, width, height)

initialize_network_server(game)

last_frame = 0
frame_length = 10

while 1:
    network_update()

    set_frame()
    dt = frame_time() - last_frame
    if dt < frame_length: continue
    last_frame = frame_time()

    character_inputs = read_inputs()
    update_world(game, character_inputs)
    send_game_state(game)