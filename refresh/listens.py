import json
import time
import zmq

context = zmq.Context()
sock = context.socket(zmq.PULL)
sock.bind("tcp://*:420")
cont = True

def accept(callback):
    message = sock.recv().decode("utf-8")
    print(">>> SOCKET: Receiving input from... please wait.")
    print("RAW MSG", message)
    callback(message)

def close():
    sock.term()
    return