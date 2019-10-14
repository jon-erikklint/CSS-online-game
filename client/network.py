from input import CharacterInput

class ClientInput:
    def __init__(self, character_input, player_index):
        self.player_index = player_index
        self.character_input = character_input


class ClientInputs:
    def __init__(self, players):
        self.inputs = {}
        for player in players:
            self.inputs[player.player_index] = CharacterInput()

    def update(self, client_input):
        self.inputs[client_input.player_index] = client_input.character_input

client_inputs = None


def initialize_network_server(game):
    global client_inputs
    client_inputs = ClientInputs(game.players)


def send_inputs(inputs, player_id):
    client_input = ClientInput(inputs, player_id)
    client_inputs.update(client_input)


def read_inputs():
    return client_inputs.inputs

game_state = None

def send_game_state(game):
    global game_state
    game_state = game


def read_game_state():
    return game_state