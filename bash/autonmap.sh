#!/bin/bash

#################################################################################
## Automate Nmap scanning.  Given an IP, do a quick scan of most common ports  ##
## If results are found, start a new scan to get more in depth information     ##
## on found ports.                                                             ##
##                                                                             ##
## After more detailed scan, optionally run scan on all ports                  ##
#################################################################################

# ANSI sequences for colored output
BLUE="\033[1;34m"
RED="\033[1;31m"
NC="\033[0m"


# Make sure IP arg is given.  In future, take range or multiple IPs
if [ $# -ne 1 ]; then
	echo "Usage: $0 x.x.x.x"
	exit 1
fi

# Make sure its a valid IP.
valid=$(echo "$1" | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}')
if [[ -z "$valid" ]]; then
	printf "${RED}[!] Enter valid IP address.${NC}\n"
	exit 1
fi

# Scan commands to use
init_scan="nmap -v -T4 $1 -oN quick_nmap"
detailed_scan="nmap -v -Pn -A $1 -p${ports} -oN nmapped"
full_scan="nmap -v -Pn -p- $1 -oN full_nmap"

# Run initial nmap scan
printf "${BLUE}[+] Running initial nmap scan:\n\n$init_scan\n\n${NC}"
eval $init_scan

# Make sure host is up
up=$(grep "Host seems down" quick_nmap)
if [[ ! -z "$up" ]]; then
	printf "${RED}[!] Host is down, quitting.${NC}\n"
	exit 1
fi

# Get ports from quick scan
ports=$(grep open quick_nmap | cut -d/ -f1 | tr "\n" ",")
ports=${ports%?} # remove last comma from array
detailed_scan="nmap -v -Pn -A $1 -p${ports} -oN nmapped"

# Run detailed scan on found ports
printf "\n${BLUE}[+] Running detailed scan:\n\n$detailed_scan\n\n${NC}"
eval $detailed_scan

# Ask if full scan is desired
while true; do
	printf "${BLUE}[+] Run full scan? ($full_scan) [y/n]${NC} "
	read full_opt
    case $full_opt in
        [Yy]* ) printf "${BLUE}[+] Running full scan.\n\n$full_scan\n\n${NC}" \
		&& eval $full_scan;;
        [Nn]* ) printf "${BLUE}[+] Exiting.${NC}\n" && exit 0;;
        * ) echo "Please answer yes or no.";;
    esac
done
