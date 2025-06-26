from paquete import packaging as pck
import random

CORRECT_SEND_PROB    = 0.80 #Probablidad de que se envie correctamente
NOT_SEND_PROB        = 0.05  #Probabilidad de que no se envie
INCORRECT_SEND_PROB  = 0.15 #Probabilidad de que se envie incorrectamente




def error_sim(array, csp, nsp, isp):
    send_opt_array = random.choices([0,1,2],weights=[csp, nsp, isp], k = len(array))
    send_array = []

    print(send_opt_array)
    print(f"Largo array de envio    : {len(array)}")
    print(f"Largo de array original : {len(send_opt_array)}")

    for i in range(0,len(array)):
        match(send_opt_array[i]):
            case 0: #Se envia correctamente
                send_array.append(array[i])
                print(f"El paquete {i} se envia Correctamente   : {array[i]}")
            case 1: #No se envia
                send_array.append("")
                print(f"El paquete {i} no se envia              : """)
            case 2: #Se envia de forma incorrecta
                incorrect_bin = array[i]
                for j in range(0,len(incorrect_bin)):
                    if random.uniform(0,1) <= 0.05:
                        if incorrect_bin[j] == '1':
                            incorrect_bin = incorrect_bin[:j] + '0' + incorrect_bin[j+1:]
                            print("Cambio")
                        else:
                            incorrect_bin = incorrect_bin[:j] + '1' + incorrect_bin[j+1:]
                            print("Cambio")
                send_array.append(incorrect_bin)
                print(f"El paquete {i} se envia con errores     : {incorrect_bin}")

    print(send_array)
    return send_array


if __name__ == "__main__":
    texto = "Did you ever hear the tragedy of Darth Plagueis the wise? No. I thought not, It's No story the jedi would tell you. It's a sith legend. Darth Plagueis was a Dark Lord of the sith. He was so powerful, Yet so wise. He could use the force to influence the medi chlorians to create, Life. He had such a knowledge of the Dark side, He could even keep the ones he cared about, From dying. He could actually, Save the ones he cared about from death? The dark side of the force is a pathway to many abilities some consider to be unnatural. Well what happened to him? Darth Plagueis became so powerful that the only thing he feared was losing his power, Which eventually of course he did. Unfortunately, He taught his apprentice everything he knew. Then his apprentice killed him in his sleep. Ironic, He could save others from death, But not himself. Is it possible to learn this power? Not from a jedi."
    clave = "rombo"
    package_array = pck(texto,clave)
    print(package_array)
    send_array = error_sim(package_array, CORRECT_SEND_PROB, NOT_SEND_PROB, INCORRECT_SEND_PROB)