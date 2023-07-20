import json
import time
import zmq

context = zmq.Context()
sock = context.socket(zmq.PULL)
sock.bind("tcp://*:420")
cont = True

def accept():
    message = sock.recv().decode("utf-8")
    print(">>> SOCKET: Receiving input from... please wait.")
    return message

def close():
    pass