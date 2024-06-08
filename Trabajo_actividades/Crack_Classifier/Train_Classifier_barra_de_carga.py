import cv2
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import joblib
from tqdm import tqdm

# Función para preprocesar la imagen
def preprocess_image(image):
    # Convertir la imagen a escala de grises
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Aplicar desenfoque gaussiano a la imagen
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    # Ecualizar el histograma de la imagen
    equalized_image = cv2.equalizeHist(blurred_image)
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

# Función para procesar imágenes en una carpeta
def process_images_in_folder(folder_path, label):
    features_list = []
    labels = []
    
    # Obtener la lista de archivos de imagen en la carpeta
    image_files = [filename for filename in os.listdir(folder_path) if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
    num_images = len(image_files)
    
    # Barra de progreso para el proceso de carga de imágenes
    with tqdm(desc=f'Cargando imágenes de la carpeta {folder_path}', total=num_images) as pbar:
        for filename in image_files:
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)
            
            if image is not None:
                # Extraer características de la imagen
                with tqdm(desc=f'Extrayendo características de {filename}', position=1, leave=False) as pbar_extract:
                    features = extract_features(image)
                    features_list.append(features)
                    labels.append(label)
                    pbar_extract.update(1)  # Actualizar la barra de progreso interna
                pbar.update(1)  # Actualizar la barra de progreso externa
            else:
                print(f"Warning: No se pudo leer la imagen {filename}")

    return features_list, labels

# Rutas de las carpetas que contienen las imágenes
grietas_folder_path = r'C:\Users\Daniel Calderon\Desktop\2024-1 Poli\Vision por computador\Trabajo_actividades\Crack_Classifier\Positive'
sin_grietas_folder_path = r'C:\Users\Daniel Calderon\Desktop\2024-1 Poli\Vision por computador\Trabajo_actividades\Crack_Classifier\Negative'

# Procesar las imágenes de grietas y sin grietas con una barra de carga
grietas_features, grietas_labels = process_images_in_folder(grietas_folder_path, 1)
sin_grietas_features, sin_grietas_labels = process_images_in_folder(sin_grietas_folder_path, 0)

# Combinar características y etiquetas de grietas y sin grietas
all_features = np.vstack((grietas_features, sin_grietas_features))
all_labels = np.hstack((grietas_labels, sin_grietas_labels))

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(all_features, all_labels, test_size=0.2, random_state=42)

# Crear y entrenar el clasificador SVM con una barra de carga
with tqdm(desc='Entrenando modelo SVM', total=1) as pbar:
    svm = SVC(kernel='linear', C=1)
    svm.fit(X_train, y_train)
    pbar.update(1)  # Actualizar la barra de progreso

# Guardar el modelo entrenado en un archivo
model_filename = 'svm_crack_classifier.pkl'
joblib.dump(svm, model_filename)
print(f"Modelo guardado en {model_filename}")

# Realizar predicciones
y_pred = svm.predict(X_test)

# Evaluar el modelo
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Mostrar el reporte de clasificación
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
