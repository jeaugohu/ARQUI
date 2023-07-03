
import socket
import pickle
import time

def generarMatrices():
	return [[[1,2],[3,4]],[[1,2],[3,4]]]

if __name__=="__main__":
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                print("Esperando al servidor ... ")
                sock.connect(("127.0.0.1",5000))
                break
            except:
                time.sleep(0.5)
                continue
        a=generarMatrices()
        sock.sendall(pickle.dumps(a))
        matriz_rawbytes=sock.recv(1024)
        matriz_respuesta=pickle.loads(matriz_rawbytes)
        print("Producto de las matrices:")
        print(matriz_respuesta)
        sock.close()
    except KeyboardInterrupt:
        sock.close()