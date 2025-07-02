import asyncio
import websockets
import random
from time import sleep
from paquete import packaging
from cifrado import cypher_decypher
from simulacion_errores import error_sim

PROB_NO_PERDIDA_PAQUETE = 1
PROB_NO_PERDIDA_NOTIFICACION = 1

texto = "Muchos años después, frente al pelotón de fusilamiento, el coronel Aureliano Buendía había de recordar aquella tarde remota en que su padre lo llevó a conocer el hielo. Macondo era entonces una aldea de veinte casas de barro y cañabrava, construidas a la orilla de un río transparente."
clave = "gato"

def traducir(datos_cifrados):
    data_text = ""
    for i in range (0, len(datos_cifrados) // 8):
        data_text += chr(int(datos_cifrados[(8*i): (8*i) + 8],2))

    return data_text

# Visualización del paquete
def ver_paquete(paquete):
    seq = paquete[0]
    bin_data = paquete[1:-40]
    cant_data_bin = paquete[-40:-32]
    cant_paq_bin = paquete[-32:-24]
    crc = paquete[-24:-8]
    termino_paquete = paquete[-8:]
    cant_data = int(cant_data_bin, 2)

    data_list = []
    for i in range(cant_data):
        dato_bin = bin_data[(8 * i):(8 * (i + 1))]
        data_list.append(dato_bin)

    headers = ["Sec", *[f"D{i+1}" for i in range(cant_data)], "CantPaq", "CantData", "CRC16", "Term"]
    row = [seq, *data_list, cant_paq_bin, cant_data_bin, crc, termino_paquete]

    col_widths = [max(len(h), len(r)) for h, r in zip(headers, row)]

    # Construir líneas compactas
    header_line = "|" + "|".join(h.ljust(w) for h, w in zip(headers, col_widths)) + "|"
    separator_line = "|" + "|".join("-" * w for w in col_widths) + "|"
    row_line = "|" + "|".join(r.ljust(w) for r, w in zip(row, col_widths)) + "|"

    print(cypher_decypher(traducir(bin_data),clave))
    print(header_line)
    print(separator_line)
    print(row_line)

    
def calcular_paridad_impar(bitstring):
    count_ones = sum(int(bit) for bit in bitstring)
    return 0 if count_ones % 2 == 1 else 1

async def handler(websocket):
    print("Cliente conectado.")
    try:
        while True:
            # Espera mensaje del cliente
   
            print("Empaquetando...")
            sleep(1)
            original_paq = packaging(texto,clave)
            
            seq = False

            for i, paq in enumerate(original_paq):
                print(f"Enviando paquete {i+1} con mensaje: ", end="")
                while True:
                    error_paq = error_sim(paq)
                    ver_paquete(error_paq)

                    # Simulación de pérdida de paquete
                    # Probabilidad del 80% de enviar el paquete
                    if(random.uniform(0, 1) <= PROB_NO_PERDIDA_PAQUETE): 
                        await websocket.send(error_paq)

                    try:
                        client_message = await asyncio.wait_for(websocket.recv(), timeout=1.0)  # espera máximo 5 segundos
                        print("Notificación recibida:", client_message)
                        if (len(client_message) != 5):
                            print(f"Reenviando paquete {i+1} por \033[31mcomprobación corrupta\033[0m")
                            continue
                        bit_paridad = client_message[4]
                        seq_cliente = client_message[3]
                        info_errores = client_message[0:3]
                        print(info_errores)
                        if info_errores == "001":
                                print("Notificación de \033[31mrechazo por fallo CRC.\033[0m Reenviando...")
                        elif info_errores == "010":
                                print("Notificación de \033[31mrechazo por superar el máximo de paquetes.\033[0m Reenviando...")
                        elif info_errores == "011":
                                print("Notificación de \033[31mrechazo por incongruencia en la cantidad de datos. \033[0m Reenviando...")
                        elif info_errores == "100":
                                print("Notificación de \033[31mrechazo por paquete duplicado.\033[0m Reenviando...")
                        elif info_errores == "101":
                                print("Notificación de \033[31mrechazo por tamaño de paquete menor al mínimo.\033[0m Reenviando...")
                                break
                        elif info_errores == "000":
                            if(random.uniform(0, 1) <= PROB_NO_PERDIDA_NOTIFICACION):
                                if seq_cliente == str(int(seq)):
                                    # Paquete recibido correctamente (ACK)
                                    seq = not seq
                                    break
                                else:   
                                    # Paquete recibido incorrectamente (NAK)
                                    print(f"Reenviando paquete {i+1} por \033[31mpaquete DUPLICADO\033[0m")
                            else:
                                # Simulación de paquete de confirmación perdido
                                print(f"Reenviando paquete {i+1} por \033[31notificación NO RECIBIDA\033[0m")
                    except asyncio.TimeoutError:
                        # Paquete de confirmación con recepción tardía o perdido
                        print(f"Reenviando paquete {i+1} por recepción \033[31mTARDÍA o pérdida de notificación\033[0m")
                print(f"\033[32mACK recibido\033[0m")
            
    except websockets.exceptions.ConnectionClosedOK:
        print("Cliente desconectado.")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("Servidor escuchando en puerto 8765...")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
