import cv2
import Tkinter as tk
from PIL import Image, ImageTk

class Button:

	def __init__(self, window, imagePath, x, y, size):
		self.image = cv2.imread(imagePath)
		self.x = x
		self.y = y
		self.size = size
		self.press = 0
		self.label = tk.Button(window, command=self.callback)

	def callback(self):
		if self.press==0:
			self.press = 1
			print 1
		else:
			self.press = 0
			print 0