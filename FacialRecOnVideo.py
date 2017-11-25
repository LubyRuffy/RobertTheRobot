import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier("/usr/local/share/opencv/haarcascades/haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
##out = cv2.VideoWriter("./facialTest1.avi",fourcc,20.0,(640,480))

while(1):
    ret,frame = cap.read()
    print (frame.shape)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
##    faces = face_cascade.detectMultiScale(gray,1.2,5)
##    
##    for(x,y,w,h) in faces:
##        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
##    
##    out.write(frame)    
    cv2.imshow("Video from webcam",frame)
    
    if(cv2.waitKey(25) & 0xFF == ord("q")):
        break

##out.release()    
cap.release()
cv2.destroyAllWindows()
