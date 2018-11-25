#!/bin/bash

################################################################################
#  Automate Nmap scanning and run enumeration tools based on results.          #
#  Given an IP, do a quick scan of most common ports. If results are found,    #
#                                                                              #
#  After more detailed scan, optionally run full TCP and UDP scan.             #
#                                                                              #
#  Next, run web (gobuster, nikto) and/or SMB (enum4linux, nmap scripts) scans #
#  based on nmap results.                                                      #
#                                                                              #
#  Work in progress.                                                           #
################################################################################

# ANSI sequences for colored output
BLUE="\033[1;34m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
NC="\033[0m"

# Make sure IP is valid
function validate_ip()
{
	# Make sure its a valid IP.
	valid=$(echo "$1" | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b")
	if [[ -z "$valid" ]]; then
		printf "${RED}[!] Enter valid IP address.${NC}\n"
		exit 1
	else
		return 0
	fi
}

# Check args (IP and -y for full scan)  In future, take range or multiple IPs
run_full=0
target=0
if [ $# -gt 2 -o $# -lt 1 ]; then
	echo "Usage: $0 x.x.x.x [-y]"
	echo " -y : Run full Nmap scan without asking"
	exit 1
elif [ $# -eq 1 ]; then
	target=$1
else
	# 2 args given
	if [ "$1" = "-y" ]; then
		target=$2	
		run_full=1
		printf "${BLUE}[*] Received -y option, full scan will be run.${NC}\n"
	elif [ "$2" = "-y" ]; then
		target=$1
		run_full=1
		printf "${BLUE}[*] Received -y option, full scan will be run.${NC}\n"
	else
		run_full=0
		printf "${YELLOW}[-] Couldn't understand one of your arguments,
			continuing with scan.${NC}\n"
		if [ ! -z $(echo $1 | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b") ]; 
		then
			target=$1
		elif [ ! -z $(echo $2 | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b") ]; 
		then
			target=$2
		fi
	fi
fi

# Make sure ip is valid
validate_ip $target

# Scan commands to use
init_scan="nmap -v -T4 $target -oN quick_nmap"
detailed_scan="nmap -v -Pn -A $target -p${ports} -oN nmapped"
full_scan="nmap -v -Pn -sU -sS -p- $target -oN full_nmap"

# Check if file exists. If not, run initial scan.
if [[ -f "quick_nmap" ]]; then
	printf "${YELLOW}[-] Found file \"quick_nmap\", skipping initial scan.${NC}\n"
else
	# Run initial nmap scan
	printf "${BLUE}[+] Running initial nmap scan:\n\n * $init_scan\n\n${NC}"
	eval $init_scan
fi

# Make sure host is up, quit if not.
up=$(grep "host down\|Host seems down" quick_nmap)
if [[ ! -z "$up" ]]; then
	printf "${RED}[!] Host is down, quitting.${NC}\n"
	exit 1
fi

# Get ports from quick scan and put into detailed scan string
ports=$(grep open quick_nmap | cut -d/ -f1 | tr "\n" ",")
ports=${ports%?} # remove last comma from array
detailed_scan="nmap -v -Pn -A $target -p${ports} -oN nmapped"

# Check if detailed scan file exists. If not, run detailed scan.
if [[ -f "nmapped" ]]; then
	printf "${YELLOW}[-] Found file \"nmapped\", skipping detailed scan.${NC}\n"
else
	# Run detailed scan on found ports
	printf "\n${BLUE}[+] Running detailed scan:\n\n * $detailed_scan\n\n${NC}"
	eval $detailed_scan
fi

# Check if full scan file exists, ask to run scan if it doesn't.
if [[ -f "full_nmap" ]]; then
	printf "${YELLOW}[-] Found file \"full_nmap\", skipping full port scan.${NC}\n"
else
	# Ask if full scan is desired and run if yes
	if [ $run_full -eq 0 ]; then
		while true; do
			printf "${BLUE}[+] Run full scan? ($full_scan) [y/n]${NC} "
			read full_opt
		    case $full_opt in
			[Yy]* ) printf "${BLUE}[+] Running full scan.\n\n * $full_scan\n\n${NC}" \
				&& eval $full_scan && break;;
			[Nn]* ) break;;
			* ) echo "Please answer yes or no.";;
		    esac
		done
	else
		# -y option given
		printf "${BLUE}[+] Running full scan.\n\n * $full_scan\n\n${NC}"
		eval $full_scan
	fi

fi

# Web scan function
function web_scan()
{
	http=$(grep '80/tcp' quick_nmap)
	https=$(grep '443/tcp' quick_nmap)
	if [[ ! -z $http ]]; then
		gobust_cmd="gobuster -u $target -t 20 -o gobuster_out 
		-w /opt/SecLists/Discovery/Web-Content/raft-small-directories.txt"
		nikto_cmd="nikto -h $target  2>&1 1 > nikto_out &"
		printf "\n${BLUE}[+] Web server is up, running web scans:\n\n"
		printf " * $gobust_cmd\n"
		printf " * $nikto_cmd${NC}\n\n"
		printf "${BLUE}[+] Running nikto in background ${YELLOW}[PID "
		#eval $nikto_cmd
		printf "$!]\n${BLUE}[+] Running gobuster now.${NC}\n\n"
		#eval $gobust_cmd
	fi

	if [[ ! -z $https ]]; then
		gobust_cmd="gobuster -u $target:443 -t 20 -o gobuster443_out 
		-w /opt/SecLists/Discovery/Web-Content/raft-small-directories.txt"
		nikto_cmd="nikto -h $target:443  2>&1 1 > nikto443_out &"
		printf "\n${BLUE}[+] Web server is up, running web scans:\n\n"
		printf " * $gobust_cmd\n"
		printf " * $nikto_cmd${NC}\n\n"
		printf "${BLUE}[+] Running nikto in background ${YELLOW}[PID "
		eval $nikto_cmd
		printf "$!]\n${BLUE}[+] Running gobuster now.${NC}\n\n"
		eval $gobust_cmd
	fi
	
}

# SMB scan function
function smb_scan()
{
	enum4linux_cmd="enum4linux -a $target | tee enum4linux_out"
	nmap_scripts="smb-enum-shares,smb-ls,smb-enum-users,smb-mbenum"
	nmap_scripts="$nmap_scripts,smb-os-discovery,smb-security-mode,smb-vuln-cve2009-3103"
	nmap_scripts="$nmap_scripts,smb-vuln-ms06-025,smb-vuln-ms07-029,smb-vuln-ms08-067"
	nmap_scripts="$nmap_scripts,smb-vuln-ms10-054,smb-vuln-ms10-061"
	nmap_smb="nmap -p 139,445 --script=$nmap_scripts $target -oN nmap_smb_out"

	printf "\n${BLUE}[+] SMB detected."
	printf "\n${BLUE}[+] Running Enum4linux now:\n\n"
	printf " * $enum4linux_cmd${NC}\n"
	#eval $enum4linux_cmd
	printf "\n\n${BLUE}[+] Running Nmap SMB enumeration scripts now.\n\n"
	printf " * $nmap_smb$\n\n${NC}"
	eval $nmap_smb

}

# Run specific scans
web=$(grep '80/tcp\|443/tcp' quick_nmap)
smb=$(grep '139/tcp\|445/tcp' quick_nmap)
if [[ ! -z $web ]]; then
	web_scan $target
fi
if [[ ! -z $smb ]]; then
	smb_scan $target
fi	

printf "${BLUE}[+] Exiting.${NC}\n"
exit 0


