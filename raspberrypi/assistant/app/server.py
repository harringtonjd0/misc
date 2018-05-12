#!/usr/bin/env python3

""" Run local web app on Raspberry Pi. Used to manage reminder service and additional functions
    will be added later. Twilio is used to manage reminder service with SMS messages.

    Note: Run concurrently with 
        1.'ngrok http 1776'
            OR
        2.'autossh -R 80:localhost:1776 serveo.net' (after installing autossh)
    
    to expose local webserver to the Internet.  Note that in order for SMS interaction to work,
    Twilio must be given the webhook to forward messages to. After beginnging ngrok or serveo
    session, change messaging webhook URL in Twilio console. """

import os, sys
import subprocess
import datetime
from functools import wraps

try:
    from flask import Flask, render_template, request, Response
    from twilio.twiml.messaging_response import MessagingResponse
except ImportError as err:
    print("[!] Twilio and Flask are required: {}".format(err))
    sys.exit(1)

app = Flask(__name__)

def check_auth(username, password):
    """ Check if a username / password combo is valid """
    try:

        return username == os.environ['FLASK_USERNAME'] and password == os.environ['FLASK_PASS']
    except:
        print("[!] Couldn't find environment variables FLASK_USERNAME/FLASK_PASS")
        sys.exit(1)

def authenticate():
    """ Send a 401 response that enables basic auth """
    return Response(
            'Could not verify your access.\n'
            'Please supply valid credentials', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    """ Require authentication for function  """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def execute_reminder(cmd):
    """ Interact with reminders.py function to manage reminders"""
    try:
        cmd = cmd.split()

        # If adding, combine reminder into single list entry
        if len(cmd) > 2 and any(x == cmd[2] for x in {'-a', 'add', 'to'}):
            
            # make sure -a argument is given (not 'add' or 'to')
            cmd[2] = '-a'
            
            # Combine reminder string into one list element for subprocess.run
            cmd[3] = ' '.join([cmd[x] for x in range(3, len(cmd))])
            cmd = cmd[:4]
        
        # Execute command
        output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # If error, print stderr. Else use stdout
        if output.returncode != 0:
            output = output.stderr.decode()
        else:
            output = output.stdout.decode()
    except Exception as err:
        output = err
    return output

## Default web page 
@app.route('/')
@requires_auth
def index():
    """ Render index.html """
    
    # Get time for server
    now = datetime.datetime.now()
    time_str = now.strftime("%Y-%m-%d %H:%M")
    
    # Get reminder list and add to webpage
    try:
        output = subprocess.run(['python3', '/opt/assistant/app/reminders.py'], stdout=subprocess.PIPE).stdout.decode()
        reminders = output.split(':')[1]
        reminders = reminders.split('\n\n')
    
        # Remove item numbers
        reminders = [reminders[i].strip('\n')[2:] for i in range(len(reminders))]
        reminders = reminders[:-1]
    except:
        reminders = ['No reminders']
    
    
    # Collect data to pass to webpage
    templateData = {
            'time': time_str,
            'reminders' : reminders
            }
    
    # Render webpage
    return render_template('index.html', **templateData)

## SMS route
@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """ Respond to texts with a hello """
    
    # Pad message to make sure the message is on a new line
    message = ' --------  '

    # Get body of message
    body = request.values.get('Body', None)
    
    # If 'remindme', execute command
    if 'remindme' in body or 'Remindme' in body:
        
        if body[0] == 'r':
            body = body.replace('remindme', 'python3 /opt/assistant/app/reminders.py')
        elif body[0] == 'R':
            body = body.replace('Remindme', 'python3 /opt/assistant/app/reminders.py')
        else:
            message += "\n\nSorry, I couldn't understand your message."
        message += execute_reminder(body)
    
    # If greeting, reply with greeting
    elif any(x in body.lower() for x in {'hi', 'hello', 'hey'}):
        message += "Hello there!"

    else:
        message += "Sorry, I couldn't understand your message."
     
    resp = MessagingResponse()
    resp.message(message)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=1776)

