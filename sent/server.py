import socket
import select
from datetime import datetime
import time
from threading import Thread


def timestamp():
    now = datetime.now()
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    hour = str(now.hour)
    minute = str(now.minute)
    second = str(now.second)
    return f"[{year:0>2}/{month:0>2}/{day:0>2}-{hour:0>2}:{minute:0>2}:{second:0>2}] "

"""----"""
RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
BLACK = "\033[30m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"
REVERSE = "\033[;7m"

_GREY = "\033[90m"
_RED = "\033[91m"
_GREEN = "\033[92m"
_YELLOW = "\033[93m"
_BLUE = "\033[94m"
_PINK = "\033[95m"
_CYAN = "\033[96m"
"""----"""

HEADER_LEN = 16
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

SOCKET_LIST = [server_socket]
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

a = 1

def online():
    global a
    while True:
        if int(time.time()) % 3 == 0:
            for socket in SOCKET_LIST:
                if socket != server_socket:
                    user = CLIENT_DICT[socket]
                    print(f"{user['data'].decode()} is Online + {a}")
                    a += 1
                    break

with open("message_log.txt", "a") as f:
    f.write(timestamp() + "Created Server\n")
    try:
        while True:
            read_sockets, _, exception_sockets = select.select(SOCKET_LIST, [], SOCKET_LIST)
            for socket in read_sockets:
                if socket == server_socket:
                    client_socket, client_address = server_socket.accept()
                    client_socket.setblocking(False)

                    user = receive(client_socket)
                    if not user:
                        continue
                    SOCKET_LIST.append(client_socket)
                    CLIENT_DICT[client_socket] = user
                    print(
                        f'{user["data"].decode()} Connected from ' + _PINK + f'{client_address[0]}:{client_address[1]}'
                        + RESET)
                    f.write(timestamp() +
                            f"{user['data'].decode()} Connected From {client_address[0]}:{client_address[1]}\n")
                else:
                    message = receive(socket)
                    if not message:
                        print(RED + f'Connection Closed From {CLIENT_DICT[socket]["data"].decode()}' + RESET)
                        f.write(timestamp() + f"{CLIENT_DICT[socket]['data'].decode()} Disconnected\n")
                        SOCKET_LIST.remove(socket)
                        del CLIENT_DICT[socket]
                        continue
                    user = CLIENT_DICT[socket]
                    print(f'Received From ' + GREEN + f'{user["data"].decode()}' +
                          CYAN + f' "{message["data"].decode()}"' + RESET + f' at {datetime.now()}')
                    f.write(timestamp() + f"{user['data'].decode()} : {message['data'].decode()}\n")

                    for client_socket in CLIENT_DICT:
                        if client_socket != socket:
                            client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])

            for socket in exception_sockets:
                SOCKET_LIST.remove(socket)
                del CLIENT_DICT[socket]

            # t = Thread(online())
            # t.start()


    finally:
        f.write(timestamp() + "Server Closed\n")
        f.write("-" * 75 + ' \n')
