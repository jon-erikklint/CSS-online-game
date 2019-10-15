from transport import *

class ClientInput:
    def __init__(self, character_input, player_index):
        self.player_index = player_index

        self.dx = character_input.movement.x
        self.dy = character_input.movement.y
        self.shooting = character_input.shooting
        self.lookx = character_input.look_direction.x
        self.looky = character_input.look_direction.y


class GameInfo:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class PlayerState:
    def __init__(self, json):
        self.player_index = json["player_index"]
        self.kills = json["kills"]
        self.dead = json["dead"]

        self.x = json["x"]
        self.y = json["y"]
        self.rotation = json["rotation"]


class BulletState:
    def __init__(self, json):
        self.x = json["x"]
        self.y = json["y"]
        self.rotation = json["rotation"]
        

class GameState:
    def __init__(self, json):
        self.winner = json["winner"]

        self.players = []
        for p in json["players"]:
            self.players.append(PlayerState(p))
        self.bullets = []
        for p in json["bullets"]:
            self.bullets.append(BulletState(p))


def get_game_info():
    game_info = GameInfo(640, 640)
    return game_info


def send_inputs(inputs, player_id):
    client_input = ClientInput(inputs, player_id)
    send(client_input)

game_state = None

def read_game_state(own_index):
    global game_state
    values = receive(GameState)
    if len(values) > 0:
        game_state = values[0]
        for player in game_state.players:
            player.own = player.player_index == own_index
    return game_state