import asyncio
import websockets
import random
from time import sleep
from paquete import packaging
from simulacion_errores import error_sim

# Visualización del paquete
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
                print(f"Enviando paquete {i+1}...")
                while True:
                    error_paq = error_sim(paq)
                    print(error_paq)

                    # Simulación de pérdida de paquete
                    # Probabilidad del 80% de enviar el paquete
                    if(random.uniform(0, 1) <= 0.8): await websocket.send(error_paq)

                    try:
                        client_message = await asyncio.wait_for(websocket.recv(), timeout=3.0)  # espera máximo 5 segundos
                        print("Mensaje recibido:", client_message)
                        if (len(client_message) != 8):
                            print(f"Reenviando paquete {i+1} por comprobación corrupta")
                            continue
                        if(random.uniform(0, 1) <= 0.8):
                            if "00000000" == client_message:
                                # Paquete recibido correctamente (ACK)
                                break
                            else:
                                # Paquete recibido incorrectamente (NAK)
                                print(f"Reenviando paquete {i+1} por NAK")
                        else:
                            # Simulación de paquete de confirmación perdido
                            print(f"Reenviando paquete {i+1} por PÉRDIDA de notificación")
                    except asyncio.TimeoutError:
                        # Paquete de confirmación con recepción tardía o perdido
                        print(f"Reenviando paquete {i+1} por recepción TARDÍA o pérdida de notificación")
            
    except websockets.exceptions.ConnectionClosedOK:
        print("Cliente desconectado.")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("Servidor escuchando en puerto 8765...")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
