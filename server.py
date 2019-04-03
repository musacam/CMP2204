import socket
import select
import datetime


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
CLIENT_DICT = dict()

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
    read_sockets, _, exception_sockets = select.select(SOCKET_LIST, [], SOCKET_LIST)
    for socket in read_sockets:
        if socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = receive(client_socket)
            if not user:
                continue
            SOCKET_LIST.append(client_socket)
            CLIENT_DICT[client_socket] = user
            print(f"""{user["data"].decode()} Connected from {client_address[0]}:{client_address[1]}""")
        else:
            message = receive(socket)
            if not message:
                print(f"""Connection Closed From {CLIENT_DICT[socket]["data"].decode()}""")
                SOCKET_LIST.remove(socket)
                del CLIENT_DICT[socket]
                continue
            user = CLIENT_DICT[socket]
            print(f"""Received From {user["data"].decode()}> {message["data"].decode()} at {datetime.datetime.now()}""")

            for client_socket in CLIENT_DICT:
                if client_socket != socket:
                    client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])

    for socket in exception_sockets:
        SOCKET_LIST.remove(socket)
        del CLIENT_DICT[socket]

