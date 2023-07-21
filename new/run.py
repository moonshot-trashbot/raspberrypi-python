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

loop = asyncio.new_event_loop()
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

def runner():
    global cont
    global rvr

    async def main():
        global cont
        global rvr
        cont = True

        await rvr.wake()
        await asyncio.sleep(2)
        await rvr.led_control.set_all_leds_color(color = Colors.pink)

        tracking = {
            "id": None,
            "seen": 0,
            "center": [None, None]
        }

        while cont:
            message = sock.recv().decode("utf-8")
            print(">>> SOCKET: Receiving input from... please wait.")
            cont = False
            return message
        
        sock.term()
        await rvr.led_control.turn_off_leds()
        await rvr.close()
    asyncio.run(main())

try:
    thr = _classes.StoppableThread(target=runner)
    thr.start()
    thr.join()
except KeyboardInterrupt as e:
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    stop(False)
except Exception as e:
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    stop(e)