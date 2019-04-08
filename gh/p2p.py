import socket
from threading import Thread
import time
from datetime import datetime


def timestamp():
    now = datetime.now()
    return "[" + str(now.date()) + " " + str(now.time())[:8] + "]"

class Server(Thread):
    def __init__(self):
        Thread.__init__(self)




