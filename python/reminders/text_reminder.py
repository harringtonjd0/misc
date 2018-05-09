#!/usr/bin/env python3

''' Reads from and writes to a list of reminders and periodically texts reminders to cell '''

import sys, os
from time import strftime
from datetime import datetime

try:
	from twilio.rest import Client
except ImportError:
	print("[!] Twilio is required. Install with 'pip3 install twilio'.")
	sys.exit(1)	

## Check reminders list in home directory
home_dir = os.environ['HOME'] + "/"
reminders_file = home_dir + "reminders.txt"

# Check if reminders file ($HOME/reminders.txt) exists
if not os.path.isfile(reminders_file):
    print("[!] Could not locate reminders file: {}.".format(reminders_file))
    sys.exit(1)

# Read from reminders file. All reminders will be sent via SMS. 
with open(reminders_file, "r") as fp:
    lines = fp.readlines()
if len(lines) == 0:
    print("[+] No reminders.")
    sys.exit(0)

# Format message to send
now = datetime.now()
date_string = now.strftime("%A (%b %d %Y)")

message = ["\r\nReminders for {}:\r\n".format(date_string)]
append = message.append
for item in lines:
    append(item)
message = ''.join(message)

# Get Twilio authentication credentials stored in environment variables
sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_num = os.environ['TWILIO_NUMBER']
cell_num = os.environ['CELL_NUMBER']


# Connect to Twilio
client = Client(sid, auth_token)


# Send test text
text = client.messages.create(body=message, from_ = twilio_num, to = cell_num)
print("[+] Sent SMS reminder with SID ",text.sid)


