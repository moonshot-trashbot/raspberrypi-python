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
rvr = SpheroRvrObserver()

# loop = asyncio.get_event_loop()
# rvr = SpheroRvrAsync(
#     dal=SerialAsyncDal(
#         loop
#     )
# )

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
    global sock
    global rvr

    cont = True

    rvr.wake()
    time.sleep(2)
    rvr.led_control.set_all_leds_color(color = Colors.pink)
    time.sleep(0.05)
    rvr.reset_yaw()
    time.sleep(0.05)

    def movement(x, y):
        print("MVMT", x, y)
        if (x < 0): # turn right
            print("Break 1...")
            if (y < 0): ### turn forward
                rvr.raw_motors(left_mode=RawMotorModesEnum.forward.value, left_speed=45, right_mode=RawMotorModesEnum.off.value, right_speed=0)
                time.sleep(20)
                print("Break ^, pt. 2")
            if (y == 0): ### pivot in place
                rvr.raw_motors(left_mode=RawMotorModesEnum.forward.value, left_speed=45, right_mode=RawMotorModesEnum.reverse.value, right_speed=45)
                time.sleep(20)
                print("Break ^, pt. 2")
            if (y > 0): ### turn backward
                rvr.raw_motors(left_mode=RawMotorModesEnum.off.value, left_speed=0, right_mode=RawMotorModesEnum.reverse.value, right_speed=45)
                time.sleep(20)
                print("Break ^, pt. 2")
        elif (x == 0): # on target
            print("Break 2...")
            if (y < 0): ### drive forward
                rvr.raw_motors(left_mode=RawMotorModesEnum.forward.value, left_speed=45, right_mode=RawMotorModesEnum.forward.value, right_speed=45)
                time.sleep(20)
                print("Break ^, pt. 2")
            if (y == 0): ### stopped
                rvr.raw_motors(left_mode=RawMotorModesEnum.off.value, left_speed=0, right_mode=RawMotorModesEnum.off.value, right_speed=0)
                time.sleep(20)
                print("Break ^, pt. 2")
            if (y > 0): ### drive backward
                rvr.raw_motors(left_mode=RawMotorModesEnum.reverse.value, left_speed=45, right_mode=RawMotorModesEnum.reverse.value, right_speed=45)
                time.sleep(20)
                print("Break ^, pt. 2")
        elif (x > 0): # turn left
            print("Break 3...")
            if (y < 0): ### turn forward
                rvr.raw_motors(left_mode=RawMotorModesEnum.off.value, left_speed=0, right_mode=RawMotorModesEnum.forward.value, right_speed=45)
                time.sleep(20)
                print("Break ^, pt. 2")
            if (y == 0): ### pivot in place
                rvr.raw_motors(left_mode=RawMotorModesEnum.reverse.value, left_speed=45, right_mode=RawMotorModesEnum.forward.value, right_speed=45)
                time.sleep(20)
                print("Break ^, pt. 2")
            if (y > 0): ### turn backward
                rvr.raw_motors(left_mode=RawMotorModesEnum.reverse.value, left_speed=45, right_mode=RawMotorModesEnum.off.value, right_speed=0)
                time.sleep(20)
                print("Break ^, pt. 2")
                

    while cont:
        message = sock.recv().decode("utf-8")
        if(message is not None):
            jso = json.loads(message)
            rvr.reset_yaw()
            if(jso.__len__() > 0):
                detectPre = jso[0]
                detect = _models.Detection(detectPre)
                print(">>> RAW", detect)
                if(detect.area > 200):
                    previousFrame = detect.frame
                    print(">>>", detect)
                    cxy = deltafy(detect.center[0], detect.center[1], detect.top)
                    debugs.stripechange(int(int(cxy[0]+6)*120), int(int(cxy[1]+6)*120))
                    movement(cxy[0], cxy[1])

    rvr.led_control.turn_leds_off()
    time.sleep(0.05)
    rvr.close()
    time.sleep(1)
try:
    asyncio.run(runner())
except KeyboardInterrupt as e:
    rvr.led_control.turn_leds_off()
    time.sleep(0.05)
    rvr.close()
    time.sleep(1)
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    stop(False)
except Exception as e:
    rvr.led_control.turn_leds_off()
    time.sleep(0.05)
    rvr.close()
    time.sleep(1)
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    stop(e)
finally:
    rvr.led_control.turn_leds_off()
    time.sleep(0.05)
    rvr.close()
    time.sleep(1)