import socket

ip='localhost'
socketNumber=5000

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
            strRaw=conn.recv(1024)
            strWrite=strRaw.decode()
            with open("pacientes.csv", 'a') as f:
                guardarPaciente(strWrite, f)
    except KeyboardInterrupt:
        if conn!=None:
            conn.close()
        sock.close()
