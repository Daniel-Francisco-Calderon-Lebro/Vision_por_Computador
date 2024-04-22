import os
import face_recognition
import cv2
import threading

# Función para procesar los cuadros
def procesar_cuadros(cap, codificaciones_rostros_conocidos, nombres_rostros_conocidos):
    # Reducir el tamaño de la imagen para acelerar el procesamiento
    resize_factor = 0.25
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo capturar el fotograma")
            break
        
        # Reducir el tamaño de la imagen
        small_frame = cv2.resize(frame, (0, 0), fx=resize_factor, fy=resize_factor)
        
        # Detectar rostros en el fotograma con el modelo HOG
        ubicaciones_rostros = face_recognition.face_locations(small_frame, number_of_times_to_upsample=1)
        
        if ubicaciones_rostros:
            for loc in ubicaciones_rostros:
                # Escalar las ubicaciones de los rostros al tamaño original de la imagen
                top, right, bottom, left = loc
                top = int(top / resize_factor)
                right = int(right / resize_factor)
                bottom = int(bottom / resize_factor)
                left = int(left / resize_factor)
                
                # Recortar la región de interés de la imagen original
                rostro = frame[top:bottom, left:right]
                
                # Codificar el rostro y compararlo con los rostros conocidos
                codificacion_rostro = face_recognition.face_encodings(rostro)
                if codificacion_rostro:
                    coincidencias = face_recognition.compare_faces(codificaciones_rostros_conocidos, codificacion_rostro[0])
                    nombre = "DESCONOCIDO"
                    if True in coincidencias:
                        indice_primera_coincidencia = coincidencias.index(True)
                        nombre = nombres_rostros_conocidos[indice_primera_coincidencia]
                else:
                    nombre = "DESCONOCIDO"
    
                # Dibujar rectángulo alrededor del rostro y etiquetar con el nombre
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, nombre, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
        
        # Mostrar el fotograma sin bloquear la cámara
        cv2.namedWindow("Fotograma", cv2.WINDOW_NORMAL)
        cv2.imshow("Fotograma", frame)
        
        # Verificar si se presiona la tecla de salida
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Salir")
            break

# Ruta de la carpeta de la base de datos
ruta_carpeta = "Reconocimiento_Facial\\basededatos"

# Cargar imágenes conocidas fuera del bucle principal
imagenes_conocidas = [face_recognition.load_image_file(os.path.join(ruta_carpeta, filename)) for filename in os.listdir(ruta_carpeta) if filename.endswith(".jpg") or filename.endswith(".png")]

# Obtener las codificaciones de los rostros conocidos
codificaciones_rostros_conocidos = [face_recognition.face_encodings(imagen)[0] for imagen in imagenes_conocidas]
nombres_rostros_conocidos = [os.path.splitext(filename)[0] for filename in os.listdir(ruta_carpeta) if filename.endswith(".jpg") or filename.endswith(".png")]

# Inicializar la captura de video
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

# Crear y ejecutar un hilo para procesar los cuadros
hilo_procesamiento = threading.Thread(target=procesar_cuadros, args=(cap, codificaciones_rostros_conocidos, nombres_rostros_conocidos))
hilo_procesamiento.start()

# Esperar a que el hilo de procesamiento termine antes de liberar la captura de video y cerrar todas las ventanas
hilo_procesamiento.join()

# Liberar la captura de video y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()
