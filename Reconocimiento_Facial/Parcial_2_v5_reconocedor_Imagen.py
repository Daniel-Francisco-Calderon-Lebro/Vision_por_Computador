import os
import face_recognition
import cv2

def procesar_imagen_y_anotar_ruta(ruta_imagen_entrada, ruta_imagen_salida):
    # Cargar imagen de entrada
    frame = face_recognition.load_image_file(ruta_imagen_entrada)
    
    # Convertir a BGR para OpenCV
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    # Definir la carpeta de base de datos de rostros conocidos
    ruta_carpeta = "Reconocimiento_Facial\\basededatos"
    codificaciones_rostros_conocidos = []
    nombres_rostros_conocidos = []

    # Cargar y codificar rostros conocidos
    for filename in os.listdir(ruta_carpeta):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            ruta_imagen = os.path.join(ruta_carpeta, filename)
            imagen = face_recognition.load_image_file(ruta_imagen)
            # Redimensionar la imagen de la base de datos
            imagen = cv2.resize(imagen, (720, 640))
            codificaciones_rostro = face_recognition.face_encodings(imagen, model="hog")
            
            if len(codificaciones_rostro) > 0:
                codificacion_rostro = codificaciones_rostro[0]
                codificaciones_rostros_conocidos.append(codificacion_rostro)
                nombres_rostros_conocidos.append(os.path.splitext(filename)[0])
            else:
                print(f"No se encontró ningún rostro en {filename}")

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
            cv2.rectangle(frame, (left, bottom), (right, bottom + 30), color, cv2.FILLED)
            cv2.putText(frame, nombre, (left + 6, bottom + 24), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)

    # Ajustar la ventana para mostrar la imagen en alta resolución
    cv2.namedWindow("Imagen Anotada", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Imagen Anotada", 1920, 1080)
    cv2.imshow("Imagen Anotada", frame)
    cv2.waitKey(0)  # Esperar hasta que se presione una tecla
    cv2.destroyAllWindows()
    
    # Guardar la imagen anotada en alta resolución
    cv2.imwrite(ruta_imagen_salida, frame, [cv2.IMWRITE_JPEG_QUALITY, 100])

# Ejemplo de uso
ruta_imagen_entrada = r"C:\Users\Daniel Calderon\Desktop\2024-1 Poli\Vision por computador\input_image.jpg"
ruta_imagen_salida = r"C:\Users\Daniel Calderon\Desktop\2024-1 Poli\Vision por computador\output_image.jpg"
procesar_imagen_y_anotar_ruta(ruta_imagen_entrada, ruta_imagen_salida)
