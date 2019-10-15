import pygame
from input import CharacterInput, init_input, read_input
from output import init_output, update_screen
from game_time import frame_time, set_frame
from network import *
from transport import network_update

pygame.init()

game_info = get_game_info()
init_input()
init_output(game_info.width, game_info.height)

player_id = 0

last_frame = 0
frame_length = 10

while 1:
    network_update()

    set_frame()
    dt = frame_time() - last_frame
    if dt < frame_length: continue
    last_frame = frame_time()

    character_input = read_input()

    send_inputs(character_input, player_id)
    game_state = read_game_state(player_id)
    update_screen(game_info, game_state)
