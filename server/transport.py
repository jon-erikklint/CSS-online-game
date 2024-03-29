import json, select
import pygame.math as gmath
from network import Socket
from game_time import frame_time

class CharacterInput:
    def __init__(self, player_index):
        self.player_index = player_index
        self.look_direction = gmath.Vector2(0, 0)
        self.movement = gmath.Vector2(0, 0)
        self.shooting = False

    def __str__(self):
        return "Look at: {}, movement: {}, shooting: {}".format(self.look_direction, self.movement, self.shooting)


def create_character_input(json, index):
    cinput = CharacterInput(index)
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


class Receiver:
    def __init__(self, ip, player_index, time):
        self.ip = ip
        self.player_index = player_index

        self.current_package_number = -1
        self.last_message = time
        self.current_input = CharacterInput(player_index)


class PlayerInitializer:
    def __init__(self, player_index, width, height):
        self.player_index = player_index
        self.width = width
        self.height = height


class Package:
    def __init__(self, package_number, content):
        self.package_number = package_number
        self.content = content


disconnect_time = 10000


class TransportHandler:
    def __init__(self, game, socket):
        self.socket = socket
        self.game = game
        self.package_number = 0 # no need for lapping as with 100 frames per second the package numbers will run out in 250 days assuming int

        self.clients = []
        self.clients_by_ip = {}
        self.clients_by_id = {}

    def get_inputs(self):
        self._receive()
        self._check_for_dead_connections()

        inputs = {}
        for client in self.clients:
            inputs[client.player_index] = client.current_input

        return inputs

    def _check_for_dead_connections(self):
        to_remove = []
        for client in self.clients:
            passed_time = frame_time() - client.last_message
            if passed_time > disconnect_time: to_remove.append(client)

        for client in to_remove:
            self.clients.remove(client)
            del self.clients_by_id[client.player_index]
            del self.clients_by_ip[client.ip]

            self.game.remove_player(client.player_index)


    def send_state(self):
        game_state = GameState(self.game)
        package = self._get_package(game_state)
        self._broadcast(package)

    def _get_package(self, data):
        number = self.package_number
        self.package_number += 1
        package = Package(number, data)

        return package  

    def _send(self, ip, message):
        self.socket.add_to_queue(message, ip)

    def _broadcast(self, message):
        for client in self.clients:
            self._send(client.ip, message) # double the trouble
            self._send(client.ip, message)

    def _receive(self):
        message_infos = self.socket.read_from_queue()

        for message, ip in message_infos:
            client = self.clients_by_ip.get(ip)
            if client == None:
                self._create_receiver(ip)
            else:
                if message.get("asd") != None: 
                    self._send_initialization(client)
                else:
                    self._save_input(client, message)

    def _create_receiver(self, ip):
        index = self.game.add_new_player()
        receiver = Receiver(ip, index, frame_time())

        self.clients.append(receiver)
        self.clients_by_id[index] = receiver
        self.clients_by_ip[ip] = receiver

        self._send_initialization(receiver)

    def _send_initialization(self, client):
        self._send(client.ip, PlayerInitializer(client.player_index, self.game.width, self.game.height))

    def _save_input(self, client, message):
        index = client.player_index
        package_number = message.get("package_number")

        if client.current_package_number < package_number:
            client.current_input = create_character_input(message.get("content"), index)
            client.package_number = package_number
            client.last_message = frame_time()