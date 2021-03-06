import cv2
import numpy as np
from matplotlib import pyplot as plt


# contrast
def Contrast(img,N):
	height = len(img)
	width = len(img[0])
	transformation = np.array([[N, 0.0, 0.0], [0.0, N, 0.0], [0.0, 0.0, N]])

	BGR = img.reshape([height*width, 3]).T
	newBGR = np.dot(transformation, BGR)
	newBGR += 128*(1-N)
	newBGR[newBGR>255] = 255
	newBGR[newBGR<0] = 0
	dst = newBGR.T.reshape([height, width, 3])
	dst = dst.astype(np.uint8)
	return dst

# brightness
def Brightness(img,N):
	height = len(img)
	width = len(img[0])
	transformation = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])

	BGR = img.reshape([height*width, 3]).T
	newBGR = np.dot(transformation, BGR)
	newBGR += N
	newBGR[newBGR>255] = 255
	newBGR[newBGR<0] = 0
	dst = newBGR.T.reshape([height, width, 3])
	dst = dst.astype(np.uint8)
	return dst

# saturation
def Saturation(img,N):
	height = len(img)
	width = len(img[0])
	transformation = np.array([[0.3086*(1.0-N)+N, 0.6094*(1-N), 0.0820*(1-N)], [0.3086*(1.0-N), 0.6094*(1-N)+N, 0.0820*(1-N)], [0.3086*(1.0-N), 0.6094*(1-N), 0.0820*(1-N)+N]])

	BGR = img.reshape([height*width, 3]).T
	newBGR = np.dot(transformation, BGR)
	newBGR[newBGR>255] = 255
	newBGR[newBGR<0] = 0
	dst = newBGR.T.reshape([height, width, 3])
	dst = dst.astype(np.uint8)
	return dst

# filter 1
def Changing_Color1(img):
	height = len(img)
	width = len(img[0])
	N = 2.0
	transformation = np.array([[N, 0.0, 0.0], [0.0, N, 0.0], [0.0, 0.0, N]])

	BGR = img.reshape([height*width, 3]).T
	newBGR = np.dot(transformation, BGR)
	newBGR += 128*(1-N)
	newBGR[newBGR>255] = 255
	newBGR[newBGR<0] = 0
	dst = newBGR.T.reshape([height, width, 3])
	dst = dst.astype(np.uint8)
	img = dst

	transformation = np.array([[1.0, 0.189, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
	BGR = img.reshape([height*width, 3]).T
	newBGR = np.dot(transformation, BGR)
	newBGR[newBGR>255] = 255
	newBGR[newBGR<0] = 0
	dst = newBGR.T.reshape([height, width, 3])
	dst = dst.astype(np.uint8)
	return dst

# filter 2
def Changing_Color2(img):
	height = len(img)
	width = len(img[0])
	N = 2.0
	transformation = np.array([[N, 0.0, 0.0], [0.0, N, 0.0], [0.0, 0.0, N]])

	BGR = img.reshape([height*width, 3]).T
	newBGR = np.dot(transformation, BGR)
	newBGR += 128*(1-N)
	newBGR[newBGR>255] = 255
	newBGR[newBGR<0] = 0
	dst = newBGR.T.reshape([height, width, 3])
	dst = dst.astype(np.uint8)
	img = dst

	transformation = np.array([[1.0, 0.189, 0.0], [0.0, 1.0, 0.0], [0.0, 0.189, 1.0]])
	BGR = img.reshape([height*width, 3]).T
	newBGR = np.dot(transformation, BGR)
	newBGR[newBGR>255] = 255
	newBGR[newBGR<0] = 0
	dst = newBGR.T.reshape([height, width, 3])
	dst = dst.astype(np.uint8)
	return dst

# filter 3
def Changing_Color3(img):
	height = len(img)
	width = len(img[0])
	N = 2.0
	transformation = np.array([[N, 0.0, 0.0], [0.0, N, 0.0], [0.189, 0.189, N]])

	BGR = img.reshape([height*width, 3]).T
	newBGR = np.dot(transformation, BGR)
	newBGR += 128*(1-N)
	newBGR[newBGR>255] = 255
	newBGR[newBGR<0] = 0
	dst = newBGR.T.reshape([height, width, 3])
	dst = dst.astype(np.uint8)
	return dst

# filter 4
def Changing_Color4(img):
	height = len(img)
	width = len(img[0])
	N = 2.0
	transformation = np.array([[N, 0.0, 0.0], [0.0, N, 0.0], [0.0, 0.0, N]])

	BGR = img.reshape([height*width, 3]).T
	newBGR = np.dot(transformation, BGR)
	newBGR += 128*(1-N)
	newBGR += 30
	newBGR[newBGR>255] = 255
	newBGR[newBGR<0] = 0
	dst = newBGR.T.reshape([height, width, 3])
	dst = dst.astype(np.uint8)
	return dst

# filter 5 - old
def OldFashion(img):
	height = len(img)
	width = len(img[0])
	transformation = np.array([[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]])

	BGR = img.reshape([height*width, 3]).T
	newBGR = np.dot(transformation, BGR)
	newBGR[newBGR>255] = 255
	newBGR[newBGR<0] = 0
	dst = newBGR.T.reshape([height, width, 3])
	dst = dst.astype(np.uint8)
	return dst

# filter 6
def Negative(img):
	height = len(img)
	width = len(img[0])
	transformation = np.array([[-1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, -1.0]])

	BGR = img.reshape([height*width, 3]).T
	newBGR = np.dot(transformation, BGR)
	newBGR += 255
	newBGR[newBGR>255] = 255
	newBGR[newBGR<0] = 0
	dst = newBGR.T.reshape([height, width, 3])
	dst = dst.astype(np.uint8)
	return dst

# filter 7 - speed up
def Drawing(img):
	height = len(img)
	width = len(img[0])
	threshold = 5

	if threshold < 0: threshold = 0
	if threshold > 100: threshold = 100
	imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	dstarray = imgray.copy()
	for h in xrange(height):
		for w in xrange(width):
			if w == width-1 or h == height-1:
				continue
			src = imgray[h, w]
			dst = imgray[h+1, w+1]

			diff = abs(int(src) - int(dst))
			if diff >= threshold:
				dstarray[h, w] = 0
			else:
				dstarray[h, w] = 255
	dstarray = cv2.cvtColor(dstarray, cv2.COLOR_GRAY2BGR)
	return dstarray