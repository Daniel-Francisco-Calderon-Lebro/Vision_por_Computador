import face_recognition
import cv2
import os

image = cv2.imread("Reconocimiento_Facial\\basededatos\\Daniel_Calderon.jpg")


######################################Leer imagenes#############################################
# Ruta al directorio que contiene las imágenes
directorio = 'Reconocimiento_Facial\\basededatos\\'

# Vector para almacenar los nombres de las imágenes
nombres_imagenes = []

# Recorre todos los archivos en el directorio
for filename in os.listdir(directorio):
    # Verifica si el archivo es una imagen
    if filename.endswith('.jpg') or filename.endswith('.png'): # Puedes añadir más extensiones según tus necesidades
        # Agrega el nombre del archivo al vector
        nombres_imagenes.append(filename)

# Imprime el vector con los nombres de las imágenes
print("Nombres de las imágenes en la carpeta:", nombres_imagenes)
######################################Leer imagenes Fin#############################################



#deteccion de rostro con [0] obteniendo el primer rostro devuelve la ubicacion
#cnn es el modelo de deteccion de rostros de m
face_loc = face_recognition.face_locations(image, model="hog")[0]
#imprime el vector de la ubicacion del rostro
#print("face_loc:", face_loc)

#Face encoding genera un vector de caracteristicas de 128 elementos
face_imagen_encodings = face_recognition.face_encodings(image,known_face_locations=[face_loc])[0]
#Imprime el vector de caracteristicas para despues comparar 
#print("face_imagen_encodings:", face_imagen_encodings)


#Dibujo del rectangulo alrededor del rostro encontrado
"""
cv2.rectangle(image, (face_loc[3], face_loc[0]), (face_loc[1], face_loc[2]), (255, 0, 0), 2)
cv2.imshow("image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if not ret:
        print("failed to grab frame")
        break
    frame = cv2.flip(frame, 1)
    face_locations = face_recognition.face_locations(frame, model="hog")
    if face_locations != []:
        for loc in face_locations:
            face_frames_encodings = face_recognition.face_encodings(frame, known_face_locations=[loc])[0]
            #se compara la imagen encontrada con la imagen de la base de datos
            #si la imagen de la base de datos coincide 
            #se comapara la disancia euclidiana entre la imagen de la base de datos y la imagen encontrada
            results = face_recognition.compare_faces([face_frames_encodings], face_imagen_encodings)
            #print("results:", results)
            if results[0] == True:
                text = "DANIEL"
                color = (0, 255, 0)
                #si la imagen de la base de datos coincide se imprime el nombre del archivo
                
            else:
                text = "UNKNOWN"
                color = (0, 0, 255)
            
            cv2.rectangle(frame, (loc[3], loc[2]), (loc[1], loc[2] + 30), color, -1)
            cv2.rectangle(frame, (loc[3], loc[0]), (loc[1], loc[2]), color, 2)
            cv2.putText(frame, text, (loc[3], loc[2] +20),2,0.8, (255, 255, 255), 2, 1)

    cv2.imshow("frame", frame)
    k = cv2.waitKey(1)
    if k == ord("q"):
        print("quit")
        break
cap.release()
cv2.destroyAllWindows()