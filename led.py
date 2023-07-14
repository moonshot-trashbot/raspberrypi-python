import sys
import time

sys.path.append('/home/pi/sphero-sdk-raspberrypi-python')

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import Colors

rvr = SpheroRvrObserver()

values = []
values2 = values.reverse()

def reset():
    rvr.led_control.turn_leds_off()

def emergency():
    rvr.led_control.set_all_leds_rgb(red = 254, green = 0, blue = 0)