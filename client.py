import socket
import json
import script

s = socket.socket()
host = "0.0.0.0"
port = 420

s.bind((host, port))
s.listen()

thevar = True

def run():
    while thevar:
        con, addr = s.accept()
        while con:
            data = con.recv(1024)
            if not data: break
            strn = str(data.decode('utf-8'))
            if(strn == ""): strn = "{}"
            son = json.loads(strn)
            script.callback(son)

def stopper():
    thevar = False

try:
    run()
except KeyboardInterrupt:
    print('\nProgram terminated due to keyboard interruption.')
finally:
    s.close()
    client.stopper()
    script.stopper()