#!/usr/bin/env python3

from math import sqrt

def isprime(p):
	if not p&1:
		return 1
	elif p < 3:
		return 1
	limit = int(sqrt(p))+1
	for i in range(3, limit, 1):
		remainder = p % i
		if remainder != 0:
			return 1
	# If for loop completes, is prime.
	return 0


