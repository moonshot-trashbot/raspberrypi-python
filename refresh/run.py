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
import json
import time
import asyncio
import _models
import manager
import listens
from threading import Thread

global run
global stopb
global recent

run = True
stopb = False
save = []
recent = int(time.time())


# ----------------------------------------
# PUBLIC FUNCTIONS
# ----------------------------------------

# REACCESS() - Get Next Processable Entry
async def reaccess():
    global save
    global recent
    global run
    if(save.__len__() > 0):
        x = save.pop(0)
        recent = int(time.time())
        return x
    else:
        final = 300
        sec = int(time.time()) - recent
        if(sec <= 5): await manager.leds_green()
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
    if(inp == "" or inp == "{}"): return Exception("No input data.")
    global save
    jso = json.loads(inp)
    new = _models.Detection(jso)
    save.append(new)
    return

moveaplifier = 0.133
tracking = -1
lastChance = int(time.time())-5

# PROCESS(Input) - Run Single Instruction [Async]
async def process(inp: _models.Detection or None):
    global tracking
    global lastChance
    await manager.leds_red()
    if(inp is None or inp is not _models.Detection): return
    print(">>> PROCESSES: Starting processing of following object...")
    print(inp)
    if(tracking == -1): tracking = inp.id
    if((int(time.time()) - lastChance) > 5): tracking = inp.id
    if(tracking == inp.id):
        lastChance = int(time.time())
        num = num * moveaplifier
        await manager.left_turn(10)
        await manager.right_turn(10)
    print(">>> PROCESSES: Finished Processing object, moving on.")
    pass

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
        if(x is not None and x is not {}):
            await process(x)

def coreSocket():
    listens.accept(addition)

def coreRobotWrapper():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        coreRobot()
    )

t2 = Thread(target = coreSocket)
t1 = Thread(target = coreRobotWrapper)

# STOP(Error) - Must Close Connections, Clean-up
async def stop(error):
    global stopb
    global run
    if(stopb is False):
        stopb = True
        run = False
        if(error is False):
            print(">>> TRACEBACK: Manually requested the program to close after sucessfull runtime. Ignore any following errors.")
        else:
            print(">>> TRACEBACK: Now forcing the program to close down... (check error log?)")
            print(error)
            traceback.print_tb(error.__traceback__, 5)
        await manager.close()
        listens.close()
        sys.exit(0)
    return None

async def main():
    try:
        print("Calling open - manager")
        await manager.open()
        print("Calling open - listener")
        listens.open()
    finally:
        try:
            t1.start()
            t2.start()
        except KeyboardInterrupt as e:
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            await stop(False)
            # t2.terminate()
            # t1.terminate()
        except Exception as e:
            await stop(e)
            # t2.terminate()
            # t1.terminate()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        main()
    )