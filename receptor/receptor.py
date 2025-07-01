import asyncio
import websockets
from cifrado import cypher_decypher as cy
from funciones import data_dump, calc_crc

CLAVE = "rombo"
lista = []

#crc, verif secuencia (duplicado, < max mensajes), cant bits recibidas sea = cant datos en cada paquete
def verificacion(prev_sec, seq, bin_data, datos_crc, cant_paq, cant_data, crc):
    
    return (crc == calc_crc(datos_crc) 
            and cant_data == int(len(bin_data)/8) 
            and cant_paq >= int(len(lista)) 
            and prev_sec != seq)

def verificar_crc16(datos_crc,crc):
    return crc == calc_crc(datos_crc)

def verificar_cant_paq(cant_paq):
    return int(len(lista)) < cant_paq

def verificar_cant_data(bin_data):
    return cant_data == int(len(bin_data)/8) 

def verificar_prev_seq(prev_seq,seq):
    return prev_seq != seq

def traducir(datos_cifrados):
    data_text = ""
    for i in range (0, len(datos_cifrados) // 8):
        data_text += chr(int(datos_cifrados[(8*i): (8*i) + 8],2))

    return data_text

async def chat():
    uri = "ws://25.53.150.13:8765"
    async with websockets.connect(uri) as websocket:
        print("Conectado al servidor.")
        try:
            mensaje_original = input("Enviar mensaje: ")
            mensaje = mensaje_original
            await websocket.send(mensaje)
            cant_paq = 1
            while len(lista) < cant_paq:
                # Espera el paquete enviado por el emisor
                server_message = await websocket.recv()
                if (len(server_message) >= 48):
                    bin_data, cant_paq, cant_data, crc = data_dump(server_message)

                    mensaje = traducir(mensaje)
                    mensaje = cy(mensaje, CLAVE)

                    # Verificación de errores
                    if (not verificar_crc16(bin_data+cant_paq+cant_data, crc)):
                        await websocket.send("10001111")
                        continue
                    if (not verificar_cant_paq(cant_paq)):
                        await websocket.send("01001111")
                        continue
                    if (not verificar_cant_data(bin_data)):
                        await websocket.send("00101111")
                        continue
                    #if (not verificar_prev_seq(prev_seq,seq)):
                    #    await websocket.send("00010000")
                    #    continue

                    lista.append(mensaje)
                    await websocket.send("00000000")
                        
                    print(f"Mensaje: {mensaje}")
                else:
                    await websocket.send("00011111") 
                        
            print("largo lista : ", len(lista))
            print (''.join(lista)==mensaje_original)     
            print("Paquetes recibidos con éxito!", ''.join(lista))

            lista = []    

        except websockets.exceptions.ConnectionClosedOK:
            print("Servidor desconectado.")

if __name__ == "__main__":
    asyncio.run(chat())
