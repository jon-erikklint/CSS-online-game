import pygame.math as gmath
from transport import *

class CharacterInput:
    def __init__(self, player_index):
        self.player_index = player_index
        self.look_direction = gmath.Vector2(0, 0)
        self.movement = gmath.Vector2(0, 0)
        self.shooting = False

    def __str__(self):
        return "Look at: {}, movement: {}, shooting: {}".format(self.look_direction, self.movement, self.shooting)


def create_character_input(json):
    cinput = CharacterInput(json["player_index"])
    cinput.look_direction = gmath.Vector2(json["lookx"], json["looky"])
    cinput.movement = gmath.Vector2(json["dx"], json["dy"])
    cinput.shooting = json["shooting"]

    return cinput


class PlayerState:
    def __init__(self, player):
        self.player_index = player.player_index
        self.dead = player.dead
        self.kills = player.kills

        self.x = player.location.x
        self.y = player.location.y
        self.rotation = player.rotation


class BulletState:
    def __init__(self, bullet):
        self.x = bullet.location.x
        self.y = bullet.location.y
        self.rotation = bullet.rotation
        

class GameState:
    def __init__(self, game):
        self.winner = game.winner.player_index if game.winner != None else None

        self.players = list(map(lambda p: PlayerState(p), game.players))
        self.bullets = list(map(lambda b: BulletState(b), game.bullets))


class ClientInputs:
    def __init__(self, players):
        self.inputs = {}
        for player in players:
            self.inputs[player.player_index] = CharacterInput(player.player_index)

    def update(self, client_input):
        self.inputs[client_input.player_index] = client_input


client_inputs = None


def initialize_network_server(game):
    global client_inputs
    client_inputs = ClientInputs(game.players)


def read_inputs():
    inputs = receive(create_character_input)
    for client_input in inputs:
        client_inputs.update(client_input)
    return client_inputs.inputs


def send_game_state(game):
    game_state = GameState(game)
    send(game_state)