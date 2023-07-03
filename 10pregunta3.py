import time
import asyncio
import random

PRECIO_MINIMO = 20000   #El precio base al que se inicia la subasta
PRECIO_MAXIMO = 100000  #El precio maximo que cualquiera de los participantes está dispuesto a pagar(úselo como tope en random.randint()
TIEMPO_LIMITE=60
NOMBRE_ARCHIVO="oferta_del_sniper.txt"

async def participante(id: int, arr,tiempo_inicio):
	while((time.time()-tiempo_inicio)<TIEMPO_LIMITE):
		if(arr.index(max(arr))!=id):
			await asyncio.sleep(random.uniform(0,10))
			if(random.randint(0,1)==1):
				if((time.time()-tiempo_inicio)<TIEMPO_LIMITE):
					arr[id]=int(random.uniform(max(arr)+500,(max(arr)+500)*1.2))
					print(f"El participante {id+1} hizo una reoferta de {arr[id]}")
		else:
			await asyncio.sleep(random.uniform(0,10))

async def sniper(arr):
	await asyncio.sleep(57)
	with open(NOMBRE_ARCHIVO, "r") as f:
		lectura=f.read()
	ofertaSniper=int(lectura)
	arr.append(ofertaSniper)
	print(f"Participante sniper hizo reoferta de {arr[5]}")

async def main():
	arr=[PRECIO_MINIMO,PRECIO_MINIMO,PRECIO_MINIMO,PRECIO_MINIMO,PRECIO_MINIMO]
	inicioSubasta=time.time()
	await asyncio.gather(participante(0,arr,inicioSubasta),participante(1,arr,inicioSubasta),participante(2,arr,inicioSubasta),participante(3,arr,inicioSubasta),participante(4,arr,inicioSubasta),sniper(arr))
	print("Se cumplió el tiempo de 60 segundos")
	winnerPrice=max(arr)
	winnerIdx=arr.index(winnerPrice)
	print("Ofertas finales:")
	print(arr)
	if(winnerIdx!=5):
		print(f"El ganador es el participante numero {winnerIdx+1}")
	else:
		print(f"El ganador es el sniper")


if __name__ == "__main__":
	asyncio.run(main())