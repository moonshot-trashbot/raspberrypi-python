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
import time
import _models

sys.path.append('/home/pi/sphero-sdk-raspberrypi-python')
from sphero_sdk import SpheroRvrObserver, Colors
rvr = SpheroRvrObserver()


# ----------------------------------------
# PUBLIC FUNCTIONS
# ----------------------------------------

# OPEN() - Create and Setup Connection
def open():
    rvr.wake()
    time.sleep(2)

# (ALL LED FUNCTIONS)
def leds_reset():
    rvr.led_control.turn_leds_off()
    time.sleep(0.1)
def leds_red():
    rvr.led_control.set_all_leds_rgb(Colors.RED)
    time.sleep(0.1)
def leds_green():
    rvr.led_control.set_all_leds_rgb(Colors.GREEN)
    time.sleep(0.1)

def drive_forward_seconds(spee, head, tim):
    rvr.drive_control.drive_forward_seconds(speed = spee, heading = head, time_to_drive = tim)
    time.sleep(tim)

def left_turn():
    rvr.drive_control.reset_heading()
    time.sleep(0.1)
    drive_forward_seconds(
        10,
        45,
        0
    )
def right_turn():
    rvr.drive_control.reset_heading()
    time.sleep(0.1)
    drive_forward_seconds(
        10,
        315,
        0
    )

# CLOSE() - Delete and Close Connection
def close():
    global rvr
    leds_reset()
    rvr.close()
    time.sleep(0.1)