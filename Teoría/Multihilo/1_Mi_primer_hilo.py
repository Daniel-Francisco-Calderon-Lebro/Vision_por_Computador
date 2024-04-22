import time
import threading

# ## Definir la función que se ejecutará en un hilo
# def imprimirValor():
#     time.sleep(0.3)
#     print("Hola mundo")

# #ejecucion secuencial
# for i in range(15):
#     imprimirValor()

# #ejecucion concurrente creamos 15 hilos
# for i in range(15):
#     hilo = threading.Thread(target=imprimirValor)
#     hilo.start()

def imprimir1():
    time.sleep(0.3)
    print("ejecutando hilo 1")

def imprimir2():
    time.sleep(0.3)
    print("ejecutando hilo 2")

def imprimir3():
    time.sleep(0.3)
    print("ejecutando hilo 3")

hilo1 = threading.Thread(target=imprimir1)
hilo2 = threading.Thread(target=imprimir2)
hilo3 = threading.Thread(target=imprimir3)

hilo1.start()
hilo2.start()
hilo3.start()