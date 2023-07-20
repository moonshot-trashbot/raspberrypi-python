import sys
import asyncio
import time
import _classes

sys.path.append('/home/pi/sphero-sdk-raspberrypi-python')
from sphero_sdk import Colors, SpheroRvrAsync, SerialAsyncDal, SpheroRvrTargets, SpheroRvrObserver

rvrObs = SpheroRvrObserver()
def get_rvrObs():
    global rvrObs
    return rvrObs

queue = []

def turn_either_degrees(start, amount):
    global queue
    queue.append({
        "type": "turn_either_degrees",
        "heading": start,
        "amount": amount
    })

def drive_forward_seconds(spee, head, time):
    global queue
    queue.append({
        "type": "drive_forward_seconds",
        "speed": spee,
        "heading": head,
        "time_to_drive": time
    })

def queue_next():
    global queue
    if(queue.__len__() > 0):
        nextest = queue.pop(0)
        return nextest
    else:
        return None

queing = True

async def run():
    while queue.__len__() > 0:
        x = queue_next()
        if(x is not None):
            if(x["type"] == "drive_forward_seconds"):
                print(">>> QUEUE TRYING:", x)
                rvrObs.drive_control.drive_forward_seconds(speed=x["speed"], heading=x["heading"], time_to_drive=x["time_to_drive"])
                time.sleep(x["time_to_drive"] + 0.1)
            elif(x["type"] == "turn_either_degrees"):
                func = rvrObs.drive_control.turn_right_degrees
                if(x["amount"] < 0): func = rvrObs.drive_control.turn_left_degrees
                func(heading=x["heading"], amount=x["amount"])
        else:
            print(">>> ERROR: QUEUE IS NONETYPE IN RUN() FUNCTION.")
            time.sleep(1)

def close():
    global queue
    global queing
    queue = []
    queing = False