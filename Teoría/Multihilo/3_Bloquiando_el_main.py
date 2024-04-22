#######Main Thread########

import time
import threading
##############################################################
# ########Hilo1 secundario########
# def dormir():
#     time.sleep(0.3)
#     print("desperté")


# hilo = threading.Thread(target=dormir)
# hilo.start()



# ######################Main Thread########
# for i in range(20):
#     time.sleep(0.05)
#     print(i)




##############################################################


# # ########sin thread########
# def prueba1():
#     time.sleep(4)
#     return 5

# def prueba2():
#     time.sleep(2.5)
#     return 3

# def prueba3():
#     time.sleep(1)
#     return 8


# x=prueba1()
# y=prueba2()
# z=prueba3()

# if x==5 and y==3 and z==8:
#     print("correcto")
# else:
#     print("incorrecto")


##########Conthread pero sin join()########

# def prueba1():
#     global x
#     time.sleep(4)
#     x = 5
#     print("terminando hilo 1")

# def prueba2():
#     global y
#     time.sleep(2.5)
#     y = 3
#     print("terminando hilo 2")

# def prueba3():
#     global z
#     time.sleep(1)
#     z = 8
#     print("terminando hilo 3")

# #########Main Thread########
# x=0
# y=0
# z=0

# hilo1 = threading.Thread(target=prueba1)
# hilo2 = threading.Thread(target=prueba2)
# hilo3 = threading.Thread(target=prueba3)

# hilo1.start()
# hilo2.start()
# hilo3.start()


# print(x,y,z)
# if x==5 and y==3 and z==8:
#     print("correcto")
# else:
#     print("incorrecto")



###############################################################


##########Conthread pero CON join()########

def prueba1():
    global x
    time.sleep(4)
    x = 5
    print("terminando hilo 1")

def prueba2():
    global y
    time.sleep(2.5)
    y = 3
    print("terminando hilo 2")

def prueba3():
    global z
    time.sleep(1)
    z = 8
    print("terminando hilo 3")

#########Main Thread########
x=0
y=0
z=0

hilo1 = threading.Thread(target=prueba1)
hilo2 = threading.Thread(target=prueba2)
hilo3 = threading.Thread(target=prueba3)

hilo1.start()
hilo2.start()
hilo3.start()
hilo1.join()
hilo2.join()
hilo3.join()

###########################Ahora si esperar a que todos los hilos terminen
print(x,y,z)
if x==5 and y==3 and z==8:
    print("correcto")
else:
    print("incorrecto")

