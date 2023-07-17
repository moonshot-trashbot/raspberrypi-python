import asyncio

import json
import modeling
import time

import prepare
import listener
import drive
import led

peoplemaybes = [1, 2, 19]

global tracking
tracking = 0
global lastFound
lastFound = 0

def getTracking():
    return tracking

def getLastFound():
    return lastFound

def setTracking(to):
    tracking = to

def setLastFound(to):
    lastFound = to

def main():
    prepare.prepare()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(drive.run())
    loop.run_until_complete(listener.run())

async def callback(son):
    js = json.loads(son)
    data = modeling.ReceivedDetection(js)
    box_x, box_y = data.center
    global tracking
    global lastFound
    if(data.type in peoplemaybes):
        if(tracking == 0):
            tracking = data.id
        else:
            if(data.id == tracking):
                lastFound = int(time.time())
            elif(lastFound < (int(time.time()) - 5)):
                    led.emergency()
                    tracking = data.id
                    lastFound = int(time.time())
        if(tracking == data.id):
            ab = abs(box_x)
            print("CONFIRMED TARGET IS CURRENT", ab)
            if(ab != 0):
                if(box_x < 0):
                    drive.turn_right()
                else:
                    drive.turn_left()

        print("TARGET", tracking, lastFound, getTracking(), getLastFound(), ">>>", box_x, box_y)
    else:
        print("No action for type " + str(data.type))

def stopper():
    drive.stopper()
    prepare.stopper()
    listener.stopper()

async def wrapper():
    try:
        main()
    except KeyboardInterrupt:
        stopper()
        print('\nProgram terminated with keyboard interrupt.')

loop = asyncio.get_event_loop()
loop.run_until_complete(wrapper())