import socket
import time

def leer_bytes(socketfun: socket):
    raw=socketfun.recv(1024)
    return raw.decode()

def escribir_cadena(texto, socketfun:socket):
    socketfun.sendall(texto.encode())
    return

if __name__=="__main__":
    try:
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        while True:
            try:
                sock.connect(("127.0.0.1",5000))
                break
            except:
                continue
        print("Conectado a servidor.")
        while True:
            t1=leer_bytes(sock)
            if t1=="salir":
                break
            print("Recibí:", t1)
            print(">",end=" ")
            t2=input()
            escribir_cadena(t2, sock)
            if t2=="salir":
                break
        time.sleep(0.5)
        sock.close()
    except KeyboardInterrupt:
        sock.close()