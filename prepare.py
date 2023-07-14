import sys
import time
import led

sys.path.append('/home/pi/sphero-sdk-raspberrypi-python')
from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()

def prepare():
    rvr.wake()
    time.sleep(2)
    rvr.drive_control.reset_heading()
    led.reset()

def stopper():
    led.reset()
    rvr.close()