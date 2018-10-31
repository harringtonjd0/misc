#!/bin/bash

## Set up dynamic SSH tunnel to VPS, configure Firefox to use tunnel to proxy
## traffic, and open new window

## Requires VPS environment variable 

# ANSI sequences for colored output
BLUE="\033[1;34m"
RED="\033[1;31m"
NC="\033[0m"

# Port to set up dynamic tunnel
port=1025

# Firefox profile preferences file
prefs_js="$HOME/.mozilla/firefox/*.default/prefs.js"


# Check if preferences file exists. Probably not the best way to do this, but necessary
# because of randomized directory name. Assumes only one default directory

check_prefs_exists()
{
	for file in $prefs_js; do
		if [ ! -f $file ]; then
			printf "${RED}[!] Couldn't find prefs.js file:  $prefs_js${NC}\n"
			return 1
		fi
	done
	return 0
}


# Check if Firefox is configured to use tunnel. If not, add settings to do so.

configure_prefs()
{
	configured=$(grep "proxy.http" $prefs_js)
	if [[ ! $configured ]]; then
		printf "${BLUE}[+] Modifying Firefox proxy settings...${NC}\n"
		echo 'user.pref("network.proxy.http", "127.0.0.1");' >> $prefs_js
		echo 'user.pref("network.proxy.http_port", '"$port"');' >> $prefs_js
	fi
}


# Monitor process list and when Firefox stops (window is closed), clean up configuration
# and kill SSH tunnel
#
# $1 : PID of SSH Dynamic tunnel

monitor_firefox() 
{
	while true; do
		sleep 0.5
		active=$(ps -elf | grep $firefox_pid)
		if [[ ! $active ]]; then
			cleanup() $1
			return 0
		fi
	done 
}

# Cleanup function -- kill SSH tunnel and restore Firefox configuration
#
# $1 : PID of SSH Dynamic tunnel

cleanup() 
{
	sed -i '/network.proxy.http/d' $prefs_js
	kill $1
}

# Terminate function -- Ensure cleanup happens and exit. 
#
# $1 : PID of SSH Dynamic tunnel

terminate()
{
	while true; do
		config_uncleaned=$(grep "proxy.http" $prefs_js)
		ssh_alive=$(ps -elf | grep $1)
		if [ $config_uncleaned || $ssh_alive ]; then
			cleanup() $1
			sleep 0.2
		else
			break
		fi
	done
	
	printf "${BLUE}[+] Restored normal configuration and killed SSH tunnel to VPS.${NC}\n"
	exit 0
}

# Catch SIGINT, try to find PID of SSH tunnel to pass to terminate
catch_sigint()
{
	emergency_ssh_pid=$(ps -elf | grep "ssh -D $port" | awk '{ print $4 }')
	terminate() $emergency_ssh_pid
}


main()
{

	# Catch SIGINT and call terminate
	trap catch_sigint INT
	
	# Open SSH tunnel. Uses & instead of -f to catch PID 
	ssh -D $port -i $HOME/.ssh/vps.pem ubuntu@$VPS -N &
	ssh_pid=$(echo $!)
	sleep 0.3

	# Check if Firefox preferences file exists. If not, exit
	check_prefs_exists()
	if [ $? ]; then
		printf "${RED}[!] Couldn't find preferences file: $prefs_fs\n"	
		exit 1
	fi
	
	# Configure prefs.js to use proxy
	configure_prefs()	
	
	# Start Firefox with modified config and catch PID
	firefox https://ifconfig.co &
	firefox_pid=$(echo $!)

	# Monitor Firefox, cleanup when closed
	monitor_firefox() $ssh_pid

	# Normal termination - do final check and exit
	terminate() $ssh_pid
	
}

main
