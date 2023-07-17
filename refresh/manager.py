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
    await asyncio.sleep(2)
    await leds_green()

# (ALL LED FUNCTIONS)
async def leds_reset():
    await rvr.led_control.turn_leds_off()
    await asyncio.sleep(1)
async def leds_red():
    await rvr.led_control.set_all_leds_color(color = Colors.red)
    await asyncio.sleep(1)
async def leds_green():
    await rvr.led_control.set_all_leds_color(color = Colors.green)
    await asyncio.sleep(1)

async def drive_forward_seconds(spee, head, tim):
    await rvr.drive_control.drive_forward_seconds(speed = spee, heading = head, time_to_drive = tim)
    await asyncio.sleep(1)

async def left_turn(num):
    num = abs(num)
    await rvr.drive_control.reset_heading()
    await drive_forward_seconds(
        10,
        360-num,
        0.1
    )
async def right_turn(num):
    num = abs(num)
    await rvr.drive_control.reset_heading()
    await drive_forward_seconds(
        10,
        num,
        0.1
    )

# CLOSE() - Delete and Close Connection
async def close():
    await leds_reset()
    await rvr.close()