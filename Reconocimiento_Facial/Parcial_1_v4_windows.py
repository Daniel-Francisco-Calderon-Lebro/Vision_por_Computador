import os
import face_recognition
import cv2
import threading

# Cargar imágenes desde la carpeta y generar codificaciones
ruta_carpeta = "Reconocimiento_Facial\\basededatos"
codificaciones_rostros_conocidos = []
nombres_rostros_conocidos = []

for filename in os.listdir(ruta_carpeta):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        ruta_imagen = os.path.join(ruta_carpeta, filename)
        imagen = face_recognition.load_image_file(ruta_imagen)
        codificaciones_rostro = face_recognition.face_encodings(imagen, model="hog")
        
        # Verificar si se detecta un rostro en la imagen
        if len(codificaciones_rostro) > 0:
            codificacion_rostro = codificaciones_rostro[0]
            codificaciones_rostros_conocidos.append(codificacion_rostro)
            nombres_rostros_conocidos.append(os.path.splitext(filename)[0])
        else:
            print(f"No se encontró ningún rostro en {filename}")

# Inicializar la captura de video
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
frame = None

def capturar_fotograma():
    global frame
    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo capturar el fotograma")
            break

# Iniciar el hilo para la captura de fotogramas
thread = threading.Thread(target=capturar_fotograma)
thread.daemon = True
thread.start()

while True:
    if frame is not None:
        # Copiar el fotograma capturado para procesarlo
        frame_copy = frame.copy()
        
        # Detectar rostros en el fotograma
        ubicaciones_rostros = face_recognition.face_locations(frame_copy, model="hog")
        
        if ubicaciones_rostros:
            for loc in ubicaciones_rostros:
                codificaciones_rostro = face_recognition.face_encodings(frame_copy, [loc])[0]
                
                # Comparar rostro con rostros conocidos
                coincidencias = face_recognition.compare_faces(codificaciones_rostros_conocidos, codificaciones_rostro)
                
                nombre = "DESCONOCIDO"
                if True in coincidencias:
                    indice_primera_coincidencia = coincidencias.index(True)
                    nombre = nombres_rostros_conocidos[indice_primera_coincidencia]
                
                # Dibujar rectángulo alrededor del rostro y etiquetar con el nombre
                top, right, bottom, left = loc
                color = (0, 0, 255)  # Rojo para desconocidos
                if nombre != "DESCONOCIDO":
                    color = (255, 0, 0)  # Verde para conocidos
                cv2.rectangle(frame_copy, (left, top), (right, bottom), color, 2)
                cv2.putText(frame_copy, nombre, (left, bottom + 20), cv2.FONT_HERSHEY_DUPLEX, 0.8, color, 1)

        # Mostrar el fotograma anotado
        cv2.imshow("Fotograma", frame_copy)

    # Verificar si se presiona la tecla de salida
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Salir")
        break

# Liberar la captura de video y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()
