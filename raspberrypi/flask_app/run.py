#!/usr/bin/env python3

import subprocess
import datetime

try:
    from flask import Flask, render_template, request, redirect
    from twilio.twiml.messaging_response import MessagingResponse
except ImportError as err:
    print("[!] Twilio and Flask are required: {}".format(err))
    sys.exit(1)

app = Flask(__name__)

def execute_reminder(cmd):
    try:
        cmd = cmd.split()

        # If -a, combine reminder into single list entry
        if len(cmd) > 1 and cmd[1] == '-a':
            cmd[2] = ''.join([cmd[x] for x in range(2, len(cmd))])
            cmd = cmd[:3]
        output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # If error, print stderr. Else use stdout
        if output.returncode != 0:
            output = output.stderr.decode()
        else:
            output = output.stdout.decode()
    except Exception as err:
        output = err
    return output

@app.route('/')
def index():
    ''' Render index.html '''
    
    # Get time for server
    now = datetime.datetime.now()
    time_str = now.strftime("%Y-%m-%d %H:%M")
    
    # Get reminder list and add to webpage
    try:
        output = subprocess.run(['/opt/reminders/reminders.py'], stdout=subprocess.PIPE).stdout.decode()
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

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    ''' Respond to texts with a hello '''
    
    # Pad message to make sure the message is on a new line
    message = ' --------  '

    # Get body of message
    body = request.values.get('Body', None)
    
    # If 'remindme', execute command
    if 'remindme' in body or 'Remindme' in body:
        
        if body[0] == 'r':
            abody = body.replace('remindme', '/opt/reminders/reminders.py')
        elif body[0] == 'R':
            abody = body.replace('Remindme', '/opt/reminders/reminders.py')
        else:
            message += "\n\nSorry, I couldn't understand your message."
        message += execute_reminder(abody)
    
    # If greeting, reply with greeting
    elif any(x in body.lower() for x in {'hi', 'hello', 'hey'}):
        message += "Hello there!"

    else:
        message += "Sorry, I couldn't understand your message."
     
    resp = MessagingResponse()
    resp.message(message)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

