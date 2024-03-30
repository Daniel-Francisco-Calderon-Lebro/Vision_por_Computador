import cv2
import numpy as np
import os

import cv2
print("Versión de OpenCV (cv2):", cv2.__version__)


def abrir_camara():
    """Abrir la cálara"""
    cap = cv2.VideoCapture(0)
    return cap

def stop_camara(cap):
    """Detener la cálara"""
    cap.release()
    cv2.destroyAllWindows()



while True:
    #1. Abrir la camara
    video = abrir_camara()
    while True:
        #2. Leer el fotograma
        ret, frame = video.read()
        # #3. Trasponer el fotograma 180°
        frame = cv2.flip(frame, 1)
        # # #4. Cambiar el frame a RGB
        # gray= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # # #5. Cambia el frame a escala de grises
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # #6. Detectar rostros en el fotograma
        face=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        #6. Dibujar un rectángulo alrededor de cada rostro detectado
        faces = face.detectMultiScale(frame, 1.3, 5)
        #7. Dibujar un rectángulo alrededor de cada rostro detectado de color azul
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255, 0), 2)
        cv2.imshow('frame', frame)
        #aca se termina la detección de rostros
        if cv2.waitKey(1) & 0xFF == ord('q'):
        
            break
        if not ret:
            break
        
        
        KeyboardInterrupt()
    stop_camara(video)
    break


#funcion para extraer las caracteristicas del rotro

