
import cv2
import os
import face_recognition

#Clase reconocimiento facial multiproceso
class reconocimiento():
    """
    Esta clase es una clase que hereda de la clase Process de la biblioteca multiprocessing.
    """
    codificaciones_rostros_conocidos = []
    nombres_rostros_conocidos = []
    def __init__(self):
        self.frame = []
        self.ubicaciones_rostros = []
        self.nombre = []

    def run_camara(self):
        video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while True:
            ret, self.frame = video.read()
            self.frame = cv2.flip(self.frame, 1)
            if not ret:
                print("No se pudo capturar el fotograma")
                break
            cv2.imshow("Camara", self.frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video.release()
        cv2.destroyAllWindows()

    def detectar_ubicacion_rostro(self):
        """
        Esta función se encarga de detectar la ubicación de un rostro en una imagen.
        """
        self.ubicaciones_rostros = face_recognition.face_locations(self.frame)
        return self.ubicaciones_rostros
    
    def codificar_rostro(self):
        """
        Esta función se encarga de codificar un rostro en una imagen.
        """
        codificaciones_rostro = face_recognition.face_encodings(self.frame, [self.ubicaciones_rostros])[0]
        return codificaciones_rostro
    
    def obtener_coincidencias_rostros(self):
        """
        Esta función se encarga de codificar un rostro en una imagen.
        """
        coincidencias = face_recognition.compare_faces(self.codificaciones_rostros_conocidos, reconocimiento.codificar_rostro())
        self.nombre = "DESCONOCIDO"
        if True in coincidencias:
                indice_primera_coincidencia = coincidencias.index(True)
                self.nombre = self.nombres_rostros_conocidos[indice_primera_coincidencia]
    def dibujar_rectangulo_alrededor_rostro(self):
        """
        Esta función se encarga de codificar un rostro en una imagen.
        """
        for loc in self.ubicaciones_rostros:
            color = (0, 0, 255)  # Rojo para desconocidos
            if self.nombre != "DESCONOCIDO":
                color = (255, 0, 0)  # Verde para conocidos
            cv2.rectangle(self.frame, (loc[3], loc[2]), (loc[1], loc[2] + 30), color, -1)
            cv2.rectangle(self.frame, (loc[3], loc[0]), (loc[1], loc[2]), color, 2)
            cv2.putText(self.frame, self.nombre, (loc[3], loc[2] + 20), 2, 0.7, (255, 255, 255), 1)
    

    @classmethod
    def capturar_rostros_conocidos_basededatos(cls,ruta_carpeta):
            for filename in os.listdir(ruta_carpeta):
                 if filename.endswith(".jpg") or filename.endswith(".png"):
                    ruta_imagen = os.path.join(ruta_carpeta, filename)
                    imagen = face_recognition.load_image_file(ruta_imagen)
                    codificaciones_rostro = face_recognition.face_encodings(imagen, model="hog")
                    
                    # Verificar si se detecta un rostro en la imagen
                    if len(codificaciones_rostro) > 0:
                        codificacion_rostro = codificaciones_rostro[0]
                        cls.codificaciones_rostros_conocidos.append(codificacion_rostro)
                        cls.nombres_rostros_conocidos.append(os.path.splitext(filename)[0])
                    else:
                        print(f"No se encontró ningún rostro en {filename}")

programa_recocnocimiento=reconocimiento()
programa_recocnocimiento.capturar_rostros_conocidos_basededatos("Reconocimiento_Facial\\basededatos")
print("Se han capturado los rostros de la base de datos")
print(programa_recocnocimiento.nombres_rostros_conocidos)
print(programa_recocnocimiento.codificaciones_rostros_conocidos)
programa_recocnocimiento.run_camara()
programa_recocnocimiento.detectar_ubicacion_rostro()
programa_recocnocimiento.codificar_rostro()
programa_recocnocimiento.obtener_coincidencias_rostros()
programa_recocnocimiento.dibujar_rectangulo_alrededor_rostro()

