import socket
import json
import main

s = socket.socket()
host = "0.0.0.0"
port = 420

s.bind((host, port))
s.listen()

def main():
    while True:
        con, addr = s.accept()
        while con:
            data = con.recv(1024)
            if not data: break
            strn = str(data.decode('utf-8'))
            if(strn == None | strn == ""): strn = "{}"
            son = json.loads(strn)
            main.callback(son)

try:
    main()
except KeyboardInterrupt:
    print('\nProgram terminated due to keyboard interruption.')
finally:
    s.close()