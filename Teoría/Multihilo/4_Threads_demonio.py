import time
import threading


# def prueba1():
#     while True:
#         print("ejecutando hilo 1")
#         time.sleep(0.5)


# hilo = threading.Thread(target=prueba1)

# hilo.start()
# print("Hola")

##################con hilo demonio################

def prueba1():
    while True:
        print("ejecutando hilo 1")
        time.sleep(0.5)




hilo = threading.Thread(target=prueba1, daemon=True)
hilo.start()
print("Hola")

# con hilo demonio se puede terminar el programa cuando el theread principal para

