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
async def leds_red():
    await rvr.led_control.set_all_leds_color(color = Colors.red)
async def leds_green():
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
    global hazard
    while hazard:
        rvrObs.led_control.set_all_leds_color(color = Colors.yellow)
        time.sleep(1)
        rvrObs.led_control.set_all_leds_color(color = Colors.white)
        time.sleep(1)

hThread = _classes.StoppableThread(target = sh_secondary)
hThread.join()

def start_hazard():
    global hazard
    global alwaysHazard
    hazard = True
    hThread.start()

def always_hazard(yesorno):
    global alwaysHazard
    alwaysHazard = yesorno

async def cancel_hazard():
    global hazard
    global alwaysHazard
    hazard = False
    alwaysHazard = False
    hThread.stop()
    hThread = _classes.StoppableThread(target = sh_secondary)
    hThread.join()

def battery_percentage_handler(battery_percentage):
    global hThread
    bp = battery_percentage["percentage"]
    if(bp is None): return
    bp = int(bp)
    print(">>> BATTERY: The battery is currently", str(bp) + "%", "full!")
    if(bp < 40):
        if(hazard is False):
            if(hThread is not None):
                start_hazard()
def battery_percentage():
    rvrObs.get_battery_percentage(handler=battery_percentage_handler)

# CLOSE() - Delete and Close Connection
async def close():
    await leds_reset()
    await rvr.close()