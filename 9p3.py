import time
import matplotlib.pyplot as plt
import statistics

#Comentarios de los resultados. Se observa que a medida que aumentan la cantidad de lineas a ordenar, el tiempo de escritura y lectura no varían tanto como el tiempo que usa el programa
#para ordenar. El cual crece muchísimo más que estas las otras dos operaciones. La forma de crecimiento del tiempo para ordenar parece seguir una funcion cuadrática respecto a la cantidad de filas a ordenar
#Mientras que los de lectura y escritura paracen casi completamente horizontales por lo poco que varían respecto a la cantidad de filas a ordenar.
def SortElement(arr):#Indice de la edad es el 4
    i=0
    while i<len(arr):
        j=i+1
        while j<len(arr):
            intI=int(arr[i][4])
            intJ=int(arr[j][4])
            if(intI>intJ):
                aux=arr[j]
                arr[j]=arr[i]
                arr[i]=aux
            j=j+1
        i=i+1
    return


def ordenarArchivo(N: int):
    tlecturaInicio=time.perf_counter()
    with open("pacientes.csv", "r") as file:
        contents=file.read()
    tlecturaFin=time.perf_counter()
    tOrdenarInicio=time.perf_counter()
    rowSeparated=contents.split("\n")
    arrVer1=[]
    for fila in rowSeparated[1:N+1]:#Empezamos en 1 para no contar la fila de encabezado
        elementos=fila.split(",")
        arrVer1.append(elementos)
    SortElement(arrVer1)
    DataOrdenada=rowSeparated[0]+"\n"
    arrVer2=[]
    separator=","
    for elem in arrVer1:
        arrVer2.append(separator.join(elem))
    separator="\n"
    DataOrdenada=DataOrdenada+separator.join(arrVer2)
    tOrdenarFin=time.perf_counter()
    tEscribirInicio=time.perf_counter()
    with open("pacientes_ordenado.csv","w") as file:
        file.write(DataOrdenada)
    tEscribirFin=time.perf_counter()
    return (tlecturaFin-tlecturaInicio)*1e3,(tEscribirFin-tEscribirInicio)*1e3,(tOrdenarFin-tOrdenarInicio)*1e3

if __name__=="__main__":
    tiempos_lectura=[]
    tiempos_escritura=[]
    tiempos_ordenar=[]
    iter=5
    tL=[]
    tE=[]
    tO=[]
    Nmax=5001
    for N in range(500,Nmax,500):
        for i in range(iter):
            tLec,tEs,tOr=ordenarArchivo(N)
            tL.append(tLec)
            tO.append(tOr)
            tE.append(tEs)
        tiempos_escritura.append(statistics.median(tE))
        tiempos_lectura.append(statistics.median(tL))
        tiempos_ordenar.append(statistics.median(tO))
        tE.clear()
        tL.clear()
        tO.clear()
    plt.plot([i for i in range(500,Nmax,500)],tiempos_lectura)
    plt.plot([i for i in range(500,Nmax,500)],tiempos_escritura)
    plt.plot([i for i in range(500,Nmax,500)],tiempos_ordenar)
    plt.xlabel("# de líneas")
    plt.ylabel("Tiempo [ms]")
    plt.legend(["Leer", "Escribir", "Ordenar"])
    plt.savefig('tiempos.png')#
