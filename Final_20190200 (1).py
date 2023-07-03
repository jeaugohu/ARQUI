import time
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import csv
import requests
import copy
import math

lineas = []
copia_lineas = []
time_multi_calc = 0
time_sync_calc = 0
time_sync = 0
time_thread = 0
time_multi = 0

#Parte previa, inciso a)
def download_file():
    global lineas
    url = "https://raw.githubusercontent.com/jeaugohu/ARQUI/main/household_power_consumption.csv"
    with requests.get(url) as resp:
        with open ('household_power_consumption.csv', 'wb') as file:
            file.write(resp._content)
    with open('household_power_consumption.csv',encoding='latin1') as data:
        Datos_consumo = csv.reader(data, delimiter = ',') 
        lineas = list(Datos_consumo)
#Función que obtiene la cabecera del csv       
def get_cols():
    header = lineas[0]
    return header

#Función que cambia la columna día/mes/año por año/mes/día
def organizar_db():
    global lineas, copia_lineas
    copia_lineas = copy.deepcopy(lineas)
    j = 0
    for i in copia_lineas:
        if(j==0):
            j = 1
            continue
        sup = list(i[0].split("/"))
        new_day = sup[2]+"/"+sup[1]+"/"+sup[0]
        i[0]=new_day

#Parte previa inciso c
def get_day(day):
    global copia_lineas
    dia = []
    for i in copia_lineas:
        if(i[0] == day):
            dia.append(i)
    return dia

#Función get day pero con entrada de datos del csv porque el multiprocessing no puede acceder a variables globales
def get_day_multi(day, data):
    Finish = False
    dia = []
    for i in data:
        if(i[0] == day):
            dia.append(i)
            Finish = True
        else:
            if(Finish):
                break
    return dia

#Cáluclo de potencia global, se consideró como potencia aparente debido a que no hubo ninguna aclaración al respecto
def potencia_global(active, reactive):
    pot = math.sqrt(float(active)**2+float(reactive)**2)
    return pot

#Parte previa inciso d
def get_mean(day):
    lineas_dia = get_day(day)
    init = 0
    pot = []
    for i in lineas_dia:
        if(init == 0):
            init = 1
            continue
        try:
            pot.append(potencia_global(i[2],i[3]))  
        except:
            continue
    return sum(pot)/len(pot)
#Parte previa inciso e
def get_max(day):
    lineas_dia = get_day(day)
    max = {"potencia": 0, "hora":0}#diccionario
    for i in lineas_dia:
        try:
            pot = potencia_global(i[2],i[3]) 
        except:
            continue
        if pot > max["potencia"]:
            max['potencia'] = pot
            max['hora'] = i[1]
    return max

#Parte previa inciso f
def get_min(day):
    lineas_dia2 = get_day(day)
    min = {"potencia": potencia_global(lineas_dia2[0][2],lineas_dia2[0][3]), "hora":lineas_dia2[0][1]}
    for i in lineas_dia2:
        try:
            pot = potencia_global(i[2],i[3]) 
        except: 
            continue
        if pot < min["potencia"]:
            min['potencia'] = pot
            min['hora'] = i[1]
    return min

#Función que obtiene la suma total de potencias del día. Se consideró el valor de suma total debido a que el texto no explica nada al respecto
#de que se debe obtener con "total"
def get_total(day):
    lineas_dia3 = get_day(day)
    total = {"total": 0}
    suma = 0
    for i in lineas_dia3:
        try:
            suma = suma + potencia_global(i[2],i[3])
        except: 
            continue
    total["total"] = suma
    return total

#Función que halla qué días pertenecen a un rango
def days_in_range(day1, day2):
    final = False
    inicio = True
    dias = []
    ev_day = day1
    for i in copia_lineas:
        if(i[0]== ev_day):
            if(i[0] == day1):
                if(inicio):
                    dias.append(day1)
                inicio = False
            else:
                continue
        if((i[0]!= ev_day)):
            if(inicio):
                continue
            if(i[0]==day2):
                final = True
            dias.append(i[0])
            ev_day = copy.copy(i[0])
        if(final):
            break
    return dias

#Parte previa inciso g
def gen_day_dict(day1, day2):
    day_dict = dict()
    dias = days_in_range(day1, day2)
    for i in dias:
        day_dict[i] = get_day(i)
    return day_dict

#Final inciso a. Toma el tiempo de descarga del archivo
def get_exec_time_a():
    init = time.perf_counter()
    download_file()
    fin = time.perf_counter()
    timing = (fin-init)*(10**6) #segundos a microsegundos
    return(f"El tiempo de ejecucion para obtener el archivo es {timing} microsegundos")    

