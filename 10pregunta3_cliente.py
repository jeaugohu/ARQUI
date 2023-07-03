import socket
import sys


if __name__=="__main__":
    try:
        client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_address=("localhost",5000)
        client_socket.connect(server_address)
        NumStr=sys.argv[1]
        client_socket.sendall(NumStr.encode())
        client_socket.close()
    except:
        client_socket.close()