
import socket
import pickle

def calcularProducto(arr):
    listaA=[]
    listaB=[]
    listaA.append(arr[0][0][0]*arr[1][0][0]+arr[0][0][1]*arr[1][1][0])
    listaA.append(arr[0][0][0]*arr[1][0][1]+arr[0][0][1]*arr[1][1][1])
    listaB.append(arr[0][1][0]*arr[1][0][0]+arr[0][1][1]*arr[1][1][0])
    listaB.append(arr[0][1][0]*arr[1][0][1]+arr[0][1][1]*arr[1][1][1])
    res=[listaA,listaB]
    return res

if __name__=="__main__":
    try:
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind(("127.0.0.1",5000))
        sock.listen(1)
        print("Esperando conexiones ...")
        while True:
            client_socket,client_address=sock.accept()
            print("Conexion entrante de", client_address)
            data_raw=client_socket.recv(1024)
            lista=pickle.loads(data_raw)
            resultado=calcularProducto(lista)
            client_socket.sendall(pickle.dumps(resultado))
            client_socket.close()
    except KeyboardInterrupt:
        print("Cerrando servidor ...")
        client_socket.close()
        sock.close()
        