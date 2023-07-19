import json
import time
import zmq

context = zmq.Context()
sock = context.socket(zmq.REP)
sock.bind("tcp://*:420")
cont = True

def open():
    global sock
    sock.bind("tcp://*:420")

def accept(callback):
    while cont:
        message = sock.recv().decode("utf-8")
        print(">>> SOCKET: Receiving input from... please wait.")
        print("RAW MSG", message)
        callback(message)

def close():
    sock.term()
    return