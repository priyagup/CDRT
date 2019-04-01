import socket, json
import time, sys
import random

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = sys.argv[1]
port = int(sys.argv[2])
s.connect((host, port))

print("Client1")

s.close()