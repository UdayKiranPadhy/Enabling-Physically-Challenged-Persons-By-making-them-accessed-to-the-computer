import cv2 as cv
import pyautogui
pyautogui.FAILSAFE = False
import math

def nothing(x):
	pass

#Declarations
area_left=[]
area_right=[]

#Trackbar for threshhold
cv.namedWindow("threshtb")
cv.createTrackbar("tb","threshtb",70,255,nothing)

#DataSets
eye_cascade=cv.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
face_cascade=cv.CascadeClassifier('haarcascade_frontalface_alt.xml')

cap=cv.VideoCapture(0)

ret, frame1=cap.read()
frame1=cv.flip(frame1, 1)
# gray=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
eyes=eye_cascade.detectMultiScale(frame1,flags=1)

while (True):
	#Declaration for Up and Down
	till=False
	area_beard=0
	max_area_left=-1
	max_area_right=-1

	ret, frame=cap.read()
	frame=cv.flip(frame, 1)
	gray=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

	#Detecting Faces and eyes
	
	face=face_cascade.detectMultiScale(gray)

	#Assigning Values for Boxes
	(x,y,w,h) =eyes[0]
	(x1,y1,w1,h1) =face[0]

	#Getting Track bar pos
	tb=cv.getTrackbarPos("tb", "threshtb")

	#Setting Face frame
	cv.rectangle(frame, (x1,y1), (x1+w1,y1+h1), (255,0,0),3)
	roi_face=frame[y1:y1+h1, x1:x1+w1]
	_,roi_face_thresh=cv.threshold(cv.cvtColor(roi_face,cv.COLOR_BGR2GRAY),tb , 255, cv.THRESH_BINARY)
	x_cord,y_cord,_=roi_face.shape

	#Seeting Eyes frame
	cv.rectangle(frame, (x,y), (x+w,y+h), (255,0,0),3)
	roi_eye_gray=gray[y:y+h, x:x+w]
	roi_eye_color=frame[y:y+h, x:x+w]
	# roi_eye_blur=cv.GaussianBlur(roi_eye_gray, (3,3), 5)
	_,roi_eye_thresh=cv.threshold(roi_eye_gray, tb, 255, cv.THRESH_BINARY_INV)


	#Showing eyes
	up=roi_eye_thresh.copy()
	lr=cv.pyrUp(up)
	lr=cv.pyrUp(lr)


	#For Detecting Eye Click (Shape)
	# median=cv.medianBlur(lr, 5)
	# median=cv.medianBlur(lr, 5)
	# median=cv.medianBlur(lr, 5)
	# for i in range(10):
	# 	roi_eye_thresh_2dfilter=cv.filter2D(median, -1, (3,3))
	# ct,_=cv.findContours(roi_eye_thresh_2dfilter,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
	# for cn in ct:
	# 	approx=cv.approxPolyDP(cn,0.01*cv.arcLength(cn,True),True)
	# cv.imshow("2d filter", roi_eye_thresh_2dfilter)
	# con,_=cv.findContours(roi_eye_thresh_2dfilter, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	# if len(con) == 2 and len(approx) == 10:
	# 	print("pyautogui.click()")


	#Trial 2 For Eye Click (Based on Face Turning)

	


	#For Scrolling Purpose
	# roi_face_half=roi_face[int(x_cord/2):x_cord,:]
	# """The 3rd parameter is for adustig argument passing values"""
	# x_cord,y_cord,_=roi_face_half.shape
	# roi_beard=roi_face_half[int(x_cord/2):x_cord,:]
	# roi_beard_gray=cv.cvtColor(roi_beard, cv.COLOR_BGR2GRAY)
	# _,roi_beard_thresh=cv.threshold(roi_beard_gray, tb, 255, cv.THRESH_BINARY_INV)
	# contour_beard,_=cv.findContours(roi_beard_thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
	# for i in contour_beard:
	# 	area_beard+=cv.contourArea(i)

	# if area_beard < 4000:
	# 	pyautogui.scroll(20)
	# 	print("Scrolling due to bread")
	# 	till=True


	#To move mouse left and right
	"""Dividing eyes into two halfs"""
	x_dim,y_dim=roi_eye_thresh.shape
	left_part_eye=roi_eye_thresh[:,:int(y_dim/2)]
	right_part_eye=roi_eye_thresh[:,int(y_dim/2):y_dim]

	contours_left_part_eye,_=cv.findContours(left_part_eye, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
	contours_right_part_eye,_=cv.findContours(right_part_eye, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

	for contour in contours_left_part_eye:
		area=cv.contourArea(contour)
		if len(area_left)<10:
			area_left.append(area)
		else:
			area_left.pop()
			area_left.insert(0,area)
		if area > max_area_left:
			max_area_left=area
	#code for average
	num=0
	summation=0
	for i in area_left:
		summation+=i
		num+=1
	if num==0:
		continue
	else:
		average_left=summation/num

	
	for contour in contours_right_part_eye:
		area=cv.contourArea(contour)
		if len(area_right)<10:
			area_right.append(area)
		if len(area_right)>10:
			area_right.pop()
			area_right.insert(0,area)
		if area>max_area_right:
			max_area_right=area
	num=0
	summation=0
	for i in area_right:
		summation+=i
		num+=1
	if num == 0:
		continue
	else:
		average_right=summation/num

	average=math.sqrt((average_right-average_left)**2)

	if ((max_area_left > max_area_right) and ((max_area_left - max_area_right)>(average/2))):
		print("The mouse is moving left and the values are"+str(max_area_left)+"and"+str(max_area_right))
		pyautogui.moveRel(-5,None)
	if (max_area_left<max_area_right) and ((max_area_right-max_area_left)>(average/2)) :
		pyautogui.moveRel(5,None)
		print("The mouse is moving right and the values are"+str(max_area_left)+"and"+str(max_area_right))




	# #Scrollinf Due to forehead
	# roi_forehead=roi_face[:int(x_cord/4),:]
	# roi_forehead_gray=cv.cvtColor(roi_forehead, cv.COLOR_BGR2GRAY)
	# _,roi_forehead_thresh=cv.threshold(roi_forehead_gray, tb, 255, cv.THRESH_BINARY)
	# contours_roi_forehead_forehead,_=cv.findContours(roi_forehead_thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
	# area=0
	# for i in contours_roi_forehead_forehead:
	# 	area+=cv.contourArea(i)

	# if area < 3251 and till==False:
	# 	pyautogui.scroll(-20)
	# 	print(area)
	# 	print("Scrolling due to forehead")



	#Displaying Image Boxes
	cv.imshow("Original Face",frame)
	# cv.imshow("face", roi_face)
	cv.imshow("Face thresh", roi_face_thresh)
	cv.imshow("Eye pyrUp Image", lr)
	# cv.imshow("Bread", roi_bread)
	# cv.imshow("Beard Thresh",roi_beard_thresh)
	# cv.imshow("forehead Thresh",roi_forehead_thresh)




	if cv.waitKey(1) == ord('q'):
		break


cap.release()
cv.destroyAllWindows()