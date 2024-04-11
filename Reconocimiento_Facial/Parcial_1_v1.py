import face_recognition
import cv2

image = cv2.imread("/home/daniel/Documentos/Vision_por_Computador/Reconocimiento_Facial/basededatos/Daniel_Calderon.jpg")

face_loc = face_recognition.face_locations(image, model="large")[0]
face_imagen_encodings = face_recognition.face_encodings(image,known_face_locations=[face_loc])[0]

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("failed to grab frame")
        break
    frame = cv2.flip(frame, 1)
    face_locations = face_recognition.face_locations(frame, model="small")
    if face_locations != []:
        for loc in face_locations:
            face_frames_encodings = face_recognition.face_encodings(frame, known_face_locations=[loc])[0]
            results = face_recognition.compare_faces([face_frames_encodings], face_imagen_encodings)
            #print("results:", results)
            if results[0] == True:
                text = "DANIEL"
                color = (0, 255, 0)
               
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