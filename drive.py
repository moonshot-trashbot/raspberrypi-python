import sys  # Allows us to use sys.path.append below
import time # Allows us to insert delays in our script

# sys.path tells the interpreter where to look for modules.
# Tell it to look in the SDK directory as well.
sys.path.append('/home/pi/sphero-sdk-raspberrypi-python')

# We're 
from sphero_sdk import SpheroRvrObserver

# Instantiate (create) a SpheroRvrObserver object
rvr = SpheroRvrObserver()

# This tells the Python interpreter that we are defining 
# a function named main that takes no arguments
def main():
    # Make sure RVR is awake and ready to receive commands
    rvr.wake()
    
    # Wait for RVR to wake up
    time.sleep(2)

    # Now RVR is ready for action.  Add new stuff here.
    rvr.drive_control.drive_forward_seconds(
        speed=64,       # This is out of 255, where 255 corresponds to 2 m/s
        heading=0,      # Valid heading values are 0-359
        time_to_drive=1 # Driving duration in seconds
    )

    

# This block gets executed if the interpreter is directly running this
# file, not importing it as a module.  It's a good general practice
if __name__ == '__main__':
    try:
        # Stuff we want to do (in this case, just call our main function)
        main()

    except KeyboardInterrupt:
        # What to do if there's a keyboard interrupt (ctrl+c) exception
        # In this case, we're just going to print a message
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        # What to do before we exit the block
        rvr.close()

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

# def drive_forward():
#     rvr.drive_control.drive_forward_seconds(
#         speed = 50,
#         heading = 0,
#         time_to_drive = 1
#     )

# def drive_backward():
#     rvr.drive_control.drive_forward_seconds(
#         speed = 50,
#         heading = 0,
#         time_to_drive = 1
#     )

# def turn_left():
#     rvr.drive_control.drive_forward_seconds(
#         speed = 10,
#         heading = 45,
#         time_to_drive = 1
#     )

# def turn_right():
#     rvr.drive_control.drive_forward_seconds(
#         speed = 10,
#         heading = 315,
#         time_to_drive = 1
#     )

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
