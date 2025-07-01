import websockets
from cifrado import cypher_decypher as cy
from funciones import data_dump, calc_crc

CLAVE = "rombo"
lista = []

def verificar_crc16(datos_crc,crc):
    return crc == calc_crc(datos_crc)

def verificar_cant_paq(cant_paq):
    return int(len(lista)) < cant_paq

def verificar_cant_data(cant_data, bin_data):
    return cant_data == int(len(bin_data)/8) 

def verificar_prev_seq(prev_seq,seq):
    return prev_seq != seq

def traducir(datos_cifrados):
    data_text = ""
    for i in range (0, len(datos_cifrados) // 8):
        data_text += chr(int(datos_cifrados[(8*i): (8*i) + 8],2))

    return data_text

def calcular_paridad_impar(bitstring):
    count_ones = sum(int(bit) for bit in bitstring)
    return 0 if count_ones % 2 == 1 else 1

def generar_confirmacion(error, prev_seq):
    confirmacion = error+str(prev_seq)
    bit_paridad = calcular_paridad_impar(confirmacion)
    return confirmacion + bit_paridad

async def chat():
    global lista 

    uri = "ws://25.53.150.13:8765"
    async with websockets.connect(uri) as websocket:
        print("Conectado al servidor.")
        try:
            cant_paq = 1
            prev_seq = True
            while len(lista) < cant_paq:
                # Espera el paquete enviado por el emisor
                server_message = await websocket.recv()

                print(server_message)
                if (len(server_message) >= 49):
                    seq, bin_data, cant_paq, cant_data, crc = data_dump(server_message)

                    mensaje = traducir(bin_data)
                    mensaje = cy(mensaje, CLAVE)
                    print ("Mensaje recibido: ", mensaje)

                    # Verificación de errores
                    if (not verificar_crc16(server_message[:-24], crc)):
                        await websocket.send(generar_confirmacion("001", prev_seq))
                        print("Mensaje ", mensaje ," rechazado por fallo CRC.")
                        continue
                    if (not verificar_cant_paq(cant_paq)):
                        await websocket.send(generar_confirmacion("010", prev_seq))
                        print("Mensaje ", mensaje ," rechazado por superar el máximo de paquetes.")
                        continue
                    if (not verificar_cant_data(cant_data, bin_data)):
                        await websocket.send(generar_confirmacion("011", prev_seq))
                        print("Mensaje ", mensaje ," rechazado por incongruencia en la cantidad de datos. ")
                        continue
                    if (not verificar_prev_seq(prev_seq,seq)):
                        await websocket.send(generar_confirmacion("100", prev_seq))
                        continue

                    lista.append(mensaje)
                    await websocket.send(generar_confirmacion("000", seq))
                        
                    print(f"Mensaje: {mensaje}")
                else:
                    await websocket.send(generar_confirmacion("101", prev_seq))
                        
            print("largo lista : ", len(lista))
            print("Paquetes recibidos con éxito! Texto completo: " , ''.join(lista))

            lista = []    

        except websockets.exceptions.ConnectionClosedOK:
            print("Servidor desconectado.")

if __name__ == "__main__":
    asyncio.run(chat())