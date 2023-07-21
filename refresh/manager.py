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
from sphero_sdk import Colors

# ----------------------------------------
# PUBLIC FUNCTIONS
# ----------------------------------------

# OPEN() - Create and Setup Connection
def open():
    driving.get_rvrObs().wake()
    time.sleep(2)
    driving.get_rvrObs().drive_control.reset_heading()
    time.sleep(1)
    leds_green()

hazard = False
faround = False
alwaysHazard = False

# (ALL LED FUNCTIONS)
def leds_reset():
    driving.get_rvrObs().led_control.turn_leds_off()
    time.sleep(0.1)
def leds_red():
    if(get_hazard()): return
    driving.get_rvrObs().led_control.set_all_leds_color(color = Colors.red)
    time.sleep(0.1)
def leds_purple():
    if(get_hazard()): return
    driving.get_rvrObs().led_control.set_all_leds_color(color = Colors.pink)
    time.sleep(0.1)
def leds_green():
    if(get_hazard()): return
    driving.get_rvrObs().led_control.set_all_leds_color(color = Colors.green)
    time.sleep(0.1)

currentHeading = 0

def heading_shift_fake(num):
    calc = heading_get() + num
    while(calc > 359 or calc < -359):
        while(calc > 358):
            calc -= 359
        while(calc < -358):
            calc += 359
    return calc

def heading_shift(num):
    global currentHeading
    calc = heading_shift_fake(num)
    currentHeading = calc
    return currentHeading

def heading_get():
    global currentHeading
    return currentHeading

def drive_forward_seconds(spee, head, tim):
    if(tim < 1):
        driving.get_debugs().headchange(heading_shift_fake(head))
        driving.turn_either_degrees(heading_get(), head)
    else:
        heading_shift(head)
        driving.get_debugs().headchange(heading_get())
        driving.drive_forward_seconds(spee, heading_get(), tim)

def left_turn(num):
    num = abs(int(num)) * -1
    print("Left", num)
    drive_forward_seconds(
        10,
        num,
        0
    )
def right_turn(num):
    num = abs(int(num))
    print("Right", num)
    drive_forward_seconds(
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

def move_sequence():
    global rvr
    while get_faround():
        left_turn(random.randint(10, 25))
        time.sleep(random.randint(0, 5))
        right_turn(random.randint(45, 180))
        time.sleep(random.randint(2, 4))
        right_turn(random.randint(45, 180))
        time.sleep(random.randint(1, 2))
        left_turn(random.randint(45, 180))
        time.sleep(random.randint(3, 8))
        left_turn(random.randint(45, 180))
        time.sleep(random.randint(1, 4))
        drive_forward_seconds(250, 0, 0)
        time.sleep(0.5)

def sh_secondary():
    global rvr
    while get_hazard():
        ti1 = 1.5
        ti2 = 1.25
        time.sleep(ti2)
        driving.get_rvrObs().led_control.set_all_leds_color(color = Colors.yellow)
        time.sleep(ti1)
        driving.get_rvrObs().led_control.set_all_leds_color(color = Colors.orange)
        time.sleep(ti2)
        driving.get_rvrObs().led_control.set_all_leds_color(color = Colors.yellow)
        time.sleep(ti1)
        driving.get_rvrObs().led_control.set_all_leds_color(color = Colors.orange)
        time.sleep(ti2)
        driving.get_rvrObs().led_control.set_all_leds_color(color = Colors.yellow)
        time.sleep(ti1)
        driving.get_rvrObs().led_control.set_all_leds_color(color = Colors.orange)
        time.sleep(ti2)
        driving.get_rvrObs().led_control.set_all_leds_color(color = Colors.yellow)
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

def cancel_hazard():
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
        driving.get_rvrObs().get_battery_percentage(handler=battery_percentage_handler_hazard)
    else:
        driving.get_rvrObs().get_battery_percentage(handler=battery_percentage_handler)

# CLOSE() - Delete and Close Connection
def close():
    cancel_hazard()
    leds_reset()
    driving.close()
    driving.get_rvrObs().close()
    time.sleep(1)