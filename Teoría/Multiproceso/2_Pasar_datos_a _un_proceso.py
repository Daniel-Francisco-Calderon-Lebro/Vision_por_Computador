import multiprocessing
import time

def suma(a, b):
    print(a + b)


if __name__ == "__main__":
    proceso1 = multiprocessing.Process(target=suma, args=(10, 25))
    proceso2 = multiprocessing.Process(target=suma, args=(5, 5))
    proceso3 = multiprocessing.Process(target=suma, args=(2, 3))
    proceso4 = multiprocessing.Process(target=suma, kwargs={"a":10, "b":25})
    proceso1.start()
    proceso2.start()
    proceso3.start()
    proceso4.start()
    print("Finaliza proceso Padre")