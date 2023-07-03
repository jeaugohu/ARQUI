import socket

ip='localhost'
socketNumber=5000

def registrarPaciente():
    print("Ingrese datos del paciente")
    print("Nombre(s):", end=" ")
    nombre=input()
    print("Apellidos:", end=" ")
    apellidos=input()
    print("Peso (kg):", end=" ")
    peso=input()#No hay necesidad de convertir a int puesto que lo transladaremos a la base de datos.
    print("Talla (cm):", end=" ")
    talla=input()
    print("Edad:", end=" ")
    edad=input()
    print("¿Cuenta con seguro? (s/n):", end=" ")
    seguro=input()
    if seguro=="s":
        seguro="True"
    elif seguro=="n":
        seguro="False"
    strFinal=nombre+","+apellidos+","+peso+","+talla+","+edad+","+seguro
    print("Enviando al servidor...")
    return strFinal


if __name__=="__main__":
        try:
            sock_client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            serverAddress=(ip,socketNumber)
            sock_client.connect(serverAddress)
            patientStr=registrarPaciente()
            sock_client.sendall(patientStr.encode())
            sock_client.close()
        except:
             sock_client.close()