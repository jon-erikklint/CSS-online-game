import pygame, sys
from input import CharacterInput, init_input, read_input, local_input
from output import init_output, update_screen
from game_time import frame_time, set_frame
from network import Socket
from transport import TransportHandler

if len(sys.argv) < 2:
    raise Exception("Give server ip")
server_ip = sys.argv[1]

pygame.init()
socket = Socket("127.0.0.1", 5002, 5001)
transport = TransportHandler(socket)

set_frame()
transport.connect(server_ip, frame_time())

while 1:
    socket.update()

    set_frame()

    game_info = transport.get_game_info(frame_time())
    if game_info != None: break
    local_input()

init_input()
init_output(game_info.width, game_info.height)

last_frame = 0
frame_length = 10

while 1:
    socket.update()

    set_frame()
    dt = frame_time() - last_frame
    if dt < frame_length: continue
    last_frame = frame_time()

    character_input = read_input()
    transport.send_input(character_input)

    game_state = transport.get_game_state()
    update_screen(game_info, game_state)
