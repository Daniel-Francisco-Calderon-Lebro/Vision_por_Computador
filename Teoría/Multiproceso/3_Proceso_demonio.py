import multiprocessing
import time

# def conteo(cantidad):
#     for i in range(cantidad):
#         time.sleep(0.5)
#         print(i)


# if __name__ == "__main__":
#     print("Inicia proceso Padre")
#     proceso = multiprocessing.Process(target=conteo, kwargs={"cantidad": 10}, daemon=False)
#     proceso.start()

#     print("Finaliza proceso Padre")



def conteo(cantidad):
    for i in range(cantidad):
        time.sleep(0.5)
        print(i)


if __name__ == "__main__":
    print("Inicia proceso Padre")
    proceso = multiprocessing.Process(target=conteo, kwargs={"cantidad": 10}, daemon=True)
    proceso.start()
    time.sleep(5)
    print("Finaliza proceso Padre")