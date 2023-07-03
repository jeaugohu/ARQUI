
import socket
import time

if __name__=="__main__":
    try: 
        while True:
            sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            try:
                sock.connect(("127.0.0.1", 5000))
                sock.close()
                print("\x1b[32m[*] El servidor está operativo\x1b[0m")
            except:
                print("\x1b[31m[-] El servidor no responde\x1b[0m")
            time.sleep(5)
    except KeyboardInterrupt:
            sock.close()
