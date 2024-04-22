import os
import face_recognition
import cv2
# import dlib

# # Configurar dlib para usar la GPU
# dlib.DLIB_USE_CUDA = True
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

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo capturar el fotograma")
        break
    frame = cv2.flip(frame, 1)
    frame=cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    #print(frame.shape)#480x640 en 1 y 2 camaras
    #frame = cv2.resize(frame, (480, 640))
    #print(frame.shape)
    
    # Detectar rostros en el fotograma
    ubicaciones_rostros = face_recognition.face_locations(frame, model="hog", number_of_times_to_upsample=2)
    
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

    # Mostrar el fotograma anotado en una ventana que se pueda ampliar
    cv2.namedWindow("Fotograma", cv2.WINDOW_NORMAL)
    cv2.imshow("Fotograma", frame)
    
    # Verificar si se presiona la tecla de salida
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Salir")
        break

# Liberar la captura de video y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()
