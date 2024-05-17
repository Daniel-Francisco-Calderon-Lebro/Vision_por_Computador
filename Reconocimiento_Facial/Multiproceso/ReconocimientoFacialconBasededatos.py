import cv2 as cv
import numpy as np
import os

direccion_basededatos = "Reconocimiento_Facial/basededatos"

def abrir_camara():
    """Abrir la cámara"""
    cap = cv.VideoCapture(0)
    return cap

def stop_camara(cap):
    """Detener la cámara"""
    cap.release()
    cv.destroyAllWindows()

def abrir_basededatos():
    """Abrir el clasificador de detección de rostros"""
    return cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

def cargar_imagenes(direccion_basededatos):
    """Cargar las imágenes de la base de datos"""
    return os.listdir(direccion_basededatos)

def extraer_caracteristicas(direccion_basededatos):
    """Extraer las características de la base de datos"""
    archivo_caracteristicas = os.path.join(direccion_basededatos, "caracteristicas.npy")
    if os.path.exists(archivo_caracteristicas):
        return np.load(archivo_caracteristicas)
    else:
        print("No se encontró el archivo de características.")
        return None

def extraer_caracteristicas_imagenes(direccion_imagen):
    """Extraer las características de una imagen"""
    # Ejemplo simple: Extracción de características utilizando Haar Cascades
    imagen = cv.imread(direccion_imagen, cv.IMREAD_GRAYSCALE)
    # Inicializar el clasificador de Haar para detectar rostros
    clasificador = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # Detectar rostros en la imagen
    rostros = clasificador.detectMultiScale(imagen, scaleFactor=1.1, minNeighbors=5)
    # Devolver el número de rostros detectados como características
    return np.array([len(rostros)])

def main():
    video = abrir_camara()
    base = abrir_basededatos()
    imagenes = cargar_imagenes(direccion_basededatos)
    caracteristicas = extraer_caracteristicas(direccion_basededatos)
    
    if caracteristicas is None:
        stop_camara(video)
        return
    
    while True:
        ret, frame = video.read()

        if not ret:
            break

        # Convertir el fotograma a escala de grises
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # Detectar rostros en el fotograma
        faces = base.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        # Dibujar un rectángulo alrededor de cada rostro detectado
        for (x, y, w, h) in faces:
            cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            # Extraer la cara del fotograma y colocarle el nombre de la foto de la base de datos
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            # colocarle el nombre del archivo de la base de datos
            for i, imagen in enumerate(imagenes):
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
                # Extraer características de la imagen actual
                caracteristicas_imagen_actual = extraer_caracteristicas_imagenes(os.path.join(direccion_basededatos, imagen))
                # Comparar las características extraídas con las características de la base de datos
                if np.array_equal(caracteristicas, caracteristicas_imagen_actual):
                    # Si las características coinciden, mostrar el nombre de la imagen
                    cv.putText(frame, imagen, (x, y+h+30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Mostrar el fotograma con el reconocimiento facial superpuesto
        cv.imshow('Reconocimiento Facial', frame)
        # comparar el fotograma con la base de datos
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    stop_camara(video)

if __name__ == "__main__":
    main()
