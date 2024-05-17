import multiprocessing
import cv2

def activar_camara():
    video = cv2.VideoCapture(0)
    while True:
        ret, frame = video.read()
        if not ret:
            print("No se pudo capturar el fotograma")
            break
        cv2.imshow("Camara", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def procesar_frame(frame_queue, lock):
    # Simula el procesamiento del frame
    while True:
        # Esperar hasta que se pueda adquirir el bloqueo para solicitar un nuevo frame
        lock.acquire()
        
        # Obtener el frame actual de la cola
        frame = frame_queue.get()
        
        print("Procesando frame:", frame)
if __name__ == "__main__":
    # Crear una cola compartida para los frames
    frame_queue = multiprocessing.Queue()
    
    # Crear un bloqueo para coordinar la comunicación entre procesos
    lock = multiprocessing.Lock()
    
    # Adquirir inicialmente el bloqueo para que la función procesar_frame pueda comenzar a procesar
    lock.acquire()
    
    # Iniciar el proceso de la cámara
    proceso_camara = multiprocessing.Process(target=funcion_camara, args=(frame_queue, lock))
    proceso_camara.start()
    
    # Iniciar el proceso para procesar los frames
    proceso_procesar = multiprocessing.Process(target=procesar_frame, args=(frame_queue, lock))
    proceso_procesar.start()
    
    # El programa principal puede continuar ejecutándose mientras la cámara está activa
    while True:
        # Hacer otras tareas o simplemente esperar
        time.sleep(1)  # Por ejemplo, espera 1 segundo entre cada iteración
        
        # Si se necesita, se pueden tomar decisiones o realizar otras acciones aquí
        
        # Para salir del bucle principal, se puede agregar una condición de salida
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Salir")
        break
    
    # Si es necesario, se puede detener la cámara al salir del programa principal
    proceso_camara.terminate()
