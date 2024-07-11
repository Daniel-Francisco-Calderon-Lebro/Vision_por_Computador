# Detector de placas

import cv2
import pytesseract

placa = []

frame = cv2.imread(r'C:\Users\Daniel Calderon\Desktop\2024-1 Poli\Vision por computador\Trabajo_actividades\Deteccion de placas\auto001.jpg')
framecopy = frame.copy()
#frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
frame = cv2.blur(frame, (3, 3))#valor 3x3
frame = cv2.Canny(frame, 150, 200)
frame = cv2.dilate(frame, None, iterations=1)
#encontramos los contornos
contours, hierarchy = cv2.findContours(frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#dibuja los contornos
cv2.drawContours(frame, contours, -1, (255,0,0), 1)

for c in contours:
    area = cv2.contourArea(c)
    print(area)
    x, y, w, h = cv2.boundingRect(c)
    epsilon = 0.1*cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, epsilon, True)

    if len(approx)==4 and area>9000:
        print('area=',area)
        cv2.drawContours(framecopy,[approx],0,(255,0,0),3)

    aspect_ratio = float(w)/h
    print( aspect_ratio )

    if aspect_ratio > 1:
        placa = framecopy[y:y+h, x:x+w]
        # cv2.imshow('placa', placa)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        text = pytesseract.image_to_string(placa, config='--psm 11')
        print('placa=', text)











# #Muestro las 2 iamgenes
# cv2.imshow('frame', frame)
# cv2.imshow('framecopy', framecopy)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

