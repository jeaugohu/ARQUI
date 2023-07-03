import time
import asyncio
import random

PRECIO_BASE_BLOQUE1=15
PRECIO_BASE_BLOQUE2=15
PRECIO_BASE_BLOQUE3=15
TIEMPO_RONDA=30

async def participante(id, bloque1,bloque2,bloque3, tiempo_inicio):
    nombre=""
    if(id==0):
        nombre="Telefonica"
    elif (id==1):
        nombre="Claro"
    elif (id==2):
        nombre="Entel"
    while((time.time()-tiempo_inicio)<TIEMPO_RONDA):
        if(bloque1.index(max(bloque1))!=id):
            await asyncio.sleep(random.uniform(0,10))
            nueva_oferta=random.randint(max(bloque1)+1,max(bloque1)+20)
            if(random.randint(0,1)==1):
                bloque1[id]=nueva_oferta
                azar=random.randint(0,3)
                if(azar==0 and nueva_oferta>max(bloque2)):
                    bloque2[id]=nueva_oferta
                    print(f"Participante {nombre} hizo oferta de {nueva_oferta} para el bloque 0 y 1")
                elif(azar==1 and nueva_oferta>max(bloque3)):
                    bloque3[id]=nueva_oferta
                    print(f"Participante {nombre} hizo oferta de {nueva_oferta} para el bloque 0 y 2")
                elif(azar==2 and nueva_oferta>max(bloque2) and nueva_oferta>max(bloque3)):
                    bloque2[id]=nueva_oferta
                    bloque3[id]=nueva_oferta
                    print(f"Participante {nombre} hizo oferta de {nueva_oferta} para el bloque 0, 1 y 2")
                else:
                    print(f"Participante {nombre} hizo oferta de {nueva_oferta} para el bloque 0")
        elif(bloque2.index(max(bloque2))!=id):
            await asyncio.sleep(random.uniform(0,10))
            nueva_oferta=random.randint(max(bloque2)+1,max(bloque2)+20)
            if(random.randint(0,1)==1):
                bloque2[id]=nueva_oferta
                azar=random.randint(0,3)
                if(azar==0 and nueva_oferta>max(bloque1)):
                    bloque1[id]=nueva_oferta
                    print(f"Participante {nombre} hizo oferta de {nueva_oferta} para el bloque 0 y 1")
                elif(azar==1 and nueva_oferta>max(bloque3)):
                    bloque3[id]=nueva_oferta
                    print(f"Participante {nombre} hizo oferta de {nueva_oferta} para el bloque 1 y 2")
                elif(azar==2 and nueva_oferta>max(bloque1) and nueva_oferta>max(bloque3)):
                    bloque1[id]=nueva_oferta
                    bloque3[id]=nueva_oferta
                    print(f"Participante {nombre} hizo oferta de {nueva_oferta} para el bloque 0, 1 y 2")
                else:
                    print(f"Participante {nombre} hizo oferta de {nueva_oferta} para el bloque 1")
        elif(bloque3.index(max(bloque3))!=id):
            await asyncio.sleep(random.uniform(0,10))
            nueva_oferta=random.randint(max(bloque3)+1,max(bloque3)+20)
            if(random.randint(0,1)==1):
                bloque3[id]=nueva_oferta
                azar=random.randint(0,3)
                if(azar==0 and nueva_oferta>max(bloque1)):
                    bloque1[id]=nueva_oferta
                    print(f"Participante {nombre} hizo oferta de {nueva_oferta} para el bloque 0 y 2")
                elif(azar==1 and nueva_oferta>max(bloque2)):
                    bloque2[id]=nueva_oferta
                    print(f"Participante {nombre} hizo oferta de {nueva_oferta} para el bloque 1 y 2")
                elif(azar==2 and nueva_oferta>max(bloque1) and nueva_oferta>max(bloque2)):
                    bloque1[id]=nueva_oferta
                    bloque2[id]=nueva_oferta
                    print(f"Participante {nombre} hizo oferta de {nueva_oferta} para el bloque 0, 1 y 2")
                else:
                    print(f"Participante {nombre} hizo oferta de {nueva_oferta} para el bloque 2")
        else:
            await asyncio.sleep(random.uniform(0,10))
    

async def main():
    print("Bloques a subastar")
    print("Bloque 0: 50 MHz")
    print("Bloque 1: 60 MHz")
    print("Bloque 2: 70 MHz")
    print("Precio base de cada bloque: $ 15 millones")
    bloque1=[15,15,15]
    bloque2=[15,15,15]
    bloque3=[15,15,15]
    print("Ronda 1:")
    print("Precios actuales")
    print(f"Bloque 0: ${max(bloque1)} millones")
    print(f"Bloque 1: ${max(bloque2)} millones")
    print(f"Bloque 2: ${max(bloque3)} millones")
    tINICIO=time.time()
    await asyncio.gather(participante(0,bloque1,bloque2,bloque3,tINICIO),participante(1,bloque1,bloque2,bloque3,tINICIO),participante(2,bloque1,bloque2,bloque3,tINICIO))
    print("Se cumplio el tiempo de 30 segundos. Ronda 1 finaliza")
    print("Ronda 2:")
    print("Precios actuales")
    print(f"Bloque 0: ${max(bloque1)} millones")
    print(f"Bloque 1: ${max(bloque2)} millones")
    print(f"Bloque 2: ${max(bloque3)} millones")
    tINICIO=time.time()
    await asyncio.gather(participante(0,bloque1,bloque2,bloque3,tINICIO),participante(1,bloque1,bloque2,bloque3,tINICIO),participante(2,bloque1,bloque2,bloque3,tINICIO))
    print("Se cumplio el tiempo de 30 segundos. Ronda 2 finaliza")
    print("Ronda 3:")
    print("Precios actuales")
    print(f"Bloque 0: ${max(bloque1)} millones")
    print(f"Bloque 1: ${max(bloque2)} millones")
    print(f"Bloque 2: ${max(bloque3)} millones")
    tINICIO=time.time()
    await asyncio.gather(participante(0,bloque1,bloque2,bloque3,tINICIO),participante(1,bloque1,bloque2,bloque3,tINICIO),participante(2,bloque1,bloque2,bloque3,tINICIO))
    print("Se cumplio el tiempo de 30 segundos. Ronda 3 finaliza")
    print("Los ganadores son:")
    nombres=["Telefonica","Claro", "Entel"]
    print(f"Bloque 0:{nombres[bloque1.index(max(bloque1))]} con ${max(bloque1)} millones")
    print(f"Bloque 1:{nombres[bloque2.index(max(bloque2))]} con ${max(bloque2)} millones")
    print(f"Bloque 2:{nombres[bloque3.index(max(bloque3))]} con ${max(bloque3)} millones")

if __name__=="__main__":
    asyncio.run(main())