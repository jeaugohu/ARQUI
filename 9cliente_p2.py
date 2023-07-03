import socket
import time
import matplotlib.pyplot as plt
import statistics

ip='localhost'
socketNumber=5000
BUFFER_MAX=1024
#Comentarios del histograma: Se observa que el histograma tiene una forma parecida a una U, en el sentido de que los valores más frecuentes son los que se encuentran a los extremos
#de la gráfica. Y al repetir esta operación varias veces la velocidad de descarga promedio parece fluctuar mucho.

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

def ImprimirMenu():
    print("¿Qué desea hacer?")
    print("1: Ingresar paciente")
    print("2: Descargar pacientes")
    return

if __name__=="__main__":
        try:
            sock_client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            serverAddress=(ip,socketNumber)
            sock_client.connect(serverAddress)
            ImprimirMenu()
            select=" "
            while select==" ":
                select=input()
                if select=="1":
                    patientStr=registrarPaciente()
                    sock_client.sendall("Ingresar".encode())
                    time.sleep(0.1)#Un pequeño delay para que el servidor pueda procesar
                    sock_client.sendall(patientStr.encode())
                    sock_client.close()
                    break
                elif select=="2":
                    sock_client.sendall("Descargar".encode())
                    DataTotal=""#Consideraremos que recibiremos por filas
                    velocidades=[]
                    while True:
                        t1=time.perf_counter()
                        dataRAW=sock_client.recv(BUFFER_MAX)
                        t2=time.perf_counter()
                        dataSize=len(dataRAW)
                        dataSizeMB=dataSize/(1e6)
                        dataDecoded=dataRAW.decode()
                        if dataDecoded=="Fin1":
                            break
                        DataTotal=DataTotal+dataDecoded+"\n"
                        velocidades.append(dataSizeMB/((t2-t1)))
                        sock_client.sendall("Ready".encode())
                    with open("descarga.csv", "w") as f:
                        f.write(DataTotal)
                    print("Velocidad de descarga:", end=" ")
                    print(statistics.mean(velocidades),end=" ")
                    print("MB/s")
                    plt.hist(velocidades)
                    plt.ylabel('Velocidad de descarga [Mb/s]')
                    plt.savefig('histogram.png')
                    break
                select=" "
            sock_client.close()
        except:
             sock_client.close()