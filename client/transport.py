class ClientInput:
    def __init__(self, character_input):
        self.dx = character_input.movement.x
        self.dy = character_input.movement.y
        self.shooting = character_input.shooting
        self.lookx = character_input.look_direction.x
        self.looky = character_input.look_direction.y


class ClientInitializer:
    def __init__(self):
        self.asd = 4


class GameInfo:
    def __init__(self, json):
        self.player_index = json["player_index"]
        self.width = json["width"]
        self.height = json["height"]


class PlayerState:
    def __init__(self, json, own_index):
        self.player_index = json["player_index"]
        self.kills = json["kills"]
        self.dead = json["dead"]

        self.x = json["x"]
        self.y = json["y"]
        self.rotation = json["rotation"]

        self.own = self.player_index == own_index


class BulletState:
    def __init__(self, json):
        self.x = json["x"]
        self.y = json["y"]
        self.rotation = json["rotation"]
        

class GameState:
    def __init__(self, json, own_index):
        self.winner = json["winner"]

        self.players = []
        for p in json["players"]:
            self.players.append(PlayerState(p, own_index))
        self.bullets = []
        for p in json["bullets"]:
            self.bullets.append(BulletState(p))


class ServerState:
    def __init__(self, ip):
        self.ip = ip

        self.own_index = None
        self.game_info = None

    def initialize(self, initializer):
        self.own_index = initializer.player_index


class TransportHandler:
    def __init__(self, socket):
        self.socket = socket
        self.server = None
        self.game_state = None

    def connect(self, server_ip):
        self.server = ServerState(server_ip)
        self._send(ClientInitializer())

    def get_game_info(self):
        self._receive_initialize()

        return self.server.game_info

    def get_game_state(self):
        self._receive_game_state()

        return self.game_state

    def send_input(self, inputs):
        client_input = ClientInput(inputs)
        self._send(client_input)

    def _send(self, message):
        self.socket.add_to_queue(message, self.server.ip)

    def _receive_initialize(self):
        messages = self._receive()
        
        for message in messages:
            if message.get("player_index") != None:
                self.server.game_info = GameInfo(message)
                self._receive_game_state(messages)
                break

    def _receive_game_state(self, messages = None):
        if messages == None: messages = self._receive()

        for message in messages:
            if message.get("player_index") == None:
                self.game_state = GameState(message, self.server.game_info.player_index)

    def _receive(self):
        message_infos = self.socket.read_from_queue()

        valid_messages = []

        for message, ip in message_infos:
            if ip == self.server.ip: valid_messages.append(message)
        
        return valid_messages