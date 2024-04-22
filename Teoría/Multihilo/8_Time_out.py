import time
import threading


def ciclar(evento1):
    print("Presione para enviar la senal\n")
    respuesta = evento1.wait(timeout=5)
    if respuesta:
        print("Sistema de enfriamiento encendido de forma manual")
    else:
        print("Sistema de enfriamiento encendido de forma automatica")

evento1 = threading.Event()
hilo = threading.Thread(target=ciclar, args=(evento1,))


print("Alamar al sistema de enfriamiento")
hilo.start()
time.sleep(3)
#evento1.set() #enciende el sistema de enfriamiento de forma manual
time.sleep(1)