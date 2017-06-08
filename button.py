import cv2
import Tkinter as tk
from PIL import Image, ImageTk

class Button:

	def __init__(self, window, imagePath, x, y, size):
		self.image = cv2.imread(imagePath)
		self.x = x
		self.y = y
		self.size = size
		self.press = False
		self.label = tk.Button(window, command=self.callback)

	def callback(self):
		if self.press==False:
			self.press = True
		else:
			self.press = False