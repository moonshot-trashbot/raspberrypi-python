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
                quit()
                return

# ADDITIOn(Input) - Add Item to Process Queue
def addition(inp):
    if(inp == "" or inp == "{}"): return Exception("No input data.")
    global save
    jso = json.loads(inp)
    new = _models.Detection(jso)
    save.append(new)
    return

# PROCESS(Input) - Run Single Instruction [Async]
async def process(inp):
    await manager.leds_red()
    if(inp is None): return
    print(">>> PROCESSES: Starting processing of following object...")
    print("   ", inp)
    await manager.left_turn()
    await manager.right_turn()
    print(">>> PROCESSES: Finished Processing object, moving on.")
    pass

# QUIT() - Request to Close Connections, Clean-up
def quit():
    stop(False)
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
def stop(error):
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
        manager.close()
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
            stop(False)
            # t2.terminate()
            # t1.terminate()
        except Exception as e:
            stop(e)
            # t2.terminate()
            # t1.terminate()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        main()
    )