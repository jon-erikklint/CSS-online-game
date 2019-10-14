import pygame, sys
import pygame.math as gmath

class CharacterInput:
    def __init__(self):
        self.look_direction = gmath.Vector2(0, 0)
        self.movement = gmath.Vector2(0, 0)
        self.shooting = False

    def __str__(self):
        return "Look at: {}, movement: {}, shooting: {}".format(self.look_direction, self.movement, self.shooting)

player_input = None

def init_input(game):
    global player_input

    for player in game.players:
        if player.own:
            player_input = CharacterInput()


def update_look_at(character_input, event):
    character_input.look_direction = gmath.Vector2(event.pos)


def update_shooting(character_input, event):
    if event.button != 1: return
    character_input.shooting = event.type == pygame.MOUSEBUTTONDOWN


def update_movement(character_input, event):
    directions = {
        119: gmath.Vector2(0,-1),
        115: gmath.Vector2(0,1),
        100: gmath.Vector2(1,0),
        97: gmath.Vector2(-1,0)
    }

    direction = directions.get(event.key)

    if direction == None: return
    
    direction *= 1 if event.type == pygame.KEYDOWN else -1

    character_input.movement += direction


def read_input():
    character_input = player_input
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEMOTION: update_look_at(character_input, event)
        elif event.type == pygame.MOUSEBUTTONDOWN: update_shooting(character_input, event)
        elif event.type == pygame.MOUSEBUTTONUP: update_shooting(character_input, event)
        elif event.type == pygame.KEYDOWN: update_movement(character_input, event)
        elif event.type == pygame.KEYUP: update_movement(character_input, event)

    return player_input