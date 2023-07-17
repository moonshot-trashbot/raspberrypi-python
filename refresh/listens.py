import socket
import json

global host
global port
global sock

host = "127.0.0.1"
port = 420
sock = socket.socket()
cont = True

def open():
    global sock
    sock.bind((host, port))
    sock.listen()

def accept(callback):
    while cont:
        con, addr = sock.accept()
        print(">>> SOCKET: Receiving input from", addr, "... please wait.")
        chunks = []
        streaming = True
        while streaming:
            chunkjoin = str("".join(chunks))
            data = con.recv(2)
            if not data:
                streaming = False
                if(chunkjoin != ""):
                    callback(chunkjoin)
                    chunks = []
            strng = str(data.decode('utf-8'))
            chunks.append(strng)

def close():
    return