#Final inciso b. Mide el tiempo de gen_day_dict  
def get_exec_time_b():
    init = time.perf_counter()
    dict_sec = gen_day_dict('2016/12/27', '2017/4/1')           
    fin = time.perf_counter()
    timing = (fin-init)*(10**6) #segundos a microsegundos
    return timing

#Final inciso c. Se utilizan threads para obtener los datos utilizando la función get day para cada día
#Como no hay ninguna exigencia, se definió como 12 el número máximo de workers.
def gen_day_dict_threaded(day1, day2):
    dias = days_in_range(day1, day2)
    dictionary = dict()
    workers = 12
    with ThreadPoolExecutor(max_workers = workers) as executor:
        results = executor.map(get_day, dias)
    for i in results:
        dictionary[i[0][0]] = i
    return dictionary

#Final inciso d. Se utiliza multiprocessing para obtener los datos utilizando la función get day multi para cada día 
def gen_day_dict_multi(day1, day2,numproc):
    dias_data = []
    dias = days_in_range(day1, day2)
    for j in dias:
        dias_data.append([j, copia_lineas])
    dictionary = dict()
    with mp.Pool(processes=numproc) as pool:
        results = pool.starmap(get_day_multi, dias_data)
        pool.close()
        pool.join()
    for i in results:
        dictionary[i[0][0]] = i
    return dictionary

#Final inciso e. Comparación y explicación
def calc_speedup_e():
    global time_sync, time_thread, time_multi
    print("Speedup de operacion con hilos", time_sync/time_thread)
    print("Speedup de operacion con multiprocessing", time_sync/time_multi)
    print("Se puede observar que no se consigue una pequeña mejora con la solución de hilos, puesto que se crean varios hilos para una operación muy corta")
    print("Además, el multiprocessing no tiene acceso a variables globales, por lo que demora más poder acceder a la base de datos")
    print("Por otro lado, la solución con multiprocessing es la peor, debido a que debe analizar varios días y tarda mucho levantar un proceso para realizar operaciones que finalmente no exigen mucho al CPU")
    print("El speedup nos demuestra que en realidad la mejor implementación es la secuencial, puesto que es un problema que se aborda directamente y no requiere cálculos demasiado largos que exijan al CPU ni tiene problemas de I/O con esperas\n\n")

#Final inciso f. Función que calcula las estadísticas de cada día de manera secuencial.
def calc_stats(inicio, fin):
    Stats =dict()
    days = days_in_range(inicio,fin)
    for i in days:
        day_stats = dict()
        mean = get_mean(i)
        maxi = get_max(i)
        mini = get_min(i)
        totali = get_total(i)
        day_stats = {"Max":maxi['potencia'], "Min": mini['potencia'], "Prom": mean, "Total": totali["total"] }
        Stats[i] = day_stats
    return Stats    

#Final inciso g
#Función que utiliza multiprocessing para que cada proceso se centre en un cálculo.
def calc_stats_conc(inicio, fin):
    Stats =dict()
    days = days_in_range(inicio,fin)
    days_op = [["max", days,copia_lineas],["min",days,copia_lineas], ["prom",days,copia_lineas],["total", days, copia_lineas] ]
    with mp.Pool(processes=4) as pool:
        results = pool.starmap(four_stats, days_op)
        pool.close()
        pool.join()
    j=0
    for i in days:
        Stats[i] = {"Max":results[0][j], "Min": results[1][j], "Prom": results[2][j], "Total": results[3][j]}
        j = j+1
    return Stats     

#Función que calcula una estadística específica de una serie de días, también tiene como entrada la data del csv
#Por utilizarse con multiprocessing no puede acceder a variables globales
def four_stats(op, day, data):
    info =[]
    for i in day:
        if(op == "prom"):
            rpta = get_mean_multi(i,data)
        elif(op == "max"):
            rpta = get_max_multi(i,data)
        elif(op == "min"):
            rpta = get_min_multi(i,data)
        else:
            rpta = get_total_multi(i,data)
        info.append(rpta)
    return info

#Función que calcula la media de potencia global de un día
#Data como entrada por utilizarse para multiprocessing   
def get_mean_multi(day,lin):
    lineas_dia = get_day_multi(day,lin)
    init = 0
    pot = []
    for i in lineas_dia:
        if(init == 0):
            init = 1
            continue
        try:
            pot.append(potencia_global(i[2],i[3]))  
        except:
            continue
    return sum(pot)/len(pot)

