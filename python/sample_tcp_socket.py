#!/usr/bin/python
# Taken from Black Hat Python

import socket
import threading


# Simple TCP Client for socket proof of concept
target_host = 'www.google.com'
target_port = 80

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host, target_port))

client.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

response = client.recv(4096)

print(response)

# Sample UDP client

target_host = "127.0.0.1"
target_port = 80

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto("AABBCC", (target_host, target_port))

data, addr = client.recvfrom(4096)

print(data)


# This is a standard multi_threaded TCP server
bind_ip = "0.0.0.0"
bind_port = 999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(5)

print("[*] Listening on %s:%d" % (bind_ip, bind_port))

def handle_client(client_socket):
    request = client_socket.recv(1024)

    print("[*] Received: %s" %(request))

    client_socket.send("ACK!")

    client_socket.close()

while True:
    client,addr = server.accept()

    print("[*] Accepted connection from: %s: %d" %(addr[0], addr[1]))

    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
