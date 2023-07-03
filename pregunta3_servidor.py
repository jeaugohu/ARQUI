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
        sock.bind(("127.0.0.1",5000))
        sock.listen(1)
        print("Server started and listening on port 5000")
        client_socket,client_address=sock.accept()
        print("Conectado a cliente:", client_address)
        while True:
            print(">",end=" ")
            t2=input()
            escribir_cadena(t2, client_socket)
            if t2=="salir":
                break
            t1=leer_bytes(client_socket)
            if t1=="salir":
                break
            print("Recibí:", t1)
        time.sleep(0.5)
        client_socket.close()
        sock.close()
    except KeyboardInterrupt:
        print("Cerrando servidor ...")
        client_socket.close()
        sock.close()
    