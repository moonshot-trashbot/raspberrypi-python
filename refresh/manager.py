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

sys.path.append('/home/pi/sphero-sdk-raspberrypi-python')
from sphero_sdk import Colors, SpheroRvrAsync, SerialAsyncDal, SpheroRvrTargets

loop = asyncio.get_event_loop()
rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)


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

async def __internal_hazard_on():
    await rvr.led_control.set_all_leds_color(color = Colors.yellow)
async def __internal_hazard_off():
    await rvr.led_control.turn_leds_off()
async def __internal_hazard():
    global hazard
    if(hazard is False): return
    await __internal_hazard_on()
    time.sleep(5)
    await __internal_hazard_off()
    time.sleep(5)

async def start_hazard():
    global hazard
    if(hazard is False):
        hazard = True
        while hazard:
            loop.run_until_complete(__internal_hazard())

def always_hazard(yesorno):
    global alwaysHazard
    alwaysHazard = yesorno

async def cancel_hazard():
    global alwaysHazard
    global hazard
    hazard = False
    alwaysHazard = False
    await rvr.led_control.turn_leds_off()

async def battery_percentage():
    time.sleep(0.1)
    x = await rvr.get_battery_percentage()
    return x

# CLOSE() - Delete and Close Connection
async def close():
    await leds_reset()
    await rvr.close()