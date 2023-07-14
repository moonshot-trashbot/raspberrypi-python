import asyncio
import socket
import json
import script

host = "0.0.0.0"
port = 420

global s
s = socket.socket()

def prepare():
    global s
    s.bind((host, port))
    s.listen()

    global thevar
    thevar = True

async def run():
    global thevar
    global s
    while thevar:
        con, addr = s.accept()
        while con:
            data = con.recv(1024)
            if not data: break
            strn = str(data.decode('utf-8'))
            if(strn == ""): strn = "{}\n"
            strn = strn.split("\\n")[0]
            script.callback(strn)

def stopper():
    global s
    global thevar
    s.close()
    thevar = False