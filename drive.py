import sys
import time

sys.path.append('/home/pi/sphero-sdk-raspberrypi-python')
from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()

def drive_forward_seconds(spee, head, tim):
    rvr.drive_control.drive_forward_seconds(
        speed=spee,       # This is out of 255, where 255 corresponds to 2 m/s
        heading=head,      # Valid heading values are 0-359
        time_to_drive=tim # Driving duration in seconds
    )
    time.sleep(1)

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
    rvr.drive_control.drive_forward_seconds(
        speed = 50,
        heading = 0,
        time_to_drive = 1
    )

def drive_backward():
    rvr.drive_control.drive_forward_seconds(
        speed = 50,
        heading = 0,
        time_to_drive = 1
    )

def turn_left():
    rvr.drive_control.drive_forward_seconds(
        speed = 10,
        heading = 45,
        time_to_drive = 1
    )

def turn_right():
    rvr.drive_control.drive_forward_seconds(
        speed = 10,
        heading = 315,
        time_to_drive = 1
    )

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
