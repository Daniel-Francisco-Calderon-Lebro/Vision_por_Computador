import cv2
import numpy as np

# Cargar la imagen
imagen = cv2.imread('Reconocimiento_Facial/basededatos/Daniel_Calderon_Actual.jpg')

imagen = cv2.resize(imagen, (720, 640))
# Verificar si la imagen se ha cargado correctamente
if imagen is None:
    print("Error: No se pudo cargar la imagen.")
    exit(1)

# Convertir la imagen a escala de grises
imagen_gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Mostrar la imagen en escala de grises
#cv2.imshow("imagen_gray", imagen_gray)

# Recorrer la imagen con una ventana de 48x48
ventana = np.zeros((24, 24), np.uint8)
filtro_Prewitt1 = np.array([[1,1,1],
                            [0,0,0]])

filtro_Prewitt2 = np.array([[0,0,0],
                            [1,1,1]])
                            
filtro_Prewitt3 = np.array([[1,0,1],
                            [1,0,1]])

filtro_Prewitt4 = np.array([[0,1,0],
                            [0,1,0]])


for i in range(0, imagen_gray.shape[0], ventana.shape[0]):
    for j in range(0, imagen_gray.shape[1], ventana.shape[1]):
        # Obtener la región de interés de la imagen
        roi = imagen_gray[i:i + ventana.shape[0], j:j + ventana.shape[1]]
        # Aplicar el operador Laplaciano a la región de interés
        filtro = cv2.filter2D(roi, cv2.CV_64F, filtro_Prewitt2) - cv2.filter2D(roi, cv2.CV_64F, filtro_Prewitt1) + cv2.filter2D(roi, cv2.CV_64F, filtro_Prewitt4) - cv2.filter2D(roi, cv2.CV_64F, filtro_Prewitt3)
        # Asignar el resultado de Laplacian a la región correspondiente de la imagen
        imagen_gray[i:i + ventana.shape[0], j:j + ventana.shape[1]] = filtro
        th=90
        # Convertir la imagen a binaria
        _, imagen_gray[i:i + ventana.shape[0], j:j + ventana.shape[1]] = cv2.threshold(roi, th, 255, cv2.THRESH_BINARY)        
        # Dibujar la ventana en la imagen
        cv2.rectangle(imagen_gray, (j, i), (j + ventana.shape[1], i + ventana.shape[0]), (0, 255, 0), 2)
        # Mostrar la imagen
        cv2.namedWindow("imagen_gray", cv2.WINDOW_NORMAL)
        cv2.imshow("imagen_gray", imagen_gray)
        # Delay for 10 milliseconds
        cv2.waitKey(10)

# Esperar a que el usuario presione una tecla y luego cerrar las ventanas
cv2.waitKey(0)
cv2.destroyAllWindows()
