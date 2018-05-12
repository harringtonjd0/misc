#!/bin/bash

## Set up Flask app in /opt and create 'pi-webapp' alias

# Check if app directory exists. If so, empty it
if [ -d "/opt/assistant" ]; then
	rm -rf "/opt/assistant/"
fi

# Copy app contents into directory
mkdir /opt/assistant
cp -R * /opt/assistant

echo "[+] Placed Flask app in /opt/assistant"

# Check if pi-webapp link exists. If not, create it.
if [ ! -L "/usr/bin/assistant" ]; then
	ln -s /opt/assistant/app/assistant /usr/bin/assistant
fi

echo "[+] Use command 'assistant' to run server."

