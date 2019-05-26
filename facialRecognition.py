#######################################################################################
# BRONTE JUREGNS

#facial recognition and response

# taken from https://github.com/raspberrycoulis/pushover/blob/master/pushover.py for notification request and 
# https://www.hackster.io/mjrobot/real-time-face-recognition-an-end-to-end-project-a10826 


########################################################################################
import urllib, httplib
import cv2
import numpy as np
import os 

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
call_interrupter = urllib2.CallInterrupter()


font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0


# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

while True:

    ret, img =cam.read()
    img = cv2.flip(img, -1) # Flip vertically

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 100):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
             conn = httplib.HTTPSConnection("api.pushover.net:443")
			 conn.request("POST", "/1/messages.json",
			  urllib.urlencode({
    			"token": "KzGDORePKggMaC0QOYAMyEEuzJnyUi",              #API key for app
    			"user": "u7rymcbj8cphiiqqk9b9dfz76m3b9j",               # User key given from app
    			"html": "1",                                # 1 for HTML, 0 to disable
    			"title": "Face Detected!",                # Title of the message
    			"message": "<b>Get/b> out!",     # Content of the message
    			"url": "http://192.068.0.53",               # Link to be included in message
    			"url_title": "View live stream",            # Text for the link
    			"sound": "siren",                           # Define the sound played
  			  }), { "Content-type": "application/x-www-form-urlencoded" })
 			 conn.getresponse()


        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
