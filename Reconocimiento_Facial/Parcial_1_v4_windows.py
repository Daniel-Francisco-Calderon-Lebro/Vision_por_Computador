import os
import face_recognition
import cv2
import concurrent.futures

# Ruta de la carpeta de la base de datos
ruta_carpeta = "Reconocimiento_Facial\\basededatos"

# Cargar imágenes conocidas fuera del bucle principal
imagenes_conocidas = [face_recognition.load_image_file(os.path.join(ruta_carpeta, filename)) for filename in os.listdir(ruta_carpeta) if filename.endswith(".jpg") or filename.endswith(".png")]

# Obtener las codificaciones de los rostros conocidos
codificaciones_rostros_conocidos = [face_recognition.face_encodings(imagen)[0] for imagen in imagenes_conocidas]
nombres_rostros_conocidos = [os.path.splitext(filename)[0] for filename in os.listdir(ruta_carpeta) if filename.endswith(".jpg") or filename.endswith(".png")]

# Inicializar la captura de video
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

def procesar_frame(frame):
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # Detectar rostros en el fotograma
    ubicaciones_rostros = face_recognition.face_locations(frame, model="hog", number_of_times_to_upsample=1)
    
    if ubicaciones_rostros:
        for loc in ubicaciones_rostros:
            codificaciones_rostro = face_recognition.face_encodings(frame, [loc])[0]
            
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
            cv2.rectangle(frame, (loc[3], loc[2]), (loc[1], loc[2] + 30), color, -1)
            cv2.rectangle(frame, (loc[3], loc[0]), (loc[1], loc[2]), color, 2)
            cv2.putText(frame, nombre, (loc[3], loc[2] + 20), 2, 0.7, (255, 255, 255), 1)

    return frame

# Procesar fotogramas en paralelo
while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo capturar el fotograma")
        break
    
    # Procesar fotograma en paralelo
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(procesar_frame, frame)
        frame = future.result()

    # Mostrar el fotograma anotado en una ventana que se pueda ampliar
    cv2.namedWindow("Fotograma", cv2.WINDOW_NORMAL)
    cv2.imshow("Fotograma", frame)
    
    # Verificar si se presiona la tecla de salida
    if cv2.waitKey(1) &0xFF == ord('q'):
        print("Salir")
        break

# Liberar la captura de video y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()
