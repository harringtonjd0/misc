#!/bin/bash

#################################################################################
# Automate Nmap scanning.  Given an IP, do a quick scan of most common ports    #
# If results are found, start a new scan to get more in depth information       #
# on found ports.                                                               #
#                                                                               #
# After more detailed scan, optionally run scan on all ports and do other stuff #
#################################################################################

# ANSI sequences for colored output
BLUE="\033[1;34m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
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

# Check if file exists
if [[ -f "quick_nmap" ]]; then
	printf "${YELLOW}[-] Found file \"quick_nmap\", skipping initial scan.${NC}\n"
else
	# Run initial nmap scan
	printf "${BLUE}[+] Running initial nmap scan:\n\n - $init_scan\n\n${NC}"
	eval $init_scan
fi

# Make sure host is up
up=$(grep "host down\|Host seems down" quick_nmap)
if [[ ! -z "$up" ]]; then
	printf "${RED}[!] Host is down, quitting.${NC}\n"
	exit 1
fi

# Get ports from quick scan
ports=$(grep open quick_nmap | cut -d/ -f1 | tr "\n" ",")
ports=${ports%?} # remove last comma from array
detailed_scan="nmap -v -Pn -A $1 -p${ports} -oN nmapped"

# Check if detailed scan file exists
if [[ -f "nmapped" ]]; then
	printf "${YELLOW}[-] Found file \"nmapped\", skipping detailed scan.${NC}\n"
else
	# Run detailed scan on found ports
	printf "\n${BLUE}[+] Running detailed scan:\n\n - $detailed_scan\n\n${NC}"
	eval $detailed_scan
fi

if [[ -f "full_nmap" ]]; then
	printf "${YELLOW}[-] Found file \"nmapped\", skipping full port scan.${NC}\n"
else
	# Ask if full scan is desired and run if yes
	while true; do
		printf "${BLUE}[+] Run full scan? ($full_scan) [y/n]${NC} "
		read full_opt
	    case $full_opt in
		[Yy]* ) printf "${BLUE}[+] Running full scan.\n\n - $full_scan\n\n${NC}" \
			&& eval $full_scan && break;;
		[Nn]* ) break;;
		* ) echo "Please answer yes or no.";;
	    esac
	done
fi

# Web scan function
function web_scan()
{
	gobust_cmd="gobuster -u $1 -w /usr/share/wordlists/dirb/common.txt -o gobuster_out"
	nikto_cmd="nikto -h $1  2>&1 1 > nikto_out &"
	printf "\n${BLUE}[+] Web server is up, running web scans:\n\n"
	printf " - $gobust_cmd\n"
	printf " - $nikto_cmd${NC}\n\n"
	printf "${BLUE}[+] Running nikto in background [PID "
	eval $nikto_cmd
	printf "$!]\n[+] Running gobuster now.${NC}\n\n"
	eval $gobust_cmd
	
}

# SMB scan function
function smb_scan()
{
	nmap_smb="nmap -p 139,445 --script=smb* $1 2>&1 1 > nmap_smb_out &"
	enum4linux_cmd="enum4linux -a $1 | tee enum4linux_out"
	printf "\n${BLUE}[+] SMB detected. Running Nmap SMB scans and Enum4linux:\n\n"
	printf " - $enum4linux_cmd\n"
	printf " - $nmap_smb$\n\n"
	printf "[+] Running Nmap SMB scripts in background [PID "
	eval $nmap_smb
	printf "$!]\n[+] Running Enum4linux now.${NC}\n"
	eval $enum4linux_cmd
}

# Run specific scans
web=$(grep '80/tcp\|443/tcp' quick_nmap)
smb=$(grep '139/tcp\|445/tcp' quick_nmap)
if [[ ! -z $web ]]; then
	web_scan $1
fi
if [[ ! -z $smb ]]; then
	smb_scan $1
fi	

printf "${BLUE}[+] Exiting.${NC}\n"
exit 0


