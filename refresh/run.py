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
import _models
import _classes
import manager
import listens

global run
global stopb
global recent

run = True
stopb = False
save = []
recent = int(time.time())
lastBattery = (int(time.time())-15)

# ----------------------------------------
# PUBLIC FUNCTIONS
# ----------------------------------------

green = False

async def battery():
    bp = await manager.battery_percentage()
    print("DEBUG_BP", bp)
    print(">>> BATTERY: The battery is currently", str(bp) + "%", "full!")

# REACCESS() - Get Next Processable Entry
async def reaccess():
    global save
    global run
    global recent
    global lastBattery
    global green
    lbm = int(time.time()) - lastBattery
    print("DEBUG_LBM", lbm)
    if(lbm >= 20):
        await battery()
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
                await battery()
                await manager.leds_green()
        if(sec <= 60): return
        if(sec <= (final - 180)):
            print(">>> PROCESSES: THERE IS NO QUEUE LEFT, IN", (str(300 - sec) + "s"),  "I WILL TURN OFF. [Checking every: 2s]")
            time.sleep(2)
        elif(sec <= (final - 120)):
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

# ADDITIOn(Input) - Add Item to Process Queue
def addition(inp):
    global save
    if(inp == "" or inp == "[]"): return Exception("No input data.")
    jso = json.loads(inp)
    for x in jso:
        new = _models.Detection(x)
        save.append(new)

moveaplifier = 0.133
tracking = -1
lastChance = int(time.time())-5

# PROCESS(Input) - Run Single Instruction [Async]
async def process(inp: _models.Detection or None):
    print(inp)
    global tracking
    global lastChance
    print(">>> PROCESSES: Starting processing of following object...")
    await manager.leds_red()
    print("Manager leds red")
    if(inp is None): return
    if(tracking == -1): tracking = inp.id
    if((int(time.time()) - lastChance) > 5): tracking = inp.id
    if(tracking == inp.id):
        lastChance = int(time.time())
        num = inp.center[0]
        num = num * moveaplifier
        if(num < 0):
            await manager.left_turn(10)
        else:
            await manager.right_turn(10)
        print(">>> TRACKING: Turned to continue following (", tracking, ").")
    else:
        print(">>> TRACKING: We aren't tracking ( ID:", inp.id, ") but they are in frame.")
    print(">>> PROCESSES: Finished Processing object, moving on.")

# QUIT() - Request to Close Connections, Clean-up
async def quit():
    await stop(False)
    sys.exit(130)


# ----------------------------------------
# MAIN INSTRUCTION
# ----------------------------------------

async def coreRobot():
    while True:
        x = await reaccess()
        if(x is not None):
            print("Quick processing")
            await process(x)
            print("Quick processing end")

def coreSocket():
    listens.accept(addition)

def coreRobotWrapper():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        coreRobot()
    )

t1 = _classes.StoppableThread(target = coreRobotWrapper)
t2 = _classes.StoppableThread(target = coreSocket)

# STOP(Error) - Must Close Connections, Clean-up
async def stop(error):
    global run
    run = False
    if(error is False):
        print(">>> TRACEBACK: Manually requested the program to close after sucessfull runtime. Ignore any following errors! This shutdown should take a few seconds.")
    else:
        print(">>> TRACEBACK: Now forcing the program to close down... (check error log?) This shutdown should take a few seconds.")
        print(error)
        traceback.print_tb(error.__traceback__, 5)
    await manager.close()
    listens.close()
    try:
        sys.exit(130)
    except SystemExit:
        os._exit(130)

async def main():
    try:
        try:
            print("Calling open - manager")
            await manager.open()
            print("Calling open - listener")
            listens.open()
        finally:
            t1.start()
            t2.start()
        t1.join()
        t2.join()
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