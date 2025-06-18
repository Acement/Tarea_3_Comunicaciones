def cypher(texto,clave):
    cypher_array = []
    key_array = []
    cypher_word = ''

    #Pasa el texto a int
    for i in texto:
        cypher_array.append(ord(i))
    
    print(cypher_array)

    #Pasa la clave a int
    for i in clave:
        key_array.append(ord(i))

    print(key_array)
    
    #Cifra la palabra
    aux = 0
    for i in range(0,len(cypher_array)):
        cypher_char = cypher_array[i] ^ key_array[aux]
        #cypher_char += 33
        #print(f"Resultado de XOR: {cypher_char}")
        aux += 1
        if aux >= len(key_array):
            aux = 0
        cypher_word = cypher_word + chr(cypher_char)
        #print(f"Letra agregada  : {chr(cypher_char)}")
        #print(f"Palabra cifrada : {cypher_word}")



    return cypher_word

def decypher(texto):
    return texto

if __name__ == "__main__":
    texto = input ("Ingrese texto: ")
    clave = input ("Ingrese clave: ")
    texto_cifrado = cypher(texto,clave)

    print(f"Texto sin cifrar            : {texto}")
    print(f"Largo de texto sin cifrar   : {len(texto)}")

    print(f"Texto cifrado               : {texto_cifrado}")
    print(f"Largo de texto cifrado      : {len(texto_cifrado)}")

    texto_descifrado = cypher(texto_cifrado,clave)
    print(f"Texto cifrado               : {texto_descifrado}")
    print(f"Largo de texto cifrado      : {len(texto_descifrado)}")