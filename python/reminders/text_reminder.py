#!/usr/bin/env python3

''' Reads from and writes to a list of reminders and periodically texts reminders to cell '''


try:
	from twilio.rest import Client
except ImportError:
	print("[!] Twilio is required. Install with 'pip3 install twilio'.")
	sys.exit(1)	

import os, sys

# Twilio authentication credentials stored in environment variables
sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_num = str(os.environ['TWILIO_NUMBER'])
cell_num = str(os.environ['CELL_NUMBER'])


# Connect to Twilio
client = Client(sid, auth_token)

# Send test text
message = client.messages.create(body="testing 123", from_ = twilio_num, to = cell_num)
print(message.sid)


