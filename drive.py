import asyncio
import sys
import time

sys.path.append('/home/pi/sphero-sdk-raspberrypi-python')
from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()

global queue
queue = []

global queueStart
queueStart = True

def drive_forward_seconds(spee, head, tim):
    global queue
    queue.append({
        "speed": spee,
        "heading": head,
        "time_to_drive": tim
    })

# import sys
# import time

# sys.path.append('/home/pi/sphero-sdk-raspberrypi-python')

# from sphero_sdk import SpheroRvrObserver

# rvr = SpheroRvrObserver()

# def main():
#     rvr.wake()
#     time.sleep(2)

#     rvr.drive_control.drive_forward_seconds(
#         speed = 64,
#         heading = 45,
#         time_to_drive = 1
#     )

#     rvr.drive_control.drive_backward_seconds(
#         speed = 64,
#         heading = 45,
#         time_to_drive = 2
#     )

def drive_forward():
    drive_forward_seconds(
        50,
        0,
        1
    )

def drive_backward():
    drive_forward_seconds(
        50,
        0,
        1
    )

def turn_left():
    drive_forward_seconds(
        10,
        45,
        0
    )

def turn_right():
    drive_forward_seconds(
        10,
        315,
        0
    )

async def run():
    global queueStart
    while(queueStart is True):
        print("RUN NOTHING QUEUE")
        if(queue.__len__() > 0):
            current = queue.pop(0)
            print(current)
            rvr.drive_control.drive_forward_seconds(speed = int(current["speed"]), heading = int(current["heading"]), time_to_drive = int(current["time_to_drive"]))
        time.sleep(1)

def stopper():
    global queueStart
    queueStart = False

# if __name__ == '__main__':
#     try:
#         # Stuff we want to do (in this case, just call our main function)
#         main()

#     except KeyboardInterrupt:
#         # What to do if there's a keyboard interrupt (ctrl+c) exception
#         # In this case, we're just going to print a message
#         print('\nProgram terminated with keyboard interrupt.')

#     finally:
#         # What to do before we exit the block
#         rvr.close()
