import multiprocessing
import time


def conteo(cantidad,queue):
    for i in range(cantidad):
        time.sleep(0.5)
        print(i)
        queue.put("Hola "+str(i))


if __name__ == "__main__":
    queue = multiprocessing.Queue()
    print("Inicia proceso Padre")
    proceso = multiprocessing.Process(target=conteo, kwargs={"cantidad": 10,"queue":queue}, daemon=True)
    proceso.start()
    time.sleep(5)
    print("Finaliza proceso Padre")
    while not queue.empty():
        print(queue.get())