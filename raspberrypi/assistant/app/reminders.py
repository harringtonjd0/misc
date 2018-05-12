#!/usr/bin/env python3

## reminders.py -- Add or remove reminders in $HOME/reminders.txt

import argparse
import sys, os
import subprocess

def check_reminders_file():
    ''' Check if reminders.txt file exists in home directory. If empty, exit. '''
    
    homedir = os.environ['HOME']
    filename = homedir + "/reminders.txt"
    
    if not os.path.isfile(filename):
        print("[!] Could not find reminders file {}.".format(filename))
        sys.exit(1)
		 
    return filename

def add_reminder(reminder, filename):
    ''' Add reminder to reminder file. Gives line number. 
	If the file does not exist, create it. '''
	
    # Count number of lines in reminder file
    p = subprocess.Popen(['wc', '-l', filename], stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
    result, err = p.communicate()
    result = int(result.split()[0])
    if p.returncode != 0:
        raise IOError(err)
        return int(result.strip().split()[0])
    
    # Append reminder to file with number
    with open(filename, "a+") as fp:
        fp.write( str(result+1) + ". " + reminder + "\n")
    
    print("[+] Wrote reminder to file.")

def delete_reminder(number, filename):
	''' Delete reminder with number specified. '''
	
	# Read file and find entry with given number
	with open(filename, "r") as read_fp:
		lines = read_fp.readlines()
	
	# Remove entry from array
	number = int(number)
	del lines[number-1]
	
	# Replace number at beginning of each entry
	list_len = len(lines)
	for i in range(list_len):
		line_num = int(lines[i].split('.')[0])
		if ( line_num != i + 1):
			lines[i] = lines[i].replace(str(line_num), str(i+1))
			
	# Write lines to file
	with open(filename, "w") as write_fp:
		for line in lines:
			write_fp.write(line)

	print("[+] Removed entry.")

def main(argv=sys.argv[1:]):

    parser = argparse.ArgumentParser(description='Add,list, or remove reminders to reminders.txt file in home directory.')
    parser.add_argument('-a', metavar='add', help='add a reminder')
    parser.add_argument('-d', metavar='delete', help='delete a reminder from the list')
    parser.add_argument('-l', action='store_true', help='list contents of reminders file')
    parser.add_argument('--clear', action='store_true', help='clear all reminders in file')

    args = parser.parse_args()
    
    # Check if log file exists and get filename if so
    filename = check_reminders_file()

    # If --clear is given, empty reminder file
    if args.clear:
        # Delete and recreate file. Faster than opening and deleting text
        open(filename, "w").close()
        print("[+] Cleared reminders.")
        sys.exit(0)
	
    # List reminders if no arguments are provided or if -l option given
    if len(argv) == 0 or args.l:
        # Output reminder file
        with open(filename, "r") as fp:
            lines = fp.readlines()
        if len(lines) == 0:
            print("[+] No reminders")
            sys.exit(0)

        print("[+] Reminders:")
        for line in lines:
            print(line)
        sys.exit(0)

    if args.a:
        # Add reminder to file
        add_reminder(args.a, filename)

    elif args.d:
        # Remove reminder with given number
        delete_reminder(args.d, filename)

if __name__ == '__main__':
    main()


