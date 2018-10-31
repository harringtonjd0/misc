#!/bin/bash

## Zip up specified directories into encrypted archive then copy to VPS for backup storage
## Requires VPS IP to be stored in VPS env variable

# ANSI sequences for colored output
BLUE="\033[1;34m"
NC="\033[0m"

# Directories to recursively zip
dirs=(/home /opt)

# Create encrypted archive. Zip twice with different passwords for no reason whatsoever
zip -r --encrypt /var/backups/bkp "${dirs[@]}" 
zip --encrypt /var/backups/backup /var/backups/bkp.zip

# Rename with current date
timestamp=$(date "+%Y%m%d-%H:%M:%S")
mv /var/backups/backup.zip /var/backups/backup_$timestamp.bak

# Copy to VPS
scp -i ~/.ssh/vps.pem /var/backups/backup.bak ubuntu@$VPS:/var/backups/laptop_$timestamp.bak 

printf "${BLUE}[+] Archived following directories to VPS @ $VPS:${NC}\n"
for dir in "${dirs[@]}"; do
	printf "\t${BLUE}$dir${NC}\n"
done
printf "${BLUE}[+] Filename: laptop_$timestamp.bak${NC}\n"

