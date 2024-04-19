
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
        super().__init__()
        self.frame = []
        self.ubicaciones_rostros = []

    def run(self):
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

reconocimiento.capturar_rostros_conocidos_basededatos("Reconocimiento_Facial\\basededatos")
# print(reconocimiento.nombres_rostros_conocidos)
# print(reconocimiento.codificaciones_rostros_conocidos)

while True:
    reconocimiento().run()
    print("Ubicaciones de los rostros: ",reconocimiento.detectar_ubicacion_rostro())