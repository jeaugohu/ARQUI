import socket

NOMBRE_ARCHIVO="oferta_del_sniper.txt"

if __name__=="__main__":
    try:
        server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_address=("localhost",5000)
        server_socket.bind(server_address)
        server_socket.listen(1)
        client_conn,client_info=server_socket.accept()
        data=client_conn.recv(1024)
        with open(NOMBRE_ARCHIVO, "w") as f:
            f.write(data.decode())
        client_conn.close()
        server_socket.close()
    except KeyboardInterrupt:
        if client_conn!=None:
            client_conn.close()
        server_socket.close()