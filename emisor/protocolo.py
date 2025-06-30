import asyncio
import websockets
import random
from time import sleep
from paquete import packaging
from simulacion_errores import error_sim

def ver_paquete(paquete):
    seq = paquete[0]

    bin_data = paquete[1:-40]
    data_text = ""

    cant_paq = int(paquete[-40:-32],2)

    cant_data = int(paquete[-32:-24],2)

    crc = paquete[-24:-8]

    for i in range(0,cant_data):
        data_text += chr(int(bin_data[(8*i)+1: (8*i) + 9],2))

    print(seq, data_text, cant_paq, cant_data, crc)

async def handler(websocket):
    print("Cliente conectado.")
    try:
        while True:
            # Espera mensaje del cliente
            client_message = await websocket.recv()
            print(f"Cliente: {client_message}")

            texto = client_message
            clave = "rombo"
            print("Empaquetando...")
            sleep(1)
            original_paq = packaging(texto,clave)
            print(original_paq)
            
            seq = False

            for i, paq in enumerate(original_paq):
                while True:
                    print("Simulando errores...")
                    error_paq = error_sim(paq)
                    print(f"Enviando paquete {i+1}...")
                    print(error_paq)
                    if(random.uniform(0, 1) <= 0.   ): await websocket.send(error_paq)
                    try:
                        client_message = await asyncio.wait_for(websocket.recv(), timeout=3.0)  # espera máximo 5 segundos
                        print("Mensaje recibido:", client_message)
                        if(random.uniform(0, 1) <= 0.8):
                            if int(client_message) == seq: 
                                seq = not seq
                                break
                            else:
                                print(f"Reenviando paquete {i+1}")
                        else:
                            print(f"Reenviando paquete {i+1} DUPLICADO")
                    except asyncio.TimeoutError:
                        print("No se recibió ningún mensaje en 3 segundos.")
            

    except websockets.exceptions.ConnectionClosedOK:
        print("Cliente desconectado.")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("Servidor escuchando en puerto 8765...")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
