# ****************************************
#
# CONTROLLER - (MANAGER.PY)
#
# This file controls the main runtime
# features for the sphero RVR robot
# from their developer kit.
#
# ****************************************


# ----------------------------------------
# PRE-CONFIGURATION
# ----------------------------------------


import sys
import asyncio
import driving
import asyncio
import time
import random
import _classes

sys.path.append('/home/pi/sphero-sdk-raspberrypi-python')
from sphero_sdk import Colors, SpheroRvrAsync, SerialAsyncDal, SpheroRvrTargets, SpheroRvrObserver

rvrObs = SpheroRvrObserver()


# ----------------------------------------
# PUBLIC FUNCTIONS
# ----------------------------------------

# OPEN() - Create and Setup Connection
async def open():
    rvrObs.wake()
    time.sleep(2)
    await leds_green()
    driving.open()

hazard = False
faround = False
alwaysHazard = False

# (ALL LED FUNCTIONS)
async def leds_reset():
    rvrObs.led_control.turn_leds_off()
    time.sleep(0.1)
async def leds_red():
    if(get_hazard()): return
    rvrObs.led_control.set_all_leds_color(color = Colors.red)
    time.sleep(0.1)
async def leds_purple():
    if(get_hazard()): return
    rvrObs.led_control.set_all_leds_color(color = Colors.pink)
    time.sleep(0.1)
async def leds_green():
    if(get_hazard()): return
    rvrObs.led_control.set_all_leds_color(color = Colors.green)
    time.sleep(0.1)

currentHeading = 0

def heading_shift(num):
    global currentHeading
    currentHeading = currentHeading + num
    if(currentHeading > 0):
        while(currentHeading > 358):
            currentHeading -= 359
    else:
        while(currentHeading < -358):
            currentHeading += 359

def heading_get():
    global currentHeading
    return currentHeading

async def drive_forward_seconds(spee, head, tim):
    heading_shift(head)
    driving.drive_forward_seconds(speed = spee, heading = heading_get(), time_to_drive = tim)

async def left_turn(num):
    num = abs(int(num)) * -1
    print("Left", num)
    await drive_forward_seconds(
        10,
        num,
        0
    )
async def right_turn(num):
    num = abs(int(num))
    print("Right", num)
    await drive_forward_seconds(
        10,
        num,
        0
    )

def get_faround():
    global faround
    return faround

def set_faround(to):
    global faround
    faround = to

async def move_sequence():
    global rvr
    while get_faround():
        await left_turn(random.randint(10, 25))
        time.sleep(random.randint(0, 5))
        await right_turn(random.randint(45, 180))
        time.sleep(random.randint(2, 4))
        await right_turn(random.randint(45, 180))
        time.sleep(random.randint(1, 2))
        await left_turn(random.randint(45, 180))
        time.sleep(random.randint(3, 8))
        await left_turn(random.randint(45, 180))
        time.sleep(random.randint(1, 4))
        await drive_forward_seconds(250, 0, 0)
        time.sleep(0.5)

async def sh_secondary():
    global rvr
    while get_hazard():
        ti1 = 1.5
        ti2 = 1.25
        time.sleep(ti2)
        await rvrObs.led_control.set_all_leds_color(color = Colors.yellow)
        time.sleep(ti1)
        await rvrObs.led_control.set_all_leds_color(color = Colors.orange)
        time.sleep(ti2)
        await rvrObs.led_control.set_all_leds_color(color = Colors.yellow)
        time.sleep(ti1)
        await rvrObs.led_control.set_all_leds_color(color = Colors.orange)
        time.sleep(ti2)
        await rvrObs.led_control.set_all_leds_color(color = Colors.yellow)
        time.sleep(ti1)
        await rvrObs.led_control.set_all_leds_color(color = Colors.orange)
        time.sleep(ti2)
        await rvrObs.led_control.set_all_leds_color(color = Colors.yellow)
        time.sleep(8)

def sh_secondary_wrapper():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(sh_secondary())

hThread = _classes.StoppableThread(target = sh_secondary_wrapper)

def get_hazard():
    global hazard
    return hazard

def set_hazard(setto):
    global hazard
    hazard = setto
    return hazard

def start_hazard():
    global hazard
    global hThread
    global alwaysHazard
    hazard = True
    hThread.start()
    hThread.join()

def always_hazard(yesorno):
    global alwaysHazard
    alwaysHazard = yesorno

async def cancel_hazard():
    global hazard
    global hThread
    global alwaysHazard
    hazard = False
    alwaysHazard = False
    hThread.stop()
    hThread = _classes.StoppableThread(target = sh_secondary_wrapper)

def battery_percentage_handler_hazard(battery_percentage):
    global hazard
    global hThread
    bp = battery_percentage_handler(battery_percentage)
    if(bp < 40):
        if(hazard is False):
            if(hThread is not None):
                start_hazard()
def battery_percentage_handler(battery_percentage):
    global hThread
    bp = battery_percentage["percentage"]
    if(bp is None): return
    bp = int(bp)
    print(">>> BATTERY: The battery is currently", str(bp) + "%", "full!")
    return bp
def battery_percentage(action):
    if(action is True):
        rvrObs.get_battery_percentage(handler=battery_percentage_handler_hazard)
    else:
        rvrObs.get_battery_percentage(handler=battery_percentage_handler)

# CLOSE() - Delete and Close Connection
async def close():
    await cancel_hazard()
    await leds_reset()
    driving.close()
    rvrObs.close()
    time.sleep(1)