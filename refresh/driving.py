import sys
import asyncio
import time
import _classes

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
    if(queue.__len__() > 0):
        queue = queue.pop(0)
        return queue
    else:
        return None

queing = True

async def run():
    global queing
    while queing:
        x = queue_next()
        if(x is not None):
            await rvr.drive_control.drive_forward_seconds(speed=x["speed"], heading=x["heading"], time_to_drive=x["time_to_drive"])
            time.sleep(x["time_to_drive"] + 0.05)
        else:
            print(">>> ERROR: QUEUE IS NONETYPE IN RUN() FUNCTION.")
            time.sleep(1)

def run_wrapper():
    loop2 = asyncio.new_event_loop()
    loop2.run_until_complete(run())

global daemon
daemon = _classes.StoppableThread(target = run_wrapper)

def open():
    daemon.start()
    daemon.join()

def close():
    global daemon
    global queue
    global queing
    if(daemon.stopped() == False): daemon.stop()
    queue = []
    queing = False