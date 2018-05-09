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
    ''' Add reminder to reminder file. Gives line number. '''

    # Count number of lines in reminder file
    p = subprocess.Popen(['wc', '-l', filename], stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
        return int(result.strip().split()[0])
    
    print("[!] Len of reminders.txt: ", result)
    
    # Append reminder to file with number
    with open(filename, "a") as fp:
        fp.write( str(result+1) + ". " + reminder )
    
    print("[+] Wrote reminder to file.")

def main(argv=sys.argv[1:]):

    parser = argparse.ArgumentParser(description='Add,list, or remove reminders to reminders.txt file in home directory.')
    parser.add_argument('-a', metavar='add', help='add a reminder')
    parser.add_argument('-d', metavar='delete', help='delete a reminder from the list')
    parser.add_argument('-l', action='store_true', help='list contents of reminders file')
    
    args = parser.parse_args()
    
    # Check if log file exists and get filename if so
    filename = check_reminders_file()

    # List reminders if no arguments are provided or if -l option given
    if len(argv) == 0 or args.l:
        # Output reminder file
        with open(filename, "r") as fp:
            lines = fp.readlines()
        print("[+] Reminders:")
        for line in lines:
            print(line)
        sys.exit(0)

    # If only one argument given, its a reminder to add
    elif len(argv) == 1:
        reminder = argv[0]
        print("[+] Adding reminder '{}' to {}".format(reminder, filename))
        sys.exit(0)
    
    else:
        if args.a:
            reminder = args.a
        elif args.d:
            pass

if __name__ == '__main__':
    main()


