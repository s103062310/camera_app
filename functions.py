import cv2
from PIL import Image, ImageTk

def opencv2tkinter(src):
	dst = cv2.cvtColor(src, cv2.COLOR_BGR2RGBA)
	dst = Image.fromarray(dst)
	dst = ImageTk.PhotoImage(image=dst)
	return dst

