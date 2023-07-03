import socket
import pickle

ip='localhost'
socketNumber=5000
BUFFER_MAX=1024

def guardarPaciente(pacienteStr, file):#Al revisar el pacientes.csv original, se tiene que la siguiente linea a escribir era una linea vacia, osea el ultimo caracter era un \n
    #Para evitar modificar el archivo innecesariamente, al final de cada escritura de paciente vamos a añadir el enter
    file.write(pacienteStr+"\n")
    return


if __name__=="__main__":
    try:
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverAddress=(ip,socketNumber)
        sock.bind(serverAddress)
        sock.listen(1)
        while True:
            conn, client_info=sock.accept()
            selectionRAW=conn.recv(1024)
            selectionDecoded=selectionRAW.decode()
            if selectionDecoded=="Ingresar":
                strRaw=conn.recv(1024)
                strWrite=strRaw.decode()
                with open("pacientes.csv", 'a') as f:
                    guardarPaciente(strWrite, f)
            elif selectionDecoded=="Descargar":
                with open("pacientes.csv", 'r') as f:
                    fileContent=f.read()
                rowAdapted=fileContent.split("\n")#Como se nos dice que nos transmitamos mas de 1024 bytes, transmitimos por filas.
                rowAdapted=rowAdapted[:-1]#La ultima fila está vacía por lo que no nos interesa transmitirla.
                for elem in rowAdapted:
                    conn.sendall(elem.encode())#Transmitimos las filas
                    msgRaw=conn.recv(1024)
                    msgDecoded=msgRaw.decode()
                    while True:
                        if msgDecoded=="Ready":
                            break
                conn.sendall("Fin1".encode())
    except KeyboardInterrupt:
        if conn!=None:
            conn.close()
        sock.close()
