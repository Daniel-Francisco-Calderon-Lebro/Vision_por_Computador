import time
import threading


# a = 0

# def sumar():
#     global a
#     for _ in range(1000000):
#         a += 1

# def restar():
#     global a
#     for _ in range(1000000):
#         a -= 1
        

# #############Main Thread############
# ############sin race condition############
# ############Manejo de variables en distintos hilos#########

# hilo1 = threading.Thread(target=sumar)
# hilo2 = threading.Thread(target=restar)

# hilo1.start()
# hilo2.start()

# hilo1.join()
# hilo2.join()

# print(a)
###############################################################################################################################################################
# ############# con race condition ############

# ####Tener en cuenta que si se usa 2 veces lock.acquire() o lock.release() el programa no funciona se queda colgado

# lock = threading.Lock()
# a = 0

# def sumar():
#     global a
#     for _ in range(1000000):
#         lock.acquire() # bloquea el acceso a la variable
#         a += 1
#         lock.release()

# def restar():
#     global a
#     for _ in range(1000000):
#         lock.acquire()
#         a -= 1
#         lock.release()

# #############Main Thread############
# ############sin race condition############
# ############Manejo de variables en distintos hilos#########

# hilo1 = threading.Thread(target=sumar)
# hilo2 = threading.Thread(target=restar)

# hilo1.start()
# hilo2.start()

# hilo1.join()
# hilo2.join()

# print(a)



# ##############se queda colgado###############################
# ####Tener en cuenta que si se usa 2 veces lock.acquire() o lock.release() el programa no funciona se queda colgado

# lock = threading.Lock()
# a = 0

# def sumar():
#     global a
#     for _ in range(1000000):
#         lock.acquire()
#         lock.acquire()
#         a += 1
#         lock.release()

# def restar():
#     global a
#     for _ in range(1000000):
#         lock.acquire()
#         a -= 1
#         lock.release()

# #############Main Thread############
# ############sin race condition############
# ############Manejo de variables en distintos hilos#########

# hilo1 = threading.Thread(target=sumar)
# hilo2 = threading.Thread(target=restar)

# hilo1.start()
# hilo2.start()

# hilo1.join()
# hilo2.join()

# print(a)






####################################################################################################################################

############con race condition############ usar Rlock Rlock()
## las veces que se usa lock.acquire() o lock.release() se tienen que cerrar

####Tener en cuenta que si se usa 2 veces lock.acquire() o lock.release() el programa no funciona se queda colgado

lock = threading.RLock()
a = 0

def sumar():
    global a
    for _ in range(1000000):
        lock.acquire() # bloquea el acceso a la variable
        lock.acquire()
        a += 1
        lock.release()
        lock.release()

def restar():
    global a
    for _ in range(1000000):
        lock.acquire()
        a -= 1
        lock.release()

#############Main Thread############
############sin race condition############
############Manejo de variables en distintos hilos#########

hilo1 = threading.Thread(target=sumar)
hilo2 = threading.Thread(target=restar)

hilo1.start()
hilo2.start()

hilo1.join()
hilo2.join()

print(a)
