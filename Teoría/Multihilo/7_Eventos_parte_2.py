import time
import threading


def ciclar1(evento1, evento3):
    while not evento3.is_set():
        evento1.wait() #si esta en false no hace nada
        print("cilcando1")
        evento1.clear()
        time.sleep(0.1)

def ciclar2(evento2, evento3):
    while not evento3.is_set():
        evento2.wait()#si esta en false no hace nada
        print("cilcando2")
        evento2.clear()
        time.sleep(0.1)


evento1 = threading.Event()
evento2 = threading.Event()
evento3 = threading.Event()

hilo1 = threading.Thread(target=ciclar1, args=(evento1, evento3))
hilo2 = threading.Thread(target=ciclar2, args=(evento2, evento3))

hilo1.start()
hilo2.start()

for i in range(5):
    evento1.set()
    time.sleep(0.1)
    evento2.set()
    time.sleep(0.1)

evento3.set()