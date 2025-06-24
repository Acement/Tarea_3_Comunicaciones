from cifrado import cypher_decypher as cy
import crcmod as crc

#Agrega la secuencia en el paquete
def sequencer(array):
    for i in range(0, len(array)):
        binary = bin(i)[2:]
        array[i] += binary.zfill(8)
    return array

#Agrega los datos cifrados al array
def data_add(array, text, cant, size):
    data_array = []

    for i in text:
        data_array.append(ord(i)) 
        
    print(data_array)


    #Llena los paquetes excepto el ultimo
    for i in range(0,cant - 1):
        for j in range(0,size):
            binary = bin(data_array[(size * i) + j])[2:]
            array[i] += binary.zfill(8)
            print(f"Valor agregado              : {int(binary,2)}")
            print(f"Valor agregado en binario   : {binary.zfill(8)}")
        print(f"Paquete hasta el momento: {array[i]}")
        print()

    #Calcula lo que falta del ultimo paquete
    if len(text) % size == 0:
        text_diff = size
    else:
        text_diff = len(text) % size

    print(f"Texto faltante: {text_diff}")

    #Agrega el paquete faltante
    for i in range(0,text_diff):
        binary = bin(data_array[(size * (cant - 1)) + i])[2:]
        array[cant - 1] += binary.zfill(8)
        print(f"Valor agregado              : {int(binary,2)}")
        print(f"Valor agregado en binario   : {binary.zfill(8)}")
    print(f"Paquete hasta el momento: {array[cant - 1]}")
    print()

    print(array)

    return array

#Agregar la cantidad de datos en el paquete y la cantidad de paquetes en total
def len_add(array, cant_paq):
    for i in range(0,len(array)):
        #Calcula la cantidad de datos y lo agrega
        cant_data = int(len(array[i]) / 8) - 1
        binary = bin(cant_data)[2:]
        array[i] += binary.zfill(8)
        print(f"Paquete hasta el momento: {array[i]}")
        
        #Agrega la cantidad total de paquetes
        binary = bin(cant_paq)[2:]
        array[i] += binary.zfill(8)
        print(f"Paquete hasta el momento: {array[i]}")
        print(i)

    return array

#Calcula el CRC-16-IBM y lo agrega al final del paquete
def crc_add(array):
    crc16 = crc.predefined.mkCrcFun('crc-16')
    for i in range(0,len(array)):
        crc_output = crc16(array[i].encode('utf-8'))
        crc_binary = format(crc_output,'016b')
        print(f"CRC-16 calculado: {crc_binary}")
        array[i] += crc_binary

    return array

#Agrega un byte lleno de 1s para terminar al paquete
def end_add(array):
    end = "1" * 8
    print(end)
    for i in range(0,len(array)):
        array[i] += end
    return array

#Empaqueta los datos
def packaging(text,key):

    #Calcula la cantidad de paquetes y crea un array de ese tamaño
    cant_paq = int(len(text) / len(key))
    if len(text) % len(key) != 0:
        cant_paq += 1

    print(f"Cantidad de paquetes: {cant_paq}")
    print()

    size_key = len(key)

    package_array = [""] * cant_paq

    #Agrega la secuencia en el paquete
    print("Agregando Secuencia...")
    package_array = sequencer(package_array)
    print("-------------------------------------------------------------------------")

    #Agrega los datos cifrados al array
    print("Agregando datos cifrados...")
    package_array = data_add(package_array, cy(text,key,False), cant_paq, size_key)
    print("-------------------------------------------------------------------------")

    #Agrega la cantidad de datos en el paquete y la cantidad total del paquete
    print("Agregando cantidad")
    package_array = len_add(package_array, cant_paq)
    print("-------------------------------------------------------------------------")

    #Agrega el checksum CRC-16_IBM
    print("Agregando CRC16...")
    package_array = crc_add(package_array)
    print("-------------------------------------------------------------------------")

    #Agregar fin de paquete
    print("Agregando Termino de paquete")
    package_array = end_add(package_array)
    print("-------------------------------------------------------------------------")

    return package_array


if __name__ == "__main__":
    #texto = input("Ingrese texto: ")
    #clave = input("Ingrese clave: ")
    texto = "hola mundo!"
    clave = "rombo"
    paq = packaging(texto,clave)