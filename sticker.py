import numpy as np
import cv2
import math

# detection module
def loadDetectModule():
	face_cascade = cv2.CascadeClassifier('C:/opencv/sources/data/haarcascades/haarcascade_frontalface_alt.xml')
	eye_cascade = cv2.CascadeClassifier('C:/opencv/sources/data/haarcascades/haarcascade_eye_tree_eyeglasses.xml')
	mouth_cascade = cv2.CascadeClassifier('C:/opencv/sources/data/haarcascades/haarcascade_mcs_nose.xml')
	kiss_cascade = cv2.CascadeClassifier('C:/opencv/sources/data/haarcascades/haarcascade_mcs_mouth.xml')
	return (face_cascade, eye_cascade, mouth_cascade, kiss_cascade)

def allSticker(img, choise, face_cascade, eye_cascade, mouth_cascade, kiss_cascade):

	# added pic
	img1 = cv2.imread('image/glasses.png',-1)
	img2 = cv2.imread('image/catnose.png',-1)
	img3 = cv2.imread('image/ear.png',-1)
	img4 = cv2.imread('image/kiss.png',-1)
	img5 = cv2.imread('image/pignose.png',-1)
	img6 = cv2.imread('image/ear1.png',-1)
	img7 = cv2.imread('image/glasses1.png',-1)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

	# face detect
	if choise[0]!=0 or choise[5]!=0 or choise[2]!=0 or choise[6]!=0:
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		
		for (x,y,w,h) in faces:
			roi_gray = gray[y:y+h, x:x+w]

			#add bunny ear
			if choise[2]!=0:
				w3,h3,c3 = img3.shape
				for i in xrange(0,w3):
					for j in xrange(0,h3):
						if img3[i,j][3]!=0:
							img[y+i-int(w*1.1)][x+j-int(h*0.35)]=img3[i][j]
			if choise[5]!=0:
				#add bunny ear1
				print("here:5")
				w6,h6,c6=img6.shape
				img6resize = cv2.resize(img6,(int(w6*0.8),int(h6*0.2)))
				w6,h6,c6=img6resize.shape
				for i in range(0,w6):
					for j in range(0,h6):
						if img6resize[i,j][3]!=0:
							img[y+i-int(w6*0.5)][x+j-int(h6*0.2)]=img6resize[i][j]
			if choise[0]!=0:
				print("here:0")
				#add galsses
				eyes = eye_cascade.detectMultiScale(roi_gray)
				for (ex,ey,ew,eh) in eyes:
					#cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
					img1 = cv2.resize(img1, (w, h))
					w1, h1, c1 = img1.shape
					for i in range(0,w1):
						for j in range(0,h1):
							if img1[i,j][3]!=0:
								img[y+i,x+j]=img1[i,j]
			if choise[6]!=0:
				print("here:6")
				#add galsses1
				eyes = eye_cascade.detectMultiScale(roi_gray)
				for (ex,ey,ew,eh) in eyes:
					#cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
					w7,h7,c7=img7.shape
					img7resize = cv2.resize(img7, (int(w7*0.45), int(h7*0.15)))
					w7, h7, c7 = img7resize.shape
					for i in range(0,w7):
						for j in range(0,h7):
							if img7resize[i,j][3]!=0:
								img[y+i+int(w7*0.5),x+j+int(h7*0.15)]=img7resize[i,j]
				  
	#reverse color map of four channel
	img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
	#bunny nose
	if choise[1]!=0:
		print("here:1")
		mouth = mouth_cascade.detectMultiScale(gray, 1.3, 5)
		ismouth=0
		for (mx, my, mw, mh) in mouth:
			ismouth=1
		if ismouth==1:
			img2resize = cv2.resize(img2,(mw*2,mh*2))   
			w2, h2, c2 = img2resize.shape
			for i in range(-w2/2,w2/2-1):
				for j in range(-h2/2,h2/2-1):
					if img2resize[i+w2/2,j+h2/2][3]!=0:
						img[my+w2/4+i,mx+h2/4+j]=img2resize[i+w2/2,j+h2/2]
	#kiss mouth
	if choise[3]!=0:
		print("here:3")
		mouth = mouth_cascade.detectMultiScale(gray, 1.3, 5)
		ismouth=0
		for (mx, my, mw, mh) in mouth:
			ismouth=1
		if ismouth==1:
			img4resize = cv2.resize(img4,(int(mw*1.3),int(mh*1.3)))   
			w2, h2, c2 = img4resize.shape
			for i in range(0,w2):
				for j in range(0,h2):
					if img4resize[i,j][3]!=0:
						img[my+int(w2*0.5)+i,mx-int(mh*0.2)+j]=img4resize[i,j]
	if choise[4]!=0:
		#print("here:4")
		#pig nose
		mouth = mouth_cascade.detectMultiScale(gray, 1.3, 5)
		ismouth=0
		for (mx, my, mw, mh) in mouth:
			ismouth=1
		if ismouth==1:
			img5resize = cv2.resize(img5,(mw*2,mh*2))   
			w2, h2, c2 = img5resize.shape
			for i in range(-w2/2,w2/2-1):
				for j in range(-h2/2,h2/2-1):
					if img5resize[i+w2/2,j+h2/2][3]!=0:
						img[my+int(w2*0.1)+i,mx+h2/4+j]=img5resize[i+w2/2,j+h2/2]
	return img