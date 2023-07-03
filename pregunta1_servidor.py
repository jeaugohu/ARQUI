import socket

if __name__=="__main__":
        try:
            sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.bind(("127.0.0.1", 5000))
            sock.listen(1)
            print("Esperando conexiones ...")
            while True:
                client_socket, client_address=sock.accept()
                print("Conexión entrante de",client_address)
                client_socket.close()
        except KeyboardInterrupt:
            print("Cerrando el servidor ... ")
            client_socket.close()
            sock.close()