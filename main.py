import cv2
import pyfirmata

pin= 2                           #relay connect to pin 2 Arduino
port = 'COM7'                    #select port COM, check device manager
board = pyfirmata.Arduino(port)
 

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
smile_cascade = cv2.CascadeClassifier("haarcascade_smile.xml")

vidCam = cv2.VideoCapture(0)

# vidCam.set(3,1280)
# vidCam.set(4,720)
count = 0
total = 0
smileState = False

while True :
    _, frame = vidCam.read()
    face = face_cascade.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor = 1.3, minNeighbors = 2)
    # for (fx, fy, fw, fh) in face:
    #     cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh), (255, 0, 0), 2)
    smile = smile_cascade.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 1.7, 22)
    
    if len(smile) > 0 and len(face) > 0  :
        value = 1
        cv2.putText(frame, "SMILE", (20, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame, "UNLOCKED", (450, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
        for (sx, sy, sw, sh) in smile :
            cv2.rectangle(frame, (sx, sy), (sx + sw, sy + sh), (0, 255, 0), 2)
        if count > 0 :
            total +=1
        count = 0
    else :
        value = 0
        count += 1
        cv2.putText(frame, "NO SMILE", (20, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, "LOCKED", (450, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
       

    board.digital[pin].write(value)

    cv2.putText(frame, "Count= "+str(total), (220, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
    

    cv2.imshow("Result", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
   

vidCam.release()
cv2.destroyAllWindows()

