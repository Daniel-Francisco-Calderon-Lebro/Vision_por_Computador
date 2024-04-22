from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import time

def funcion1(a, b):
    time.sleep(5)
    return a + b

def funcion2(a, b):
    time.sleep(2)
    return a + b
def funcion3(a, b):
    time.sleep(1)
    return a + b

def resultado1(futuro):
    print("la suma es: ", futuro.result())

if __name__ == "__main__":

    # #ejemplo 1###############################################
    # with ProcessPoolExecutor(max_workers=2) as executor:
    #     futuro1 = executor.submit(funcion1, 5, 10)
    #     futuro1.add_done_callback(resultado1)

    #     futuro2 = executor.submit(funcion2, 50, 1)
    #     futuro2.add_done_callback(resultado1)

    #     futuro3 = executor.submit(funcion3, 38, 15)
    #     futuro3.add_done_callback(resultado1)

    #     Ejemplo 2################################################
    # con multiprocesos y shutdown ############################
    executor = ProcessPoolExecutor(max_workers=2)
    futuro1 = executor.submit(funcion1, 5, 10)
    futuro1.add_done_callback(resultado1)

    futuro2 = executor.submit(funcion2, 50, 1)
    futuro2.add_done_callback(resultado1)

    futuro3 = executor.submit(funcion3, 100, 100)
    futuro3.add_done_callback(resultado1)

    executor.shutdown()
    print("finalizo la ejecucion")





