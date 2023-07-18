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
import time
import _models
import _classes

sys.path.append('/home/pi/sphero-sdk-raspberrypi-python')
from sphero_sdk import Colors, SpheroRvrAsync, SerialAsyncDal, SpheroRvrTargets, SpheroRvrObserver

loop = asyncio.get_event_loop()
rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)
rvrObs = SpheroRvrObserver()


# ----------------------------------------
# PUBLIC FUNCTIONS
# ----------------------------------------

# OPEN() - Create and Setup Connection
async def open():
    await rvr.wake()
    time.sleep(2)
    await leds_green()

hazard = False
alwaysHazard = False

# (ALL LED FUNCTIONS)
async def leds_reset():
    await rvr.led_control.turn_leds_off()
    await rvr.led_control.turn_leds_off()
async def leds_red():
    if(get_hazard()): return
    await rvr.led_control.set_all_leds_color(color = Colors.red)
async def leds_green():
    if(get_hazard()): return
    await rvr.led_control.set_all_leds_color(color = Colors.green)

async def drive_forward_seconds(spee, head, tim):
    await rvr.drive_control.drive_forward_seconds(speed = spee, heading = head, time_to_drive = tim)
    time.sleep(1)

async def left_turn(num):
    num = abs(num)
    print("Left", num)
    await rvr.drive_control.reset_heading()
    await drive_forward_seconds(
        10,
        360-num,
        0.1
    )
async def right_turn(num):
    num = abs(num)
    print("Right", num)
    await rvr.drive_control.reset_heading()
    time.sleep(0.1)
    await drive_forward_seconds(
        10,
        num,
        0.1
    )

async def sh_secondary():
    global rvr
    while get_hazard():
        ti1 = 1.5
        ti2 = 1.25
        time.sleep(ti2)
        await rvr.led_control.set_all_leds_color(color = Colors.yellow)
        time.sleep(ti1)
        await rvr.led_control.set_all_leds_color(color = Colors.orange)
        time.sleep(ti2)
        await rvr.led_control.set_all_leds_color(color = Colors.yellow)
        time.sleep(ti1)
        await rvr.led_control.set_all_leds_color(color = Colors.orange)
        time.sleep(ti2)
        await rvr.led_control.set_all_leds_color(color = Colors.yellow)
        time.sleep(ti1)
        await rvr.led_control.set_all_leds_color(color = Colors.orange)
        time.sleep(ti2)
        await rvr.led_control.set_all_leds_color(color = Colors.yellow)
        time.sleep(8)
        drive_forward_seconds(254, 90, 3)
        drive_forward_seconds(10, 30, 10)
        drive_forward_seconds(254, 45, 10)
        drive_forward_seconds(10, 0, 10)

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
    await rvr.close()