from cifrado import cypher_decypher as cy
import crcmod as crc

#Calcula CRC-16-IBM
def calc_crc(data):
    crc16 = crc.predefined.mkCrcFun('crc-16')
    crc_output = crc16(data.encode('utf-8'))
    crc_binary = format(crc_output,'016b')
    return crc_binary

def data_dump(package):
    seq = package[0]
    bin_data = package[0:-40]

    cant_paq = int(package[-40:-32],2)
    cant_data = int(package[-32:-24],2)

    crc = package[-24:-8]

    return seq, bin_data, cant_data,cant_paq, crc