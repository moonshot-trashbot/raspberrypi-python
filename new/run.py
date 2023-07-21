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
from sphero_sdk import Colors, SpheroRvrAsync, SerialAsyncDal, SpheroRvrTargets, SpheroRvrObserver, RawMotorModesEnum

# loop = asyncio.get_event_loop()
# rvr = SpheroRvrAsync(
#     dal=SerialAsyncDal(
#         loop
#     )
# )
rvr = SpheroRvrObserver()

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

previousFrame = 0

def deltafy(xarr1, xarr2, xarr2top):
    return [int((1280-int(xarr1))/120)-6, int(((int(xarr2)+xarr2top)/2)/120)-6]

async def runner():
    global previousFrame
    global cont
    global rvr
    global sock

    cont = True

    rvr.wake()
    time.sleep(2)
    rvr.led_control.set_all_leds_color(color = Colors.pink)
    time.sleep(0.05)
    
    def raw_motors(lspeed, _lmode, rspeed, _rmode):
        if(lspeed == 0 and rspeed == 0): return
        if(_lmode == 0 and _rmode == 0): return
        left_mode = RawMotorModesEnum.off.value
        if(_lmode == 1): left_mode = RawMotorModesEnum.forward.value
        if(_lmode == 2): left_mode = RawMotorModesEnum.reverse.value
        right_mode = RawMotorModesEnum.off.value
        if(_rmode == 1): right_mode = RawMotorModesEnum.forward.value
        if(_rmode == 2): right_mode = RawMotorModesEnum.reverse.value
        left_speed = lspeed
        right_speed = rspeed
        if(left_speed is None or not left_speed): left_speed = 0
        if(right_speed is None or not right_speed): right_speed = 0
        print({left_mode, right_mode, left_speed, right_speed})
        rvr.raw_motors(
            left_mode=left_mode,
            left_speed=left_speed,
            right_mode=right_mode,
            right_speed=right_speed
        )
        time.sleep(1)

    def movement(x, y):
        if (x < 0): # turn right
            if (y < 0): ### turn forward
                raw_motors(45, 1, 0, 0)
            if (y == 0): ### pivot in place
                raw_motors(45, 1, 45, 2)
            if (y > 0): ### turn backward
                raw_motors(0, 0, 45, 2)
        elif (x == 0): # on target
            if (y < 0): ### drive forward
                raw_motors(45, 1, 45, 1)
            if (y == 0): ### stopped
                raw_motors(0, 0, 0, 0)
            if (y > 0): ### drive backward
                raw_motors(45, 2, 45, 2)
        elif (x > 0): # turn left
            if (y < 0): ### turn forward
                raw_motors(0, 0, 45, 1)
            if (y == 0): ### pivot in place
                raw_motors(45, 2, 45, 1)
            if (y > 0): ### turn backward
                raw_motors(45, 2, 0, 0)
                

    while cont:
        message = sock.recv().decode("utf-8")
        if(message is not None):
            jso = json.loads(message)
            rvr.reset_yaw()
            if(jso.__len__() > 0):
                detectPre = jso[0]
                detect = _models.Detection(detectPre)
                print(">>> RAW", detect)
                if(detect.frame != previousFrame and detect.width > 100 and detect.area > 40000):
                    previousFrame = detect.frame
                    print(">>>", detect)
                    cxy = deltafy(detect.center[0], detect.center[1], detect.top)
                    debugs.stripechange(int(int(cxy[0]+6)*120), int(int(cxy[1]+6)*120))
                    movement(cxy[0], cxy[1])

    sock.term()
    rvr.led_control.turn_off_leds()
    rvr.close()
try:
    asyncio.run(runner())
except KeyboardInterrupt as e:
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    stop(False)
except Exception as e:
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    stop(e)
