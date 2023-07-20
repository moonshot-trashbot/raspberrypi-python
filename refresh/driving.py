import sys
import asyncio
import time
import _classes

sys.path.append('/home/pi/sphero-sdk-raspberrypi-python')
from sphero_sdk import SpheroRvrAsync, SerialAsyncDal

loop = asyncio.get_event_loop()
rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)

queue = []

def drive_forward_seconds(spee, head, time):
    global queue
    queue.append({
        "speed": spee,
        "heading": head,
        "time_to_drive": time
    })

def queue_next():
    global queue
    if(queue.__len__() > 0):
        nextest = queue.pop(0)
        return nextest
    else:
        return None

queing = True

async def run():
    global queing
    global rvr
    while queing:
        x = queue_next()
        if(x is not None):
            if(x["speed"] < 0): x["speed"] = 0
            if(x["speed"] > 255): x["speed"] = 255
            if(x["heading"] < 0): x["heading"] = 0
            if(x["heading"] > 359): x["heading"] = 359
            print(">>> ERROR: QUEUE TRYING:", x)
            await rvr.drive_control.drive_forward_seconds(speed=x["speed"], heading=x["heading"], time_to_drive=x["time_to_drive"])
            time.sleep(x["time_to_drive"] + 0.05)
        else:
            print(">>> ERROR: QUEUE IS NONETYPE IN RUN() FUNCTION.")
            time.sleep(1)

def run_wrapper():
    loop2 = asyncio.new_event_loop()
    asyncio.set_event_loop(loop2)
    loop2.run_until_complete(run())

global daemon
daemon = _classes.StoppableThread(target = run_wrapper)

def open():
    daemon.start()

def close():
    global daemon
    global queue
    global queing
    if(daemon.stopped() == False): daemon.stop()
    queue = []
    queing = False