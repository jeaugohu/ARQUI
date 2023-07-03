import time
import asyncio
import random

PRECIO_MINIMO = 20000   #El precio base al que se inicia la subasta
PRECIO_MAXIMO = 100000  #El precio maximo que cualquiera de los participantes está dispuesto a pagar(úselo como tope en random.randint()

async def participante(id, arr):
	await asyncio.sleep(random.uniform(0,10))
	arr[id]=random.randint(PRECIO_MINIMO,PRECIO_MAXIMO)
	return

async def main():
	arr=[0,0,0,0,0]
	await asyncio.gather(participante(0,arr),participante(1,arr),participante(2,arr),participante(3,arr),participante(4,arr))
	winnerPrice=max(arr)
	winnerIdx=arr.index(winnerPrice)
	print("Ofertas finales:")
	print(arr)
	print(f"El ganador es el participante numero {winnerIdx+1}")


if __name__ == "__main__":
	asyncio.run(main())