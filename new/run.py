# ****************************************
#
# RUNTIME - (RUN.PY)
#
# This file controls the main runtime
# program for the sphero RVR and
# server socket connection.
#
# ****************************************


# ----------------------------------------
# PRE-CONFIGURATION
# ----------------------------------------

import traceback
import signal
import random
import sys
import os
import asyncio
import json
import time
import asyncio
import math
import random
import debugs
import _models
import _classes
import zmq

sys.path.append('/home/pi/sphero-sdk-raspberrypi-python')
from sphero_sdk import Colors, SpheroRvrAsync, SerialAsyncDal, SpheroRvrTargets, SpheroRvrObserver

loop = asyncio.get_event_loop()
rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)

context = zmq.Context()
sock = context.socket(zmq.PULL)
sock.bind("tcp://*:420")

cont = True

def stop(error):
    global cont
    cont = False
    if(error is False):
        print(">>> TRACEBACK: Manually requested the program to close after sucessfull runtime. Ignore any following errors! This shutdown should take a few seconds.")
    else:
        print(">>> TRACEBACK: Now forcing the program to close down... (check error log?) This shutdown should take a few seconds.")
        print(error)
        traceback.print_tb(error.__traceback__, 10)
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
        exit()

def deltafy(xarr1, xarr2, xarr2top):
    return [int((1280-int(xarr1))/120)-6, int(((int(xarr2)+xarr2top)/2)/120)-6]

async def runner():
    global cont
    global rvr
    global sock

    cont = True

    await rvr.wake()
    await asyncio.sleep(2)
    await rvr.led_control.set_all_leds_color(color = Colors.pink)
    await asyncio.sleep(0.05)

    tracking = {
        "id": None,
        "seen": 0,
        "center": [None, None]
    }

    async def turnleft(deg):
        await rvr.drive_control.reset_heading()
        await rvr.drive_control.turn_left_degrees(0, deg)
        await asyncio.sleep(0.3)
        return
    async def turnright(deg):
        await rvr.drive_control.reset_heading()
        await rvr.drive_control.turn_right_degrees(0, deg)
        await asyncio.sleep(0.3)
        return
    async def goforward(sec):
        await rvr.drive_control.reset_heading()
        await rvr.drive_control.drive_forward_seconds(45, 0, 1)
        await asyncio.sleep(0.8)
        return
    async def gobackward(sec):
        await rvr.drive_control.reset_heading()
        await rvr.drive_control.drive_backward_seconds(45, 0, 1)
        await asyncio.sleep(0.8)
        return

    while cont:
        message = sock.recv().decode("utf-8")
        print(">>> SOCKET: Receiving input from... please wait.")
        print(">>> RAW", message)
        if(message is None): return
        jso = json.loads(message)
        if(jso.__len__() > 0):
            detectPre = jso[0]
            detect = _models.Detection(detectPre)
            print(">>>", detect)
            cxy = deltafy(detect.center[0], detect.center[1], detect.top)
            debugs.stripechange(int(int(cxy[0]+6)*120), int(int(cxy[1]+6)*120))
            print(cxy)
            if(cxy[0] > 0): await turnleft(8)
            if(cxy[0] < 0): await turnright(8)
            if(cxy[1] < 0): await goforward(1)
            if(cxy[1] > 0): await gobackward(1)

    sock.term()
    await rvr.led_control.turn_off_leds()
    await rvr.close()
try:
    asyncio.run(runner())
except KeyboardInterrupt as e:
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    stop(False)
except Exception as e:
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    stop(e)