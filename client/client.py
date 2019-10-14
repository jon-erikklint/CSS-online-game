import pygame
from input import CharacterInput, init_input, read_input
from model import Game, Player, new_game, update_world
from output import init_output, update_screen
from game_time import frame_time, set_frame
from network import *

width, height = 640, 640

pygame.init()

game = new_game(3, width, height)
init_input(game)
init_output(width, height)

initialize_network_server(game)

player_id = next(player.player_index for player in game.players if player.own)

last_frame = 0
frame_length = 10

while 1:
    set_frame()
    dt = frame_time() - last_frame
    if dt < frame_length: continue
    last_frame = frame_time()

    character_input = read_input()

    send_inputs(character_input, player_id)
    character_inputs = read_inputs()

    update_world(game, character_inputs)

    send_game_state(game)
    game_state = read_game_state()

    update_screen(game_state)
