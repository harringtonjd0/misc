#!/bin/bash

# Set up Flask app in /opt

if [ ! -d "/opt/flask_app" ]
then
	mkdir "/opt/flask_app"
fi

cp -R * /opt/flask_app
echo "[+] Placed Flask app in /opt/flask_app"

