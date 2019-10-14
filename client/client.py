import pygame, time
from input import CharacterInput, init_input, read_input
from model import Game, Player, new_game, update_world
from output import init_output, update_screen

width, height = 640, 640

pygame.init()

game = new_game(3, width, height)
init_input(game, game.players[0])
init_output(width, height)

last_frame = 0
frame_length = 10

while 1:
    ms = time.time() * 1000
    dt = ms - last_frame
    if dt < frame_length: continue
    last_frame = ms

    character_inputs = read_input()
    update_world(ms, game, character_inputs)
    update_screen(game)
