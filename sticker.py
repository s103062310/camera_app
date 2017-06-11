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

def depart(img):
	h, w, c = img.shape
	img = img.reshape([w*h, c]).T
	dst = []
	for i in xrange(c):
		temp = img[i][:]
		temp = temp.T.reshape([h, w])
		dst.append(temp)
	return dst

def merge(B, G, R):
	h, w = B.shape
	img = np.array([B, G, R]).reshape([3, -1])
	img = img.T.reshape([h, w, 3])
	return img

def expend(img, height, width, x, y):
	h, w = img.shape
	print (x, y)
	img = np.concatenate((np.zeros((x, w)), img), axis=0) # up
	img = np.concatenate((img, np.zeros((height-h-x, w))), axis=0) # down
	img = np.concatenate((np.zeros((height, y)), img), axis=1) # left
	img = np.concatenate((img, np.zeros((height, width-w-y))), axis=1) # right
	return img

def addSmallImage(src, img, x, y, hscale, wscale, threshold):

	# get basic info
	img = cv2.resize(img, (int(img.shape[0]*hscale), int(img.shape[1]*wscale)), interpolation=cv2.INTER_CUBIC)
	height, width, _ = src.shape
	h, w, _ = img.shape

	# depart every channel
	src = depart(src)
	srcB, srcG, srcR = src
	img = depart(img)
	imgB, imgG, imgR, imgA = img

	# produce mask
	imgA[imgA<threshold] = 0
	imgA[imgA>=threshold] = 1

	# expend small image to dst size
	imgB = expend(imgB, height, width, x, y)
	imgG = expend(imgG, height, width, x, y)
	imgR = expend(imgR, height, width, x, y)
	imgA = expend(imgA, height, width, x, y)
	imgAinvert = 1-imgA

	# stick - multiply with mask
	dstB = np.multiply(srcB, imgAinvert) + np.multiply(imgB, imgA)
	dstG = np.multiply(srcG, imgAinvert) + np.multiply(imgG, imgA)
	dstR = np.multiply(srcR, imgAinvert) + np.multiply(imgR, imgA)

	# merge
	dst = merge(dstB, dstG, dstR).astype(np.uint8)
	return dst

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

			#add bunny ear
			if choise[2]!=0:
				#img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
				#w3,h3,c3=img3.shape
				#w3=w3/2
				#h3=h3/2
				#img = addSmallImage(img, img3, int(x+h/2-h3/2), int(y+w/2-w3/2), 0.7, 0.7, 20)
				#img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
				w3,h3,c3 = img3.shape
				for i in xrange(0,w3):
					for j in xrange(-h3/2,h3/2-1):
						if img3[i,j+h3/2][3]!=0:
							img[y+i-int(h*1.05)][x+j+w/2]=img3[i,j+h3/2]
			if choise[5]!=0:
				#add bunny ear1
				#print("here:5")
				w6,h6,c6=img6.shape
				img6resize = cv2.resize(img6,(int(w6*0.8),int(h6*0.2)))
				w6,h6,c6=img6resize.shape
				for i in range(0,w6):
					for j in range(0,h6):
						if img6resize[i,j][3]!=0:
							img[y+i-int(w6*0.5)][x+j-int(h6*0.2)]=img6resize[i][j]
			if choise[0]!=0:
				#print("here:0")
				#add galsses
				roi_gray = gray[y:y+h, x:x+w]
				eyes = eye_cascade.detectMultiScale(roi_gray)
				for (ex,ey,ew,eh) in eyes:
					#cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
					img1 = cv2.resize(img1, (int(w*0.8), int(h*0.8)))
					w1, h1, c1 = img1.shape
					for i in range(0,w1):
						for j in range(0,h1):
							if img1[i,j][3]!=0:
								img[int(y*1.1)+i,int(x*1.1)+j]=img1[i,j]
			if choise[6]!=0:
				#print("here:6")
				#add galsses1
				roi_gray = gray[y:y+h, x:x+w]
				eyes = eye_cascade.detectMultiScale(roi_gray)
				for (ex,ey,ew,eh) in eyes:
					#cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
					#w7,h7,c7=img7.shape
					img7resize = cv2.resize(img7, (int(w*0.7),int(h*0.5)))
					w7, h7, c7 = img7resize.shape
					for i in range(0,w7):
						for j in range(0,h7):
							if img7resize[i,j][3]!=0:
								img[int(y*1.25)+i,int(x*1.15)+j]=img7resize[i,j]
				  
	#reverse color map of four channel
	img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
	#bunny nose
	if choise[1]!=0:
		#print("here:1")
		mouth = mouth_cascade.detectMultiScale(gray, 1.3, 5)
		for (mx, my, mw, mh) in mouth:
			img2resize = cv2.resize(img2,(mw*2,mh*2))   
			w2, h2, c2 = img2resize.shape
			for i in range(-w2/2,w2/2-1):
				for j in range(-h2/2,h2/2-1):
					if img2resize[i+w2/2,j+h2/2][3]!=0:
						img[my+int(mh/2)+i,mx+int(mw/2)+j]=img2resize[i+w2/2,j+h2/2]
	#kiss mouth
	if choise[3]!=0:
		#print("here:3")
		mouth = mouth_cascade.detectMultiScale(gray, 1.3, 5)
		for (mx, my, mw, mh) in mouth:
			img4resize = cv2.resize(img4,(int(mw*1.3),int(mh*1.3)))   
			w2, h2, c2 = img4resize.shape
			for i in range(-w2/2,w2/2-1):
				for j in range(-h2/2,h2/2-1):
					if img4resize[i+w2/2,j+h2/2][3]!=0:
						img[my+int(mh*1.45)+i,mx+int(mw/2)+j]=img4resize[i+w2/2,j+h2/2]
	if choise[4]!=0:
		#print("here:4")
		#pig nose
		mouth = mouth_cascade.detectMultiScale(gray, 1.3, 5)
		for (mx, my, mw, mh) in mouth:
			img5resize = cv2.resize(img5,(int(mw*1.8),int(mh*1.8)))   
			w2, h2, c2 = img5resize.shape
			for i in range(-w2/2,w2/2-1):
				for j in range(-h2/2,h2/2-1):
					if img5resize[i+w2/2,j+h2/2][3]!=0:
						img[my+int(mh/2)+i,mx+int(mw/2)+j]=img5resize[i+w2/2,j+h2/2]
	img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
	return img