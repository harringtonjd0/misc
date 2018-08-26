
""" Maintains a list of articles or websites to read/browse through
    and opens a browser window to a chosen or random selection """

import argparse
import random
from subprocess import Popen

chrome_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
list_location = r"C:\Users\Jake\Desktop\Reading_List.txt"

def main():
    
    # TODO Parse arguments from user

    # TODO Read from reading list file
    reading_list = ["facebook.com"]

    # Select URL to open
    selected_url = random.choice(reading_list)

    # Open browser window with selected URL
    Popen([chrome_location, selected_url])

if __name__ == '__main__':
    main()


