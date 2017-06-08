import numpy as np
import cv2

oldTrans = np.array([[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]])

def oldFashion(img):
	height = len(img)
	width = len(img[0])

	BGR = img.reshape([height*width, 3]).T
	newBGR = np.dot(oldTrans, BGR)
	newBGR[newBGR>255] = 255
	newBGR[newBGR<0] = 0
	dst = newBGR.T.reshape([height, width, 3])
	dst = dst.astype(np.uint8)

	return dst
