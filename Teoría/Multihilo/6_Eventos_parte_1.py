import time
import threading



def ciclar(evento1, evento2):
    while not evento2.is_set():
        print("cilcando")
        evento1.wait()

evento1 = threading.Event()
evento2 = threading.Event()

hilo = threading.Thread(target=ciclar, args=(evento1, evento2))

hilo.start()

for i in range(5):
    time.sleep(0.5)
    print("Realizando for")

evento1.set()
time.sleep(1)
evento2.set()