#Función que calcula el max. de potencia global de un día
#Data como entrada por utilizarse para multiprocessing 
def get_max_multi(day,lin):
    lineas_dia = get_day_multi(day,lin)
    max = {"potencia": 0, "hora":0}
    for i in lineas_dia:
        try:
            pot = potencia_global(i[2],i[3]) 
        except:
            continue
        if pot > max["potencia"]:
            max['potencia'] = pot
            max['hora'] = i[1]
    return max['potencia']

#Función que calcula el min de potencia global de un día
#Data como entrada por utilizarse para multiprocessing 
def get_min_multi(day,lin):
    lineas_dia2 = get_day_multi(day,lin)
    min = {"potencia": potencia_global(lineas_dia2[0][2],lineas_dia2[0][3]), "hora":lineas_dia2[0][1]}
    for i in lineas_dia2:
        try:
            pot = potencia_global(i[2],i[3]) 
        except: 
            continue
        if pot < min["potencia"]:
            min['potencia'] = pot
            min['hora'] = i[1]
    return min['potencia']

#Función que calcula el total de potencia global de un día
#Data como entrada por utilizarse para multiprocessing 
def get_total_multi(day,lin):
    lineas_dia3 = get_day_multi(day,lin)
    total = {"total": 0}
    suma = 0
    for i in lineas_dia3:
        try:
            suma = suma + potencia_global(i[2],i[3])
        except: 
            continue
    total["total"] = suma
    return total["total"]

#Final inciso h
def calc_speedup_h():
    global time_sync_calc, time_multi_calc
    print("Speedup de operacion con multiprocessing", time_sync_calc/time_multi_calc)
    print("Para alcanzar una mejora, opté por utilizar multiprocessing ya que nos pedían 4 cálculos (max, min, prom, total) y se podía dividir en 4 procesos")
    print("Se puede observar que esta división permite obtener un mejor speed up al separar las operaciones secuenciales del CPU en 4 procesos")
    print("Esto solo se consigue con un intervalo grande, puesto que con intervalos pequeños, no vale la pena levantar los 4 procesos extra")
    print("Las limitaciones de la mejora son claras:")
    print("  - Si se dividen los cálculos en más procesos, estos nuevos procesos tendrán una menor carga que ejecutar y se tardará más en levantarlos")
    print("  - Si se utilizan intervalos pequeños, no conviene levantar procesos pues se ejecutan pocas instrucciones")
    print("  - Si se utilizan intervalos grandes, como este caso, el tiempo de ejecución secuencial aumenta, pero también el tiempo de ejecución en paralelo")
    print("Por estas razones no se puede alcanzar una mejora indefinida del desempeño del sistema (Se cumple la ley de Amdahl)")

if __name__ == '__main__':
    
    #Examen, inciso a) 
    print(get_exec_time_a())
    #Parte previa, inciso b)
    encabezado = get_cols()
    #Se cambia el orden de la fecha para que coincida con los que nos solicitan. De día/mes/año a año/mes/día
    organizar_db()
    
    time_sync = get_exec_time_b()
    print("El tiempo de ejecucion de gen_day_dict es ", time_sync, " microsegundos")
    
    #Con threads:
    init = time.perf_counter()
    dict_thread = gen_day_dict_threaded('2016/12/27', '2017/4/1')         
    fin = time.perf_counter()
    time_thread = (fin-init)*(10**6)
    print("El tiempo de ejecucion de gen_day_dict_threaded ", time_thread , " microsegundos")
   
    #Con multiprocessing:
    init = time.perf_counter()
    dict_multi = gen_day_dict_multi('2016/12/27', '2017/4/1', 12)
    fin = time.perf_counter()
    time_multi = (fin-init)*(10**6)
    print("El tiempo de ejecucion de gen_day_dict_multi ", time_multi , " microsegundos\n")  
    
    calc_speedup_e()
   
    #Estadísticas en un intervalo
    init = time.perf_counter()
    Stats = calc_stats('2016/12/27', '2017/4/15')
    fin = time.perf_counter()
    time_sync_calc = (fin-init)*(10**6)
    print("El tiempo de ejecucion de calc_stats ", time_sync_calc , " microsegundos\n")
    
    #Estadísticas en un intervalo analizado de manera concurrente
    init = time.perf_counter()
    Stats_multi = calc_stats_conc('2016/12/27', '2017/4/15')
    fin = time.perf_counter()
    time_multi_calc = (fin-init)*(10**6)
    print("El tiempo de ejecucion de calc_stats_conc ", time_multi_calc , " microsegundos\n")
    
    print("Se escogió multiprocessing y no threading debido a que el problema exige cálculos utilizando el CPU y no eventos de I/O ni tiempos muertos que aprovechar")
    
    calc_speedup_h()