from cifrado import cypher_decypher as cy
import crcmod as crc
import random

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

#Calcula CRC-16-IBM
def calc_crc(data):
    crc16 = crc.predefined.mkCrcFun('crc-16')
    crc_output = crc16(data.encode('utf-8'))
    crc_binary = format(crc_output,'016b')
    return crc_binary

#Agrega el checksum CRC-16 al final del paquete
def crc_add(array):
    for i in range(0,len(array)):
        crc_binary = calc_crc(array[i])
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

def mixer(array):
    mixed_array = array.copy()
    random.shuffle(mixed_array)
    print(f"Array sin mezclar       : {array}")
    print("Largo de los elementos   : ",end="")
    for i in array:
        print(len(i),end=", ")
    print()

    print(f"Array mezclado      : {mixed_array}")
    print("Largo de los elementos   : ",end="")
    for i in mixed_array:
        print(len(i),end=", ")
    print()

    return mixed_array

#Mira si la integridad del paquete esta bien usando checksum
def check_checksum(package):
    check = True
    print(f"Largo original  : {len(package)}")
    check_sum = package[-24:-8]
    crc_binary = calc_crc(package[:-24])

    if check_sum != crc_binary:
        check = False
        print("ERROR!, Checksum no coincide")
    else:
        print("Checksum")
        package = package[:-24]
        print(f"Paquete cortado : {package}")
        print(f"Largo Nuevo     : {len(package)}")
        print()
        
    return package,check

def data_dump(package):
    seq = int(package[:8],2)
    #seq = package[:8]

    cant_paq = int(package[-8:],2)
    #cant_paq = package[-8:]

    cant_data = int(package[-16:-8],2)
    #cant_data = package[-16:-8]

    bin_data = package[8:-16]
    data_text = ""

    #print(f"Largo del paquete   : {len(package)}")
    #print(f"Suma de las partes  : {len(seq) + len(cant_paq) + len(cant_data) + len(data)}")

    for i in range(0,cant_data):
        data_text += chr(int(bin_data[(8*i): (8*i) + 8],2))

    print(f"Numero de secuencia             : {seq}")
    print(f"Cantidad total de paquetes      : {cant_paq}")
    print(f"Cantidad de datos en el paquete : {cant_data}")
    print(f"Cantidad real de datos          : {len(bin_data)/8}")
    print

    return seq, data_text, cant_paq




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
    package_array = data_add(package_array, cy(text,key), cant_paq, size_key)
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

#Hace las operaciones de desempaquetado, ordenado y descifrado, sirve para este ejemplo
def data(array,key):
    mixed_tuples = []
    cyphered_text = ""
    for i in array:
        mixed_tuples.append(depackaging(i,key))

    ordered_data = [""] * len(mixed_tuples)
    print(len(ordered_data))
    for i in mixed_tuples:
        ordered_data[i[0]] = i[1]
    
    for i in ordered_data:
        cyphered_text += i

    decyphered_text = cy(cyphered_text,key)
    print(decyphered_text)



    


#Desempaqueta, Devuelve una "tupla" talque: [numero de sequencia, datos]
def depackaging(package,key):
    depackaged = package

    print("Checkeando integridad")
    depackaged,check = check_checksum(package)
    print("-------------------------------------------------------------------------")
    if check: 
        print()
        seq, data_text, cant_packages = data_dump(depackaged)
        depackaged = [seq,data_text]
        return depackaged
    else:
        print("Error!, Checksum malo")
        #Aqui colocar como se sale


if __name__ == "__main__":
    #texto = input("Ingrese texto: ")
    #clave = input("Ingrese clave: ")
    texto = "hola mundo!"
    clave = "rombo"
    paq = packaging(texto,clave)
    print("Mezclando paquetes")
    mixed_paq = mixer(paq)
    print("-------------------------------------------------------------------------")
    data(mixed_paq,clave)
    