import cv2
import os

# Ruta absoluta al archivo Haar Cascade
cascade_path = 'C:/Users/Daniel Calderon/Desktop/2024-1 Poli/Vision por computador/Clasificadores/haarcascade_frontalface_default.xml'

# Verificar si el archivo Haar Cascade existe
if not os.path.isfile(cascade_path):
    print(f"Error: Haar Cascade file '{cascade_path}' not found.")
    exit(1)

# Cargar el archivo Haar Cascade
haar_cascade = cv2.CascadeClassifier(cascade_path)

# Verificar si el clasificador Haar Cascade se cargó correctamente
if haar_cascade.empty():
    print("Error: Could not load Haar Cascade Classifier.")
    exit(1)

# Inicializar captura de video
cap = cv2.VideoCapture(0)

# Verificar si se abrió la captura de video correctamente
if not cap.isOpened():
    print("Error: Could not open video capture.")
    exit(1)

while cap.isOpened():
    # Leer un fotograma de la cámara
    ret, frame = cap.read()
    if not ret:
        print("No se pudo capturar el fotograma")
        break
    
    # Voltear el fotograma horizontalmente para efecto espejo
    frame = cv2.flip(frame, 1)
    
    # Convertir el fotograma a escala de grises
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Aplicar el método de detección de rostros en la imagen en escala de grises
    faces_rect = haar_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=9)
    
    # Dibujar rectángulos alrededor de los rostros detectados
    for (x, y, w, h) in faces_rect:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Mostrar el fotograma con los rostros detectados
    cv2.imshow('Detected faces', frame)
    
    # Salir del bucle cuando se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar captura de video y cerrar todas las ventanas de OpenCV
cap.release()
cv2.destroyAllWindows()
