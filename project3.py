import cv2 as cv
import pyautogui
import math


area_left=[]
area_right=[]
eye_cascade=cv.CascadeClassifier('haarcascade_eye.xml')
cap=cv.VideoCapture(0)
count=0
ret,frame1=cap.read()
gray1=cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
eyes=eye_cascade.detectMultiScale(gray1,flags=1)


while (True):
	ret, frame=cap.read()
	frame=cv.flip(frame, 1)

	gray=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	
	(x,y,w,h) =eyes[0]
	cv.rectangle(frame, (x,y), (x+w,y+h), (255,0,0),3)
	roi_gray=gray[y:y+h, x:x+w]
	roi_color=frame[y:y+h, x:x+w]
	
	#Appling types of blur
	blur=cv.GaussianBlur(roi_gray, (3,3), 5)
	# blur=cv.blur(roi_gray, (5,5))
	_,thresh=cv.threshold(blur, 70, 255, cv.THRESH_BINARY_INV)
	
	#Appling filter
	# thresh=cv.medianBlur(thresh, 5)
	# thresh=cv.bilateralFilter(thresh, 9, 75, 75)


	up=thresh.copy()
	lr=cv.pyrUp(up)
	lr=cv.pyrUp(lr)
	cv.imshow("pyrUp", lr)




	median=cv.medianBlur(lr, 5)
	median=cv.medianBlur(lr, 5)
	median=cv.medianBlur(lr, 5)
	for i in range(10):
		gau=cv.filter2D(median, -1, (3,3))

	cv.imshow("2d filter", gau)
	con,_=cv.findContours(gau, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	for cont in con:
		cv.drawContours(gau, cont, -1,(0,255,0),thickness=5)
	cv.imshow("gau", gau)
	if len(con)==2:
		print("pyautogui.click()")
	else:
		pass

	

	

	#To move mouse left and right
	x_dim,y_dim=thresh.shape
	left_img=thresh[:,:int(y_dim/2)]
	right_img=thresh[:,int(y_dim/2):y_dim]

	conturs1,hierachy=cv.findContours(left_img, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
	conturs2,hierachy2=cv.findContours(right_img, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

	max_area_left=-1
	for contur1 in conturs1:
		area=cv.contourArea(contur1)
		if len(area_left)<10:
			area_left.append(area)
		if len(area_left)>10:
			area_left.pop()
			area_left.insert(0,area)
		if area > max_area_left:
			max_area_left=area

	#code for averagr
	num=0
	summation=0
	for i in area_left:
		summation+=i
		num+=1
	if (num>0):
		average_left=summation/num

	if len(area_left)>20:
		area_left.clear()

	if len(area_right)>20:
		area_right.clear()

	max_area_right=-1
	for contur2 in conturs2:
		area=cv.contourArea(contur2)
		if len(area_right)<10:
			area_right.append(area)
		if len(area_right)>10:
			area_right.pop()
			area_right.insert(0,area)
		if area>max_area_right:
			max_area_right=area

	#code for averagr
	num=0
	summation=0
	for i in area_right:
		summation+=i
		num+=1
	average_right=summation/num

	average=math.sqrt((average_right-average_left)**2)

	if ((max_area_left > max_area_right) and ((max_area_left - max_area_right)>(average/2))):
		print("The mouse is moving left and the values are"+str(max_area_left)+"and"+str(max_area_right))
		pyautogui.moveRel(-5,None)
	if (max_area_left<max_area_right) and ((max_area_right-max_area_left)>(average/2)) :
		pyautogui.moveRel(5,None)
		print("The mouse is moving right and the values are"+str(max_area_left)+"and"+str(max_area_right))
	count+=1


		

	#To move mouse top and bottom
	# x_dim,y_dim=thresh.shape
	# top_img=thresh[ : int(x_dim/2), : ]
	# bottom_img=thresh[int(x_dim/2):x_dim, : ]

	# conturs3,hierachy=cv.findContours(top_img, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
	# conturs4,hierachy2=cv.findContours(bottom_img, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

	# max_area_top=-1
	# for contur3 in conturs3:
	# 	area=cv.contourArea(contur3)
	# 	if area > max_area_top:
	# 		max_area_top=area
	# max_area_bottom=-1
	# for contur4 in conturs4:
	# 	area=cv.contourArea(contur4)
	# 	if area>max_area_bottom:
	# 		max_area_bottom=area

	# if max_area_top>max_area_bottom :
	# 	pyautogui.moveRel(None,10)
	# if max_area_top<max_area_bottom:
	# 	pyautogui.moveRel(None,-10)




	cv.imshow("thresh",thresh)
	cv.imshow("image",frame)


	if cv.waitKey(1) == ord('q'):
		break


cap.release()
cv.destroyAllWindows()