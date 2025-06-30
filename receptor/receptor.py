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

def descifrar(datos_cifrados):
    data_text = ""
    for i in range (0, len(datos_cifrados) // 8):
        data_text += chr(int(datos_cifrados[(8*i): (8*i) + 8],2))

    return cy(data_text, CLAVE)

async def chat():
    uri = "ws://25.53.150.13:8765"
    async with websockets.connect(uri) as websocket:
        print("Conectado al servidor.")
        try:
            mensaje_original = input("Enviar mensaje: ")
            mensaje = mensaje_original
            await websocket.send(mensaje)
            prev_sec = True
            cant_paq = 1
            while len(lista)<cant_paq:
                # Cliente envía texto plano
                
                server_message = await websocket.recv()
                if (server_message !=""):
                    seq, bin_data, cant_paq, cant_data, crc = data_dump(server_message)
                    seq = seq=="1"
                    mensaje = descifrar(bin_data)

                    if (verificacion(prev_sec, seq, bin_data, server_message[:-24], cant_paq,cant_data, crc)):
                        prev_sec = seq
                        lista.append(mensaje)
                        await websocket.send(str(int(seq)))
                    else:
                        await websocket.send(str(int(prev_sec)))
                        
                    print(f"Mensaje: {mensaje}")     
            print("largo lista : ", len(lista))
            print (''.join(lista)==mensaje_original)     
            print("Paquetes recibidos con éxito!", ''.join(lista))        
        except websockets.exceptions.ConnectionClosedOK:
            print("Servidor desconectado.")

if __name__ == "__main__":
    asyncio.run(chat())
