import cv2
import numpy as np
import joblib
import os
from tqdm import tqdm

# Cargar el clasificador SVM entrenado
model_filename = 'svm_crack_classifier.pkl'
svm = joblib.load(model_filename)
print(f"Modelo cargado desde {model_filename}")

# Función para preprocesar la imagen
def preprocess_image(image):
    # Convertir la imagen a escala de grises
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Aplicar desenfoque gaussiano a la imagen
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    # Ecualizar el histograma de la imagen
    equalized_image = cv2.equalizeHist(blurred_image)
    # Mostrar la imagen preprocesada
    cv2.imshow('Original', image)
    cv2.imshow('Preprocesada', equalized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return equalized_image

# Función para detectar grietas en la imagen
def detect_cracks(image):
    # Aplicar el detector de bordes Canny a la imagen
    edges = cv2.Canny(image, 50, 150)
    # Aplicar la transformada de Hough para detectar líneas
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)
    return lines

# Función para extraer características de la imagen
def extract_features(image):
    # Preprocesar la imagen
    preprocessed_image = preprocess_image(image)
    # Detectar grietas en la imagen
    lines = detect_cracks(preprocessed_image)
    # Redimensionar la imagen
    resized_image = cv2.resize(preprocessed_image, (224, 224))

    # Parámetros para el descriptor HOG
    winSize = (224, 224)
    blockSize = (32, 32)
    blockStride = (16, 16)
    cellSize = (16, 16)
    nbins = 9
    
    # Calcular el descriptor HOG
    hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)
    h = hog.compute(resized_image)
    
    # Calcular la longitud promedio y máxima de las líneas (si se detectan)
    if lines is not None:
        line_lengths = [np.sqrt((x2 - x1)**2 + (y2 - y1)**2) for x1, y1, x2, y2 in lines[:, 0]]
        avg_length = np.mean(line_lengths)
        max_length = np.max(line_lengths)
    else:
        avg_length = 0
        max_length = 0
    
    # Concatenar el descriptor HOG con las longitudes de las líneas
    return np.hstack((h.ravel(), avg_length, max_length))

# Ruta de la carpeta con imágenes de prueba
test_images_folder_path = r'C:\Users\Daniel Calderon\Desktop\2024-1 Poli\Vision por computador\Trabajo_actividades\Crack_Classifier\Test_image_folder'

# Procesar las imágenes de prueba con una barra de carga
for filename in tqdm(os.listdir(test_images_folder_path), desc='Procesando imágenes'):
    if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        image_path = os.path.join(test_images_folder_path, filename)
        image = cv2.imread(image_path)
        
        if image is not None:
            features = extract_features(image)
            prediction = svm.predict([features])
            result = "grieta" if prediction == 1 else "sin grieta"
            print(f"La imagen {filename} contiene una {result}.")
        else:
            print(f"Warning: No se pudo leer la imagen {filename}")
