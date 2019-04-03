import socket
import select


HEADER_LEN = 10
IP = "127.0.0.1"
PORT = 4269

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

try:
    server_socket.bind((IP, PORT))
except:
    PORT += 1
    server_socket.bind((IP, PORT))
server_socket.listen()
print(f"Server Created on Port: {PORT}")

SOCKET_LIST = list(server_socket)
CLEINT_DICT = dict()

def receive(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LEN)
        if not len(message_header):
            return False
        message_len = int(message_header.decode().strip())
        return {"header": message_header, "data": client_socket.recv(message_len)}
    except:
        return False

while True:
    pass
