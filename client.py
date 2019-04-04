import socket
import sys
import errno


HEADER_LEN = 10
IP = "127.0.0.1"
PORT = 4269

username = input("Please Enter a Username: ")
uname = username
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((IP, PORT))
except:
    PORT += 1
    client_socket.connect((IP, PORT))
client_socket.setblocking(False)
username_encoded = username.encode("utf-8")
username_header = f"{len(username):<{HEADER_LEN}}".encode("utf-8")
client_socket.send(username_header + username_encoded)

while True:
    message = input(f"{username}> ").strip("\n")
    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message):<{HEADER_LEN}}".encode("utf-8")
        client_socket.send(message_header + message)
    try:
        while True:
            temp_header = client_socket.recv(HEADER_LEN)
            if not len(temp_header):
                print("Connection Terminated by the Server")
                sys.exit()
            temp_length = int(temp_header.decode("utf-8"))
            temp = client_socket.recv(temp_length).decode("utf-8")
            print(f"{temp}> {message}")
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Message Could not be Read", str(e))
            sys.exit()
        continue
    except Exception as e:
        print("Caught an Error!", str(e))
        sys.exit()
