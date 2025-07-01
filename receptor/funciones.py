from cifrado import cypher_decypher as cy
import crcmod as crc

#Calcula CRC-16-IBM
def calc_crc(data):
    crc16 = crc.predefined.mkCrcFun('crc-16')
    crc_output = crc16(data.encode('utf-8'))
    crc_binary = format(crc_output,'016b')
    return crc_binary

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
    #seq = package[0]
    bin_data = package[0:-40]

    cant_paq = int(package[-40:-32],2)
    cant_data = int(package[-32:-24],2)

    crc = package[-24:-8]

    return bin_data, cant_data,cant_paq, crc

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
    return(decyphered_text)

#Desempaqueta, Devuelve una "tupla" talque: [numero de sequencia, datos]
def depackaging(package,key):
    depackaged = package

    print("Checkeando integridad")
    depackaged,check = check_checksum(package)
    seq, data_text, cant_packages = data_dump(depackaged)
    depackaged = [seq,data_text]
    print("-------------------------------------------------------------------------")
    if check: 
        print()
        return depackaged
    else:
        print("Error!, Checksum malo")
        return [seq, "????????"]
        #Aqui colocar como se sale

    