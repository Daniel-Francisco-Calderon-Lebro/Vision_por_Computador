import time
import threading
from concurrent.futures import ThreadPoolExecutor
from threading import current_thread

# def sumar(a, b):
#     time.sleep(0.1)
#     print(current_thread().getName())
#     print(a + b, "\n")


# excecutor = ThreadPoolExecutor(max_workers=2) #subclases de ThreadPoolExecutor
# excecutor.submit(sumar, 2, 3)
# excecutor.submit(sumar, 5, 9)
# excecutor.submit(sumar, 7, 8)
# excecutor.submit(sumar, 4, 6)
# excecutor.submit(sumar, 1, 1)

# excecutor.shutdown()


# def sumar(a, b):
#     time.sleep(5)
#     return a + b

# def fin(futuro):
#     print("finalizo la ejecucion")
#     print(futuro.result())

# excecutor = ThreadPoolExecutor(max_workers=2) #subclases de ThreadPoolExecutor
# futuro = excecutor.submit(sumar, 15, 37)
# futuro.add_done_callback(fin)


# for i in range(15):
#     time.sleep(0.5)
#     print(i)



def sumar(a, b):
    time.sleep(5)
    return a + b

def fin1(futuro):
    print("finalizo la suma 1")
    print(futuro.result())

def fin2(futuro):
    print("finalizo la suma 2")
    print(futuro.result())

def fin3(futuro):
    print("finalizo la suma 3")
    print(futuro.result())
def fin4(futuro):
    print("finalizo la suma 4")
    print(futuro.result())


excecutor = ThreadPoolExecutor(max_workers=2) #subclases de ThreadPoolExecutor
futuro = excecutor.submit(sumar, 15, 37)
futuro.add_done_callback(fin1)
futuro.add_done_callback(fin2)
futuro.add_done_callback(fin3)
futuro.add_done_callback(fin4)


for i in range(15):
    time.sleep(0.2)
    print(i)