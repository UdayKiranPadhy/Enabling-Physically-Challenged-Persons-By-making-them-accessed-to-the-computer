import cv2 as cv
import pyautogui
import math

def nothing(x):
	pass
cv.namedWindow("threshtb")
cv.createTrackbar("tb","threshtb",70,255,nothing)
face_cascade=cv.CascadeClassifier('haarcascade_frontalface_alt.xml')
cap=cv.VideoCapture(0)
# ret,frame1=cap.read()
# gray1=cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)


while (True):
	
	ret, frame=cap.read()
	frame=cv.flip(frame, 1)


	till=False
	gray=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	face=face_cascade.detectMultiScale(gray)
	(x1,y1,w1,h1) =face[0]
	tb=cv.getTrackbarPos("tb", "threshtb")
	cv.rectangle(frame, (x1,y1), (x1+w1,y1+h1), (255,0,0),3)
	roi_fac=frame[y1:y1+h1, x1:x1+w1]
	cv.imshow("face", roi_fac)
	_,roi_face_thresh=cv.threshold(cv.cvtColor(roi_fac,cv.COLOR_BGR2GRAY),tb , 255, cv.THRESH_BINARY)
	cv.imshow("Face thresh", roi_face_thresh)


	x_cord,y_cord,_=roi_fac.shape

	





	face_half=roi_fac[int(x_cord/2):x_cord,:]
	x_cord,y_cord,_=face_half.shape
	beard=face_half[int(x_cord/2):x_cord,:]
	# cv.imshow("Bread", bread)
	beard_gray=cv.cvtColor(beard, cv.COLOR_BGR2GRAY)
	
	_,beard_thresh=cv.threshold(beard_gray, tb, 255, cv.THRESH_BINARY_INV)
	cv.imshow("Beard Thresh",beard_thresh)
	cont_beard,_=cv.findContours(beard_thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
	area=0
	for i in cont_beard:
		area+=cv.contourArea(i)

	if area < 4000:
		pyautogui.scroll(20)
		print("Scrolling due to bread")
		till=True








	forehead=roi_fac[:int(x_cord/4),:]
	forehead_gray=cv.cvtColor(forehead, cv.COLOR_BGR2GRAY)
	tb=cv.getTrackbarPos("tb", "threshtb")
	_,forehead_thresh=cv.threshold(forehead_gray, tb, 255, cv.THRESH_BINARY)
	cv.imshow("forehead Thresh",forehead_thresh)
	cont_forehead,_=cv.findContours(forehead_thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
	area=0
	for i in cont_forehead:
		area+=cv.contourArea(i)

	if (area > 3100 and area <3200) and till==False:
		pyautogui.scroll(-20)
		print(area)
		print("Scrolling due to forehead")





	

	if cv.waitKey(1) == ord('q'):
		break


cap.release()
cv.destroyAllWindows()