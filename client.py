import socket
import sys
import errno

HEADER_LEN = 10
IP = "127.0.0.1"
PORT = 4269

username = input("Please Enter a Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((IP, PORT))
except:
    PORT += 1
    client_socket.connect((IP, PORT))
client_socket.setblocking(False)
username_encoded = username.encode("utf-8")
username_header = f"{len(username_encoded):<{HEADER_LEN}}".encode("utf-8")
client_socket.send(username_header + username_encoded)

while True:
    pass


