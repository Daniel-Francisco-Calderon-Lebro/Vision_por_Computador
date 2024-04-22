import time
import threading
from concurrent.futures import ThreadPoolExecutor
from threading import current_thread
from concurrent.futures import as_completed


# def sumar(a, b):
#     time.sleep(1)
#     return a + b

# ex = ThreadPoolExecutor(max_workers=3)
# lista = [(2, 3), (5, 1), (8, 6), (9, 5)]
# listafuturos = [ex.submit(sumar, a, b) for a, b in lista]

# for futuro in as_completed(listafuturos):
#     print(futuro.result())



def sumar(datos):
    time.sleep(1)
    return datos[0] + datos[1]

ex = ThreadPoolExecutor(max_workers=3)
lista = [(2, 3), (5, 1), (8, 6), (9, 5)]
listafuturos = ex.map(sumar, lista)

for valores in listafuturos:
    print(valores)