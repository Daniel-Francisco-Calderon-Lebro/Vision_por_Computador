import time
import threading


def sumar(a, b):
    print(a + b)

# hilo = threading.Thread(target=sumar, args=[2, 3])
# hilo.start()

# hilo = threading.Thread(target=sumar, args=(5, 9))
# hilo.start()

hilo = threading.Thread(target=sumar, kwargs={'a': 5, 'b': 9})
hilo.start()

####################################################################
# def sumar(a):
#     print(a + a)

# hilo = threading.Thread(target=sumar, args=(5,))
# hilo.start()

#######################################################################

