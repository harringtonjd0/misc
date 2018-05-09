#!/usr/bin/env python3

import sys

def caesar(string, k):
    n = len(string)
    k %= 26
    s =  [ord(c.lower()) + k  if c.isalpha() else c for c in string]
    s = [letter - 26 if (isinstance(letter, int) and letter > ord('z')) else letter for letter in s]
    s = [chr(letter) if isinstance(letter, int) else letter for letter in s]
    s = ''.join([s[i].upper() if string[i].isupper() else s[i]  for i in range(n) ])
    print(s)

string = sys.argv[1]
k = int(sys.argv[2])

caesar(string, k)
