import socket
import sys
import errno


HEADER_LEN = 10
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
    message = input(f"{username}> ")
    if message:
        message = message.encode()
        message_header = f"{len(message):<{HEADER_LEN}}".encode()
        client_socket.send(message_header + message)
    try:
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

            print(f"\n{username}> {message}\n")
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Message Could not be Read", str(e))
            sys.exit()
        continue
    except Exception as e:
        print("Caught an Error!", str(e))
        sys.exit()
