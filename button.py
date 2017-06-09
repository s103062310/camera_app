import cv2
import Tkinter as tk
from PIL import Image, ImageTk
import functions as fc

class Button:

	def __init__(self, window, imagePath, x, y, size, num, btnArray):
		print (imagePath, x, y, size, num)
		self.image = cv2.imread(imagePath)
		self.x = x
		self.y = y
		self.size = size
		self.num = num
		self.press = False
		self.btnArray = btnArray
		self.label = tk.Button(window, command=self.defaultCallback)

	def defaultCallback(self):
		if self.press==False:
			self.pressed()
			if self.btnArray.mutual==True:
				self.btnArray.releaseAll(self.num)
		else:
			self.released()

	def changeBtnView(self):
		img = cv2.resize(self.image, (self.size, self.size), interpolation=cv2.INTER_CUBIC)
		imgtk = fc.opencv2tkinter(img)
		self.label.imgtk = imgtk
		self.label.configure(image=imgtk)
		self.label.place(x = self.x, y = self.y)

	def hide(self):
		self.label.pack()
		self.label.pack_forget()

	def show(self):
		self.label.pack()
		self.changeBtnView()
	
	def pressed(self):
		print ("press", self.num)
		self.press = True
		self.size -= 20
		self.x += 10
		self.y += 10
		if self.num!=-1:
			self.btnArray.nowPressed = self.num
		self.changeBtnView()

	def released(self):
		print ("released", self.num)
		self.press = False
		self.size += 20
		self.x -= 10
		self.y -= 10
		self.changeBtnView()

class ButtonArray:

	def __init__(self, mutual):
		self.array = []
		self.num = 0
		self.mutual = mutual
		self.nowPressed = -1
		self.first = 0

	def append(self, window, filename, x, y, size, num):
		self.num += 1
		self.array.append(Button(window, filename, x, y, size, num, self))

	def btnPressState(self):
		state = []
		for btn in self.array:
			if btn.press==True:
				state.append(1)
			else:
				state.append(0)
		state.append(self.nowPressed)
		return state

	def releaseAll(self, num):
		for i in xrange(self.num):
			if i!=num:
				if self.array[i].press==True:
					self.array[i].released()

	def hide(self):
		for btn in self.array:
			btn.hide()

	def show(self):
		for btn in self.array:
			btn.show()