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
import sys
import os
import json
import time
import asyncio
import math
import _models
import _classes
import manager
import listens

def calculate_heading(center_x, center_y):
    # The width and height of the frame shot
    frame_width = 1280
    frame_height = 720

    # Center of the frame
    frame_center_x = frame_width / 2
    frame_center_y = frame_height / 2

    # Calculate the difference in x and y coordinates from the center of the frame
    delta_x = center_x - frame_center_x
    delta_y = center_y - frame_center_y

    # Calculate the angle (in degrees) to rotate the robot
    angle_rad = math.atan2(delta_y, delta_x)
    angle_deg = math.degrees(angle_rad)

    return angle_deg

global run
global recent
global green
global faround

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
    print("Start bat")
    bp = manager.battery_percentage(dosum)

def get_faround():
    global faround
    return faround

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
        return x
    else:
        final = 300
        sec = int(time.time()) - recent
        if(sec >= 10):
            if(green is False):
                green = True
                await battery(False)
                manager.leds_purple()
                def faround():
                    manager.set_faround(True)
                    newl = asyncio.new_event_loop()
                    asyncio.set_event_loop(newl)
                    newl.run_until_complete(manager.move_sequence())
        if(sec <= 60): return
        if(sec <= (final - 180)):
            print(">>> PROCESSES: THERE IS NO QUEUE LEFT, IN", (str(300 - sec) + "s"),  "I WILL TURN OFF. [Checking every: 2s]")
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

# ADDITION(Input) - Add Item to Process Queue
def addition(inp):
    global save
    if(inp == "" or inp == "[]"): return Exception("No input data.")
    jso = json.loads(inp)
    for x in jso:
        new = _models.Detection(x)
        save.append(new)

moveaplifier = 0.0133
tracking = -1
lastChance = int(time.time())-5

async def parse(inp: str):
    if(inp is None or inp is {}): return None
    return await process(_models.Detection(inp))

# PROCESS(Input) - Run Single Instruction [Async]
async def process(inp: _models.Detection or None):
    print(inp)
    global tracking
    global lastChance
    print(">>> PROCESSES: Starting processing of following object...")
    manager.leds_red()
    print("Manager leds red")
    if(inp is None): return
    obj_id = inp.id
    obj_class = inp.type
    center_x, center_y = inp.center
    if((int(time.time()) - lastChance) > 5): tracking = None
    if(tracking == obj_id or tracking == -1):
        tracking = obj_id
        lastChance = int(time.time())

        heading_change = calculate_heading(center_x, center_y)
        if heading_change < 0:
            manager.turn_left(abs(heading_change))
        else:
            manager.turn_right(heading_change)
        print(">>> TRACKING: We turned to continue tracking (", tracking, "). Debug...", "\nCXY:", center_x, center_y, "\nHEADCHANGE", heading_change)
    else:
        print(">>> TRACKING: We aren't tracking box ( ID:", inp.id, ") but it is in frame.")
    print(">>> PROCESSES: Finished Processing object, moving on.")

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
        traceback.print_tb(error.__traceback__, 5)
    manager.close()
    listens.close()
    try:
        sys.exit(130)
    except SystemExit:
        os._exit(130)

async def main():
    global run
    try:
        print("Calling open - manager")
        manager.open()
        print("Calling open - listener")
        run = True
        while run:
            print("Trying accept")
            y = listens.accept()
            if(y is None): return None
            print("... from Trying accept: not none")
            jso = json.loads(y)
            if(jso is None): return None
            for x in jso:
                z = await parse(x)
                print("Break 1")
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