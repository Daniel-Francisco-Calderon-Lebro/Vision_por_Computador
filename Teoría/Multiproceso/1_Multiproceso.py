import multiprocessing
import time

def algo():
    print("Hola")
    time.sleep(1)
    print("Adios")

if __name__ == "__main__":
    proceso = multiprocessing.Process(target=algo)
    proceso.start()
    print("Finaliza proceso Padre")