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

import os
import time
import json
import _models
import manager
import listens
from threading import Thread

run = True
stopb = False
save = []


# ----------------------------------------
# PUBLIC FUNCTIONS
# ----------------------------------------

# REACCESS() - Get Next Processable Entry
def reaccess():
    global save
    x = save.pop()
    return x

def addition(inp):
    global save
    jso = json.loads(inp)
    new = _models.Detection(jso)
    save.append(new)

# PROCESS(Object) - Run Single Instruction
def process(inp):
    print(inp)
    pass

# STOP() - Close Connections, Clean-up
def stop():
    global stopb
    if(stopb is False):
        stopb = True
        print("Now forcing the program to close down... (check error log if not manually triggered.)")
        manager.close()
        listens.close()


# ----------------------------------------
# MAIN INSTRUCTION
# ----------------------------------------

def coreRobot():
    manager.open()
    global run
    while run:
        try:
            x = reaccess()
            if(x is not None and x is not {}):
                # (?) Add more here, maybe.
                process(x)
        except:
            run = False
            stop()
    stop()

def coreSocket():
    listens.open()
    global run
    while run:
        try:
            listens.accept()
        except:
            run = False
            stop()
    stop()

Thread(target = coreRobot).start()
Thread(target = coreSocket).start()