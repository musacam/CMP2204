import socket
import sys
import errno


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

username = input("Please Enter a Username: ")
uname = username.strip(" ").strip("\n")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((IP, PORT))
except:
    PORT += 1
    client_socket.connect((IP, PORT))
client_socket.setblocking(False)
username_encoded = username.encode()
username_header = f"{len(username_encoded):<{HEADER_LEN}}".encode()
client_socket.send(username_header + username_encoded)

while True:
    username = uname
    message = input(_YELLOW + f"{username}> " + RESET)
    # SENDING MESSAGE
    if message:
        message = message.encode()
        message_header = f"{len(message):<{HEADER_LEN}}".encode()
        client_socket.send(message_header + message)
    try:
        # RECEIVING MESSAGE
        while True:
            username_header = client_socket.recv(HEADER_LEN)
            if not len(username_header):
                print("Connection Terminated by the Server")
                sys.exit()
            username_length = int(username_header.decode().strip())
            username = client_socket.recv(username_length).decode()

            message_header = client_socket.recv(HEADER_LEN)
            message_length = int(message_header.decode().strip())
            message = client_socket.recv(message_length).decode()

            print("\033[1;96m" + f"\n{username}> " + "\033[0;0m" + f"{message}\n")
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Message Could not be Read", str(e))
            sys.exit()
        continue
    except Exception as e:
        print("Caught an Error!", str(e))
        sys.exit()
