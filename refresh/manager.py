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

# sys.path.append('/home/pi/sphero-sdk-raspberrypi-python')
# from sphero_sdk import SpheroRvrObserver, Colors
# rvr = SpheroRvrObserver()


# ----------------------------------------
# PUBLIC FUNCTIONS
# ----------------------------------------

# OPEN() - Create and Setup Connection
def open():
    global rvr
    # rvr.wake()
    time.sleep(2)
    pass

# (ALL LED FUNCTIONS)
def leds_reset():
    global rvr
    # rvr.led_control.turn_leds_off()
def leds_red():
    global rvr
    # rvr.led_control.set_all_leds_rgb(Colors.RED)
def leds_green():
    global rvr
    # rvr.led_control.set_all_leds_rgb(Colors.GREEN)

# CLOSE() - Delete and Close Connection
def close():
    global rvr
    leds_reset()
    time.sleep(1)
    # rvr.close()
    time.sleep(1)
    pass