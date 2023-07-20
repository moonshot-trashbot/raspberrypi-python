import sys
import asyncio
import time

sys.path.append('/home/pi/sphero-sdk-raspberrypi-python')
from sphero_sdk import SpheroRvrAsync, SerialAsyncDal

loop = asyncio.new_event_loop()
rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)

global queue
queue = []

def drive_forward_seconds(spee, head, time):
    global queue
    queue.append({
        "speed":spee,
        "heading":head,
        "time_to_drive":time
    })

def queue_next():
    global queue
    queue = queue.pop(0)
    return queue

async def run():
    global queing
    while queing:
        x = queue_next()
        if(x is not None):
            await rvr.drive_control.drive_forward_seconds(speed=x["speed"], heading=x["heading"], time_to_drive=x["time_to_drive"])
            time.sleep(x["time_to_drive"] + 0.05)
        else:
            print(">>> ERROR: QUEUE IS NONETYPE IN RUN() FUNCTION.")

def open():
    global loop
    loop.run_until_complete(run())

def close():
    global queue
    global queing
    queue = []
    queing = False