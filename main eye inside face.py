import cv2 as cv
import pyautogui
pyautogui.FAILSAFE = False
import math

def nothing(x):
	pass

area_left=[]
area_right=[]
eye_cascade=cv.CascadeClassifier('haarcascade_eye.xml')
cv.namedWindow("threshtb")
cv.createTrackbar("tb","threshtb",70,255,nothing)
face_cascade=cv.CascadeClassifier('haarcascade_frontalface_alt.xml')
cap=cv.VideoCapture(0)
# ret,frame1=cap.read()
# gray1=cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)



while (True):
	ret, frame=cap.read()
	frame=cv.flip(frame, 1)

	gray=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	eyes=eye_cascade.detectMultiScale(frame,flags=1)
	
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




	# median=cv.medianBlur(lr, 5)
	# median=cv.medianBlur(lr, 5)
	# median=cv.medianBlur(lr, 5)
	# for i in range(10):
	# 	gau=cv.filter2D(median, -1, (3,3))

	# ct,_=cv.findContours(gau,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
	# for cn in ct:
	# 	approx=cv.approxPolyDP(cn,0.01*cv.arcLength(cn,True),True)

	# cv.imshow("2d filter", gau)
	# con,_=cv.findContours(gau, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	# for cont in con:
	# 	cv.drawContours(gau, cont, -1,(0,255,0),thickness=5)
	# cv.imshow("gau", gau)
	# if len(con)==2 and len(approx)==10:
	# 	print("pyautogui.click()")
	# else:
	# 	pass

	

	

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
	if num==0:
		continue
	average_left=summation/num


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
		pyautogui.moveRel(-10,None)
	if (max_area_left<max_area_right) and ((max_area_right-max_area_left)>(average/2)) :
		pyautogui.moveRel(10,None)
		print("The mouse is moving right and the values are"+str(max_area_left)+"and"+str(max_area_right))

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

	





	# face_half=roi_fac[int(x_cord/2):x_cord,:]
	# x_cord,y_cord,_=face_half.shape
	# bread=face_half[int(x_cord/2):x_cord,:]
	# # cv.imshow("Bread", bread)
	# bread_gray=cv.cvtColor(bread, cv.COLOR_BGR2GRAY)
	
	# _,bread_thresh=cv.threshold(bread_gray, tb, 255, cv.THRESH_BINARY_INV)
	# cv.imshow("Bread Thresh",bread_thresh)
	# cont_bread,_=cv.findContours(bread_thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
	# area=0
	# for i in cont_bread:
	# 	area+=cv.contourArea(i)
	# print("area covered by beard "+str(area))
	# if area < 4000:
	# 	x,y=pyautogui.position()
	# 	pyautogui.move(x,y-10)
	# 	print("Scrolling due to bread")
	# 	till=True








	# forehead=roi_fac[:int(x_cord/4),:]
	# forehead_gray=cv.cvtColor(forehead, cv.COLOR_BGR2GRAY)
	# tb=cv.getTrackbarPos("tb", "threshtb")
	# _,forehead_thresh=cv.threshold(forehead_gray, tb, 255, cv.THRESH_BINARY)
	# cv.imshow("forehead Thresh",forehead_thresh)
	# cont_forehead,_=cv.findContours(forehead_thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
	# area=0
	# for i in cont_forehead:
	# 	area+=cv.contourArea(i)
	# print("Area covered by forehead "+str(area))
	# if area < 2100 and till==False:
	# 	x,y=pyautogui.position()
	# 	print(area)
	# 	print("Scrolling due to bread")
	# 	pyautogui.move(x,y-10)



	
	cv.imshow("thresh",thresh)
	cv.imshow("image",frame)


	if cv.waitKey(1) == ord('q'):
		break


cap.release()
cv.destroyAllWindows()