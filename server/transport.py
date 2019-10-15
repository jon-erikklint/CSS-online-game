import socket, json, select

OWN_IP = "127.0.0.1"
OWN_PORT = 5001

CLIENT_IP = "127.0.0.1"
CLIENT_PORT = 5002

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s2.bind((OWN_IP, OWN_PORT))
s2.setblocking(False)

inputs = [s2]
outputs = [s]

to_be_read = []
to_be_written = []


def network_update():
    readable, writeable, _ = select.select(inputs, outputs, [])
    for r in readable:
        data, recv = r.recvfrom(2048)
        to_be_read.append(data)
    for w in writeable:
        if len(to_be_written) > 0:
            w.sendto(to_be_written.pop(), (CLIENT_IP, CLIENT_PORT))


def send(message):
    coded_message = json.dumps(message.__dict__, default = lambda x: x.__dict__).encode()
    to_be_written.append(coded_message)


def receive(constructor):
    global to_be_read
    items = list(map(lambda x: constructor(json.loads(x)), to_be_read))
    to_be_read = []

    return items