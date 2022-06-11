#!/usr/bin/env python
"""Flask app to handle setting and stopping alarms"""
import os
from crontab import CronTab
import sys
import signal
import json

from flask import render_template
from flask import Flask

app = Flask(__name__, static_url_path="")


def lookup_alarms():
    cron = CronTab(user="pi")
    return [str(job) for job in cron if job.is_enabled()]


def lookup_sounds():
    return [x.split(".")[0] for x in os.listdir("/home/pi/alarm/sounds")]


@app.route("/")
def hello():
    """
    entry point


    :return: returns basic "hello world" string
    """
    sounds = lookup_sounds()
    scheduled = [x.split() for x in lookup_alarms()]
    data = {"sounds": sounds, "scheduled": scheduled}
    return render_template("index.html", **data)


@app.route("/running_alarms")
def running_alarms():
    """
    gets list of running alarms
    :return: returns list of running alarms
    """
    return json.dumps(os.listdir("/home/pi/alarm/alarms"))


@app.route("/set_alarm/<newalarm>")
def set_alarm(newalarm):
    """
    sets and alarm
    :param newalarm: a string representing the alarm to dset
    :return: returns success or failure base on data
    """
    print(f"got back: {newalarm}")
    days, hours, sound = newalarm.split("-")
    if not days or not hours or not sound:
        return json.dumps("Failure")

    # determine days
    day_string = []
    for x in days:
        if x == "U":
            day_string.append(0)
        elif x == "M":
            day_string.append(1)
        elif x == "T":
            day_string.append(2)
        elif x == "W":
            day_string.append(3)
        elif x == "R":
            day_string.append(4)
        elif x == "F":
            day_string.append(5)
        elif x == "S":
            day_string.append(6)
        else:
            return json.dumps("Failure")

    times = hours.split(":")

    for day in day_string:

        cron = CronTab(user="pi")
        job = cron.new(command="/home/pi/alarm/alarm.py {0}".format(sound))
        job.dow.on(day)

        # determine hours
        job.hour.on(times[0])
        job.minute.on(times[1])
        # create new cron
        if job.is_valid():
            job.enable()
            cron.write()

    return json.dumps("success")


@app.route("/get_alarms")
def get_alarms():
    return json.dumps(lookup_alarms())


@app.route("/sounds")
def get_sounds():
    return json.dumps(lookup_sounds())


@app.route("/kill/<int:pid>")
def kill(pid):
    try:
        os.kill(pid, signal.SIGHUP)
        return "success"
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
