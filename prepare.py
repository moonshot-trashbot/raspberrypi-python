import sys
import time

sys.path.append('/home/pi/sphero-sdk-raspberrypi-python')
from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()

def prepare():
    rvr.wake()
    time.sleep(2)
    rvr.drive_control.reset_heading()

def unpare():
    rvr.close()