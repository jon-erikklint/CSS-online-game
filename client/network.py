import socket, json, select

class Socket:
    def __init__(self, own_ip, own_port, client_port):
        self.OWN_IP = own_ip
        self.OWN_PORT = own_port

        self.CLIENT_PORT = client_port

        self.output_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.input_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.input_socket.bind((self.OWN_IP, self.OWN_PORT))
        self.input_socket.setblocking(False)

        self.inputs = [self.input_socket]
        self.outputs = [self.output_socket]

        self.input_message_queue = []
        self.output_message_queue = []

    def update(self):
        readable, writeable, _ = select.select(self.inputs, self.outputs, [])
        for r in readable: self._read(r)
        for w in writeable: self._write(w)

    def _read(self, r):
        raw_data, recv = r.recvfrom(2048)

        data = json.loads(raw_data)
        ip = recv[0]

        self.input_message_queue.append((data, ip))

    def _write(self, w):
        if len(self.output_message_queue) == 0: return

        message, ip = self.output_message_queue.pop(0)

        w.sendto(message, (ip, self.CLIENT_PORT))

    def read_from_queue(self):
        messages = self.input_message_queue
        self.input_message_queue = []

        return messages

    def add_to_queue(self, message, ip):
        message = json.dumps(message.__dict__, default = lambda x: x.__dict__).encode()

        self.output_message_queue.append((message, ip))
    