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
import json
import time
import asyncio
import driving
import math
import _models
import _classes
import manager
import listens

def custom_exponential_heading(x):
    k = 0.02  # Adjust this value to control the smoothness of the transition
    x0 = 167.5  # The midpoint between 20 and 315
    y_min = 20  # The value at x = 20
    y_max = 45  # The value at x = 315

    return y_min + (y_max - y_min) / (1 + math.exp(-k * (x - x0)))

def custom_exponential_forward(x):
    k = 0.02  # Adjust this value to control the smoothness of the transition
    x0 = 167.5  # The midpoint between 20 and 315
    y_min = 20  # The value at x = 20
    y_max = 45  # The value at x = 315

    return y_min + (y_max - y_min) / (1 + math.exp(-k * (x - x0)))

def calculate_heading(center_x):
    frame_width = 1280
    frame_center_x = frame_width / 2
    delta_x = center_x - frame_center_x
    return delta_x

def calculate_forward(center_y):
    frame_height = 720
    frame_center_y = frame_height / 2
    delta_y = center_y - frame_center_y
    return custom_exponential_forward(delta_y)

global run
global recent
global green
global faround

driving.get_debugs()

green = False
run = True
save = []
recent = int(time.time())
lastBattery = (int(time.time())-58)


# ----------------------------------------
# PUBLIC FUNCTIONS
# ----------------------------------------

async def battery(dosum):
    time.sleep(0.05)
    bp = manager.battery_percentage(dosum)

def get_faround():
    global faround
    return faround

def randomize():
    turn = random.randint(45, 315)
    driving.drive_forward_seconds(5, turn, 0)

# REACCESS() - Get Next Processable Entry
async def reaccess():
    global save
    global run
    global recent
    global faround
    global lastBattery
    global green
    lbm = int(time.time()) - lastBattery
    if(lbm >= 60):
        faround = False
        await battery(True)
        lastBattery = int(time.time())
    if(save.__len__() > 0):
        x = save.pop(0)
        recent = int(time.time())
        await process(x)
        return
    else:
        final = 300
        sec = int(time.time()) - recent
        if(sec >= 10):
            if(green is False):
                green = True
                await battery(False)
                manager.leds_purple()
        if(sec <= 60):
            randomize()
            return
        if(sec <= (final - 180)):
            print(">>> PROCESSES: THERE IS NO QUEUE LEFT, IN", (str(300 - sec) + "s"),  "I WILL TURN OFF. [Checking every: 2s]")
            randomize()
            time.sleep(2)
        elif(sec <= (final - 120)):
            manager.set_faround(False)
            print(">>> PROCESSES: THERE IS NO QUEUE LEFT, IN", (str(300 - sec) + "s"),  "I WILL TURN OFF. [Checking every 5s]")
            time.sleep(5)
        elif(sec < (final - 60)):
            print(">>> PROCESSES: THERE IS NO QUEUE LEFT, IN", (str(300 - sec) + "s"),  "I WILL TURN OFF. [Checking every 10s]")
            time.sleep(10)
        else:
            if(sec >= final):
                run = False
                print(">>> NOTICE: Finished processing, inactive for over 5 minutes, shutting down.")
                await quit()
                return

tracking = -1
lastChance = int(time.time())-5

# ADDITION(Input) - Add Item to Process Queue
def addition(inp):
    global save
    global tracking
    if(inp == "" or inp == "[]"): return Exception("No input data.")
    jso = json.loads(inp)
    if (jso.__len__() == 1): tracking = jso[0].id
    for x in jso:
        new = _models.Detection(x)
        save.append(new)

async def parse(inp: str):
    if(inp is None or inp is {}): return None
    return save.append(_models.Detection(inp))

# PROCESS(Input) - Run Single Instruction [Async]
async def process(inp: _models.Detection or None):
    global tracking
    global lastChance
    manager.leds_red()
    if(inp is None): return
    obj_id = inp.id
    if(obj_id == -1): return
    obj_class = inp.type
    center_x, center_y = inp.center
    if((int(time.time()) - lastChance) > 5): tracking = -1
    if(tracking == obj_id or tracking == -1):
        tracking = obj_id
        lastChance = int(time.time())
        heading_change = calculate_heading(center_x)
        driving.get_debugs().stripechange(center_x, center_y)
        if heading_change > 50:
            manager.left_turn(10)
        elif heading_change < -50:
            manager.right_turn(10)
        print(">>> TRACKING: We turned to continue tracking (", tracking, "). Debug...", "\nCXY:", center_x, center_y, "\nHEADCHANGE", heading_change)
    else:
        print(">>> TRACKING: We aren't tracking box ( ID:", inp.id, ") but it is in frame.")

# QUIT() - Request to Close Connections, Clean-up
async def quit():
    await stop(False)


# ----------------------------------------
# MAIN INSTRUCTION
# ----------------------------------------

# STOP(Error) - Must Close Connections, Clean-up
async def stop(error):
    global run
    global server_object
    run = False
    if(error is False):
        print(">>> TRACEBACK: Manually requested the program to close after sucessfull runtime. Ignore any following errors! This shutdown should take a few seconds.")
    else:
        print(">>> TRACEBACK: Now forcing the program to close down... (check error log?) This shutdown should take a few seconds.")
        print(error)
        traceback.print_tb(error.__traceback__, 10)
    manager.close()
    listens.close()
    try:
        sys.exit(130)
    except SystemExit:
        os._exit(130)

async def main():
    global run
    try:
        print(">>> OPENING: Hardware Manager")
        manager.open()
        print(">>> OPENING: Socket Listener")
        run = True
        while run:
            await reaccess()
            await driving.run()
            y = listens.accept()
            if(y is None): return None
            jso = json.loads(y)
            if(jso is None): return None
            for x in jso:
                z = await parse(x)
    except KeyboardInterrupt as e:
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        await stop(False)
    except Exception as e:
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        await stop(e)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        main()
    )