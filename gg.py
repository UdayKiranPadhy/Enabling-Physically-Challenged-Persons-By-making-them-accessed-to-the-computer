import cv2 as cv
import pyautogui
pyautogui.FAILSAFE = False
import math

DEBUG = False

def nothing(x):
	pass


#Trackbar for threshhold
# cv.namedWindow("Threshold Track Bar")
# cv.createTrackbar("Track Bar","Threshold Track Bar",70,255,nothing)
        # ThreshHold_Value = cv.getTrackbarPos("Track Bar","Threshold Track Bar")

#DataSets
eye_cascade=cv.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
face_cascade=cv.CascadeClassifier('haarcascade_frontalface_alt.xml')

cap=cv.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

while cap.isOpened():
    ret , frame = cap.read()

    if ret:
        frame = cv.flip(frame,1)

        # The reason for this is gray channel is easy to process and is computationally less intensive as it contains only 1-channel of black-white.
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # pass the gray image, reduce the size by 5%, you increase the chance of a matching size with the model for detection is found. 
        # This also means that the algorithm works slower since it is more thorough. You may increase it to as much as 1.4 for faster detection, with the risk of missing some faces altogether. In our case, I have used 1.0485258 as the scaleFactor as this worked perfectly for the image that I was using.
        # Parameter specifying how many neighbors each candidate rectangle should have to retain it. This parameter will affect the quality of the detected faces. Higher value results in fewer detections but with higher quality. 3~6 is a good value for it. In our case, I have taken 6 as the minNeighbors and this has worked perfectly for the image that I have used.
        faces = face_cascade.detectMultiScale(gray,1.05,6,minSize = (30,30))


        #Setting Face frame
        if faces is not None:
    
            for x,y,w,h in faces:

                if DEBUG:
                    cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)

                roi_face = frame[y:y+h, x:x+w]
                roi_face_gray = cv.cvtColor(roi_face,cv.COLOR_BGR2GRAY)

                # We are resizing the Region Of Interest only because of our convenience to see the intermediate result
                if DEBUG:
                    roi_face_resized = cv.resize(roi_face, (540, 540),interpolation=cv.INTER_AREA)
                    cv.imshow("face",roi_face_resized)


                # EYES
                eyes = eye_cascade.detectMultiScale(roi_face_gray,1.05,8)

                # That detects both the eyes so we slice the np array to size 1
                if len(eyes) >1:
                    eyes = eyes[:1]


                for ex,ey,ew,eh in eyes:

                    if DEBUG:
                        cv.rectangle(roi_face,(ex,ey),(ex+ew,ey+eh),(0,255,0),3)

                    roi_eye = roi_face[ey:ey+eh,ex:ex+ew]
                    
                    roi_eye_gray = cv.cvtColor(roi_eye,cv.COLOR_BGR2GRAY)

                    
                    # We are resizing the Region Of Interest only because of our convenience to see the intermediate result
                    roi_eye_resized = cv.resize(roi_eye, (200, 200))

                    cv.imshow("Eye" , roi_eye_resized)



        cv.imshow("Image",frame)

        k = cv.waitKey(1) & 0xFF 
        if k == ord('q'):
            break

cap.release()
cv.destroyAllWindows()