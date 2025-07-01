## Funcion de cifrado cimetrico XOR 
# Es la misma operacion para cifrar y decifrar
def cypher_decypher(texto, clave):
    cypher_array = []
    key_array = []
    cypher_word = ''

    #Pasa el texto a int
    for i in texto:
        cypher_array.append(ord(i))

    #Pasa la clave a int
    for i in clave:
        key_array.append(ord(i))
    
    #Cifra la palabra
    aux = 0
    for i in range(0,len(cypher_array)):
        cypher_char = cypher_array[i] ^ key_array[aux]
        aux += 1
        if aux >= len(key_array):
            aux = 0
        cypher_word = cypher_word + chr(cypher_char)

    return cypher_word
