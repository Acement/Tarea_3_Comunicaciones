import random

CORRECT_SEND_PROB     = 0.70 # Probablidad de que se envie correctamente
INCOMPLETE_SEND_PROB  = 0.15 # Probabilidad de que se envie incompleto
INCORRECT_SEND_PROB   = 0.15 # Probabilidad de que se envie incorrectamente

def error_sim(message):
    send_opt = random.choices([0, 1, 2], weights=[CORRECT_SEND_PROB, INCOMPLETE_SEND_PROB, INCORRECT_SEND_PROB], k=1)[0]
    error_message = ""
    #print(send_opt_array)
    #print(f"Largo array de envio    : {len(array)}")
    #print(f"Largo de array original : {len(send_opt_array)}")

    match(send_opt):
        case 0: #Se envia correctamente
            error_message = message
            #print(f"El paquete se envia Correctamente   : {error_message}")
        case 1: #Se envia con menos bits
            error_message = message
            for j in range(0,len(error_message)):
                if random.uniform(0,1) <= 0.05:
                    error_message = error_message[:j] + error_message[j+1:]
            #print(f"El paquete se envia con menos bits  : {error_message}")
        case 2: #Se envia de forma incorrecta
            error_message = message
            for j in range(0,len(error_message)):
                if random.uniform(0,1) <= 0.05:
                    if error_message[j] == '1':
                        error_message = error_message[:j] + '0' + error_message[j+1:]
                        #print("Cambio")
                    else:
                        error_message = error_message[:j] + '1' + error_message[j+1:]
                        #print("Cambio")
            ##print(f"El paquete se envia con errores    : {error_message}")

    #print(error_message)
    return error_message
