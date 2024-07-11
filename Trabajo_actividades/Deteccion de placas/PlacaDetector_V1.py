import cv2
import pytesseract

# Especificar la ruta completa a tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Cargar la imagen
image_path = r'C:\Users\Daniel Calderon\Desktop\2024-1 Poli\Vision por computador\Trabajo_actividades\Deteccion de placas\auto003.jpg'
frame = cv2.imread(image_path)

# Convertir a escala de grises
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Aplicar desenfoque gaussiano
gray = cv2.GaussianBlur(gray, (1, 1), 0)

# Detección de bordes usando Canny
edges = cv2.Canny(gray, 100, 200)

# Dilatación para unir posibles discontinuidades en los bordes
#edges = cv2.dilate(edges, None, iterations=2)
#edges = cv2.erode(edges, None, iterations=1)

# Encontrar contornos
contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
    area = cv2.contourArea(c)
    x, y, w, h = cv2.boundingRect(c)
    epsilon = 0.02 * cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, epsilon, True)

    if len(approx) == 4 and 1 < area < 40000:
        aspect_ratio = float(w) / h
        if 2 < aspect_ratio < 5:  # Relación de aspecto típica de una placa
            cv2.drawContours(frame, [approx], 0, (0, 255, 0), 3)
            placa = frame[y:y + h, x:x + w]
            
            # Mostrar la placa extraída
            cv2.imshow('Placa', placa)
            cv2.waitKey(0)
            
            # Aplicar OCR para extraer el texto de la placa
            text = pytesseract.image_to_string(placa, config='--psm 11')
            print('Placa detectada:', text)
            
            # Mostrar el texto en la imagen copiada
            cv2.putText(frame, text.strip(), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

# Mostrar las imágenes resultantes
cv2.imshow('Bordes', edges)
cv2.imshow('Deteccion de Placas', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
