#!/usr/bin/env python3

import os, sys
import argparse
import random
import webbrowser

def read_from_list(filename):
    
    """ Read URLs into dict from reading list file """
    reading_list = []
    with open(filename, 'r') as fp:
        reading_list = fp.readlines()
        reading_list = [s.strip('\n') for s in reading_list]
        
    # Parse lines to convert list to dict
    list_dict = dict(entry.split(';;;') for entry in reading_list)

    return list_dict

def main(argv):
    
    """ Maintains a list of articles or websites to read/browse through
    and opens a browser window to a chosen or random selection """
    
    # Check for WEB_READING_LIST environment variable
    # This allows the user to easily define their own filepath, one and done
    try:
        reading_list_file = os.environ['WEB_READING_LIST']
    except KeyError:
        sys.stderr.write('[!] This script uses an environment variable called '
                '\'WEB_READING_LIST\' to find the file containing URL entries.'
                '\n[!] Please define this variable with the desired file path.\n')
        sys.exit(1)

    ## Take command line arguments from user
    
    # Add command line arguments and options
    parser = argparse.ArgumentParser(description="Open an interesting website or article in a web browser.")
    parser.add_argument('-l', action='store_true', help='List contents of reading list')
    parser.add_argument('--list', action='store_true', help='List contents of reading list')
    parser.add_argument('-r', action='store_true', help='Select random URL to visit.')
    parser.add_argument('-c', metavar='choice', help='Select URL by key name')
    parser.add_argument('-a', metavar='add', help='Add URL to reading list. Enter desired key '
        'at runtime and enter URL when prompted.')
    parser.add_argument('-d', metavar='delete', help='Delete entry from list')

    # Parse args
    args = parser.parse_args()
    
    # Read in list from file. NOTE: reading_list is a dict
    reading_list = read_from_list(reading_list_file)
    
    # Optionally output reading list contents and exit
    if (args.l or args.list):
        print(" "*17 + "Reading List:")
        print("="*50)
        for key, val in reading_list.items():
            print("\t{key}  [{value}]".format(key=key, value=val))
        print("="*50)

    # (Default/optional) Select random URL and go there
    elif (args.r or len(argv) == 1):
        
        # Randomly select URL from list dict
        selected_url = random.choice([i for i in reading_list.values()])
        
        # Open URL in default web browser. Opens new tab if window is open.
        webbrowser.open(selected_url)

    # Optionally select URL by name using key name
    elif (args.c):
        selection = args.c
        
        # Check if key is in reading list dict
        if (selection not in reading_list):
            sys.stderr.write("[!] Key not found in reading list.\n")
            sys.exit(1)

        # Open selected page
        webbrowser.open(reading_list[selection])
    
    # Add entry to list
    elif (args.a):
        addition = args.a

        # addition var holds key, so prompt user to get URL
        url = input('[>] URL: ')
        
        # Form entry string with key and url
        entry = ';;;'.join([addition, url])
        entry += '\n'

        # Write to file
        with open(reading_list_file, 'a') as fp:
            fp.write(entry)

    # Delete entry from list
    elif (args.d):
        entry_to_delete = args.d

        # Delete entry, and write back to file
        deleted = reading_list.pop(entry_to_delete)
        with open(reading_list_file, 'w') as fp:
            for key, val in reading_list.items():
                entry = ';;;'.join([key, val])
                fp.write(entry + '\n')

    return 0

if __name__ == '__main__':
    main(sys.argv)


