from model import Game, Player, update_world
from game_time import frame_time, set_frame
from network import Socket
from transport import TransportHandler

width, height = 640, 640

game = Game(width, height)
socket = Socket("0.0.0.0", 5001, 5002)
transport_handler = TransportHandler(game, socket)

last_frame = 0
frame_length = 10

while 1:
    socket.update()

    set_frame()
    dt = frame_time() - last_frame
    if dt < frame_length: continue
    last_frame = frame_time()

    character_inputs = transport_handler.get_inputs()
    update_world(game, character_inputs)
    transport_handler.send_state()