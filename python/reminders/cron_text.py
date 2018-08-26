#!/usr/bin/env python3

""" Create a cronjob to send a reminder text at a specific time """

from dateparser import parse
from crontab import CronTab

date = "tomorrow at 09:00"

date = parse(date)


