# git@github.com:jheise/alarmclock.git!/usr/bin/env python

import os
import sys
import time
import signal
import argparse

from syslog import syslog


def play_alarm(alarm):
    syslog("starting loop {0}".format(times))
    syslog("playing alarm")
    os.system("/usr/bin/mpg123 {0}".format(alarm))
    syslog("sleeping")
    time.sleep(10)


parser = argparse.ArgumentParser(description="Run an Alarm")
parser.add_argument(
    "-d", "--dry-run", action="store_true", help="play sound 3 times and stop"
)
parser.add_argument(
    "alarm", default="bell.mp3", help="What sound to play, default is bell.mp3"
)
args = parser.parse_args()

dry_run = args.dry_run

pid = str(os.getpid())
syslog("pid is {0}".format(pid))

sounds = "/home/pi/alarm/sounds/"
default = "bell.mp3"

running = True

current = "/home/pi/alarm/alarms/" + pid
with open(current, "w") as fh:
    fh.write(pid + "\n")

alarm = sounds + args.alarm
if not os.path.isfile(alarm):
    alarm = sounds + default

syslog("playing %s" % alarm)


def stopHandler(signum, frame):
    global running
    syslog("handler hit")
    running = False


times = 0

signal.signal(signal.SIGHUP, stopHandler)


if dry_run:
    for x in range(3):
        play_alarm(alarm)
else:
    while running:
        play_alarm(alarm)
syslog("running is now {0}".format(running))
os.remove(current)
