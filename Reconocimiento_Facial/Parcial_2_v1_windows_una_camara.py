import os
import face_recognition
import cv2
# import torch
# import dlib
# device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
# Configurar dlib para usar la GPU
# dlib.DLIB_USE_CUDA = True

# Ruta a la carpeta de la base de datos
ruta_carpeta = "Reconocimiento_Facial/basededatos"
codificaciones_rostros_conocidos = []
nombres_rostros_conocidos = []

# Cargar y procesar las imágenes de la base de datos
for filename in os.listdir(ruta_carpeta):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        ruta_imagen = os.path.join(ruta_carpeta, filename)
        imagen = face_recognition.load_image_file(ruta_imagen)
        # Cambiar el tamaño de todas las imágenes de la base de datos a 720x640
        imagen = cv2.resize(imagen, (720, 640))
        print(imagen.shape)
        codificaciones_rostro = face_recognition.face_encodings(imagen, model="hog")
        
        # Verificar si se detecta un rostro en la imagen
        if len(codificaciones_rostro) > 0:
            codificacion_rostro = codificaciones_rostro[0]
            codificaciones_rostros_conocidos.append(codificacion_rostro)
            nombres_rostros_conocidos.append(os.path.splitext(filename)[0])
        else:
            print(f"No se encontró ningún rostro en {filename}")

# Inicializar la captura de video
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_size = (frame_width, frame_height)

# Definir el codec y crear el objeto VideoWriter
output_filename = 'output_video.avi'
codec = 'XVID'
fps = 6
fourcc = cv2.VideoWriter_fourcc(*codec)
out = cv2.VideoWriter(output_filename, fourcc, fps, frame_size)

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo capturar el fotograma")
        break
    frame = cv2.flip(frame, 1)
    
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
            cv2.putText(frame, nombre, (left + 6, bottom + 20), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)

    # Escribir el frame en el archivo de video
    out.write(frame)

    # Mostrar el fotograma anotado en una ventana que se pueda ampliar
    cv2.namedWindow("Fotograma", cv2.WINDOW_NORMAL)
    cv2.imshow("Fotograma", frame)
    
    # Verificar si se presiona la tecla de salida
    if cv2.waitKey(30) & 0xFF == ord('q'):
        print("Salir")
        break

# Liberar la captura de video y cerrar todas las ventanas
cap.release()
out.release()
cv2.destroyAllWindows()
