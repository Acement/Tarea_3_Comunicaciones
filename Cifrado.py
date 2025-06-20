MOSTRAR_PROCESO = False

## Funcion de cifrado cimetrico XOR 
# Es la misma operacion para cifrar y decifrar
def cypher_decypher(texto, clave, mostrar):
    cypher_array = []
    key_array = []
    cypher_word = ''

    #Pasa el texto a int
    for i in texto:
        cypher_array.append(ord(i))

    #Pasa la clave a int
    for i in clave:
        key_array.append(ord(i))

    #Mostrar el proceso
    if mostrar == True:
        print(cypher_array)
        print(key_array)
    
    #Cifra la palabra
    aux = 0
    for i in range(0,len(cypher_array)):
        cypher_char = cypher_array[i] ^ key_array[aux]
        aux += 1
        if aux >= len(key_array):
            aux = 0
        cypher_word = cypher_word + chr(cypher_char)

        #Mostrar el proceso
        if mostrar == True:
            print(f"Resultado de XOR: {cypher_char}")
            if cypher_char < 33:
                print(f"Letra agregada  : CTRL + {cypher_char}") #Muestra el valor ASCII del caracter de control que dio como resultado de la operacion
            else:
                print(f"Letra agregada  : {chr(cypher_char)}")
            print(f"Palabra cifrada : {cypher_word}")

    return cypher_word

if __name__ == "__main__":
    texto = input ("Ingrese texto: ")
    clave = input ("Ingrese clave: ")
    texto_cifrado = cypher_decypher(texto,clave, MOSTRAR_PROCESO)

    print(f"Texto sin cifrar            : {texto}")
    print(f"Largo de texto sin cifrar   : {len(texto)}")

    print(f"Texto cifrado               : {texto_cifrado}")
    print(f"Largo de texto cifrado      : {len(texto_cifrado)}")

    texto_descifrado = cypher_decypher(texto_cifrado,clave, MOSTRAR_PROCESO)
    print(f"Texto cifrado               : {texto_descifrado}")
    print(f"Largo de texto cifrado      : {len(texto_descifrado)}")