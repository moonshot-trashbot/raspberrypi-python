import socket
import run

host = "0.0.0.0"
port = 420

sock = socket.socket()

def open():
    global sock
    sock.bind((host, port))
    sock.listen()

def accept():
    global sock
    con, addr = sock.accept()
    while con:
        data = con.recv(1024)
        if not data: break
        strn = str(data.decode('utf-8'))
        if(strn == ""): strn = "{}\n"
        strn = strn.split("\\n")[0]
        run.addition(strn)

def close():
    global sock
    sock.close()