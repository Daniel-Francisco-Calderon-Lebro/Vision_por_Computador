import os
import face_recognition
import cv2
import threading

def cargar_codificaciones(ruta_carpeta):
    codificaciones_rostros_conocidos = []
    nombres_rostros_conocidos = []

    for filename in os.listdir(ruta_carpeta):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            ruta_imagen = os.path.join(ruta_carpeta, filename)
            imagen = face_recognition.load_image_file(ruta_imagen)
            codificaciones_rostro = face_recognition.face_encodings(imagen, model="hog")
            
            if len(codificaciones_rostro) > 0:
                codificacion_rostro = codificaciones_rostro[0]
                codificaciones_rostros_conocidos.append(codificacion_rostro)
                nombres_rostros_conocidos.append(os.path.splitext(filename)[0])
            else:
                print(f"No se encontró ningún rostro en {filename}")
    
    return codificaciones_rostros_conocidos, nombres_rostros_conocidos

def procesar_frame(frame, codificaciones_rostros_conocidos, nombres_rostros_conocidos):
    frame = cv2.flip(frame, 1)
    ubicaciones_rostros = face_recognition.face_locations(frame, model="hog")
    
    if ubicaciones_rostros:
        for loc in ubicaciones_rostros:
            codificaciones_rostro = face_recognition.face_encodings(frame, [loc])[0]
            coincidencias = face_recognition.compare_faces(codificaciones_rostros_conocidos, codificaciones_rostro)
            
            nombre = "DESCONOCIDO"
            if True in coincidencias:
                indice_primera_coincidencia = coincidencias.index(True)
                nombre = nombres_rostros_conocidos[indice_primera_coincidencia]
            
            top, right, bottom, left = loc
            color = (0, 0, 255)
            if nombre != "DESCONOCIDO":
                color = (255, 0, 0)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, nombre, (left, bottom + 20), cv2.FONT_HERSHEY_DUPLEX, 0.8, color, 1)
    
    cv2.imshow("Reconocimiento facial", frame)

if __name__ == "__main__":
    ruta_carpeta = "Reconocimiento_Facial\\basededatos"
    codificaciones_rostros_conocidos, nombres_rostros_conocidos = cargar_codificaciones(ruta_carpeta)
    
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo capturar el fotograma")
            break
        
        # Crear un hilo para procesar el fotograma
        thread = threading.Thread(target=procesar_frame, args=(frame, codificaciones_rostros_conocidos, nombres_rostros_conocidos))
        thread.start()
        
        # Mostrar el fotograma original
        cv2.imshow("Video original", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Salir")
            break
    
    cap.release()
    cv2.destroyAllWindows()
