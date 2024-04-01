import face_recognition
import cv2

# Cargar la imagen de la cara delknown
known_image = face_recognition.load_image_file("basededatos/WIN_20240324_02_38_16_Pro.jpg")
known_face_encoding = face_recognition.face_encodings(known_image)[0]

# Abrir la cámara
video_capture = cv2.VideoCapture(0)

while True:
    # Capturar un marco de la cámara
    ret, frame = video_capture.read()

    # Convertir el marco a escala de grises para facilitar el reconocimiento facial
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar caras en el marco actualizado
    face_locations = face_recognition.face_locations(gray_frame)

    # Comparar las caras detectadas con la imagen conocida
    face_encodings = face_recognition.face_encodings(gray_frame, face_locations)

    for face_location, face_encoding in zip(face_locations, face_encodings):
        # Verificar si la cara detectada coincide con la imagen conocida
        matches = face_recognition.compare_faces(
            [known_face_encoding], face_encoding
        )

        # Si hay una coincidencia, mostrar un mensaje
        if True in matches:
            top, right, bottom, left = face_location
            name = "Known Face"
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, bottom - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Mostrar el marco actualizado con las detecciones de rostro
    cv2.imshow("Face Recognition", frame)

    # Esperar por el pressionar de una tecla
    key = cv2.waitKey(1)

    # Si se presiona la tecla 'q', salir del bucle
    if key == ord("q"):
        break

# Cerrar la cámara
video_capture.release()
cv2.destroyAllWindows()