#!/usr/bin/env python3

from math import sqrt

def isprime(p):
	
	# Two is the first prime
	if p == 2:
		return 0

	# If number is even, it's not prime
	if not p&1:
		return 1
	
	# If number is 0, 1, or negative, its not prime
	elif p < 2:
		return 1
	
	# Only search for divisors <= sqrt(p)
	limit = int(sqrt(p))+1
	
	# Attempt to divide each odd number in range (3, limit) evenly
	for i in xrange(3, limit, 1):
		remainder = p % i
		if remainder != 0:
			return 1
	
	# If for loop completes, is prime.
	return 0


