import os
import face_recognition
import cv2

# Cargar imágenes y generar codificaciones
ruta_carpeta = "Reconocimiento_Facial\\basededatos"
codificaciones_rostros_conocidos = []
nombres_rostros_conocidos = []

for filename in os.listdir(ruta_carpeta):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        ruta_imagen = os.path.join(ruta_carpeta, filename)
        imagen = face_recognition.load_image_file(ruta_imagen)
        codificaciones_rostro = face_recognition.face_encodings(imagen, model="hog")
        
        if codificaciones_rostro:
            codificacion_rostro = codificaciones_rostro[0]
            codificaciones_rostros_conocidos.append(codificacion_rostro)
            nombres_rostros_conocidos.append(os.path.splitext(filename)[0])
        else:
            print(f"No se encontró ningún rostro en {filename}")

# Inicializar la captura de video
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Preprocesamiento antes del bucle principal
ubicaciones_rostros = []
while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo capturar el fotograma")
        break
    frame = cv2.flip(frame, 1)
    
    # Detectar rostros en el fotograma
    ubicaciones_rostros = face_recognition.face_locations(frame, model="hog")
    if ubicaciones_rostros:
        break

# Bucle principal
while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo capturar el fotograma")
        break
    frame = cv2.flip(frame, 1)
    
    for loc in ubicaciones_rostros:
        codificaciones_rostro = face_recognition.face_encodings(frame, [loc])[0]
        coincidencias = face_recognition.compare_faces(codificaciones_rostros_conocidos, codificaciones_rostro)
        nombre = "DESCONOCIDO" if True not in coincidencias else nombres_rostros_conocidos[coincidencias.index(True)]
        top, right, bottom, left = loc
        color = (0, 0, 255) if nombre == "DESCONOCIDO" else (255, 0, 0)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, nombre, (left, bottom + 20), cv2.FONT_HERSHEY_DUPLEX, 0.8, color, 1)

    # Mostrar el fotograma anotado
    cv2.imshow("Fotograma", frame)
    
    # Verificar si se presiona la tecla de salida
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Salir")
        break

# Liberar la captura de video y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()
