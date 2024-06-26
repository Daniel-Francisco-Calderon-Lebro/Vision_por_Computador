import face_recognition
import cv2
import os

# Ruta al video de entrada
input_video_path = "input_video.mp4"

# Cargar el video
cap = cv2.VideoCapture(input_video_path)

# Definir el codec y crear el objeto VideoWriter para el video de salida
output_filename = 'output_video.avi'
codec = 'XVID'
fps = 30  # Puedes ajustar este valor según el FPS del video de entrada
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_size = (frame_width, frame_height)
fourcc = cv2.VideoWriter_fourcc(*codec)
out = cv2.VideoWriter(output_filename, fourcc, fps, frame_size)

# Ruta a la carpeta de la base de datos de rostros conocidos
ruta_carpeta = "Reconocimiento_Facial/basededatos"
codificaciones_rostros_conocidos = []
nombres_rostros_conocidos = []

# Cargar y procesar las imágenes de la base de datos
for filename in os.listdir(ruta_carpeta):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        ruta_imagen = os.path.join(ruta_carpeta, filename)
        imagen = face_recognition.load_image_file(ruta_imagen)
        # Cambiar el tamaño de todas las imágenes de la base de datos a 720x640
        #imagen = cv2.resize(imagen, (720, 640))
        codificaciones_rostro = face_recognition.face_encodings(imagen, model="hog")
        
        # Verificar si se detecta un rostro en la imagen
        if codificaciones_rostro:
            codificaciones_rostros_conocidos.append(codificaciones_rostro[0])
            nombres_rostros_conocidos.append(os.path.splitext(filename)[0])
        else:
            print(f"No se encontró ningún rostro en {filename}")

# Procesar cada frame del video
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("No se pudo capturar el fotograma")
        break

    # Detectar rostros en el fotograma
    ubicaciones_rostros = face_recognition.face_locations(frame, model="hog")
    
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
                color = (255, 0, 0)  # Azul para conocidos
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom), (right, bottom + 30), color, -1)
            cv2.putText(frame, nombre, (left + 6, bottom + 20), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)

    # Escribir el frame procesado en el archivo de video de salida
    out.write(frame)

    # Mostrar el fotograma anotado en una ventana que se pueda ampliar
    cv2.namedWindow("Fotograma", cv2.WINDOW_NORMAL)
    cv2.imshow("Fotograma", frame)
    
    # Verificar si se presiona la tecla de salida
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Salir")
        break

# Liberar la captura de video y cerrar todas las ventanas
cap.release()
out.release()
cv2.destroyAllWindows()
