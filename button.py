import cv2
import Tkinter as tk
from PIL import Image, ImageTk
import functions

class Button:

	def __init__(self, window, imagePath, x, y, size, num, belong, control):
		print (imagePath, x, y, size, num)
		self.image = cv2.imread(imagePath)
		self.x = x
		self.y = y
		self.size = size
		self.num = num
		self.press = False
		self.visible = False
		self.belong = belong
		self.control = control
		self.label = tk.Button(window, command=self.defaultCallback)

	def defaultCallback(self):
		if self.press==False:
			self.pressed()
			if self.belong.mutual==True:
				self.belong.releaseAll(self.num)
		else:
			self.released()

	def changeBtnView(self):
		img = cv2.resize(self.image, (self.size, self.size), interpolation=cv2.INTER_CUBIC)
		imgtk = functions.opencv2tkinter(img)
		self.label.imgtk = imgtk
		self.label.configure(image=imgtk)
		self.label.place(x = self.x, y = self.y)

	def hide(self):
		if self.visible==True:
			self.label.pack()
			self.label.pack_forget()
			self.visible = False

	def show(self):
		if self.visible==False:
			self.label.pack()
			self.changeBtnView()
			self.visible = True
	
	def pressed(self):
		self.press = True
		self.size -= 20
		self.x += 10
		self.y += 10
		if self.num!=-1:
			if self.belong.array[self.belong.nowPressed].control!=None:
				self.belong.array[self.belong.nowPressed].control.hide()
			if self.control!=None:
				self.control.show()
			self.belong.nowPressed = self.num
		self.changeBtnView()

	def released(self):
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

	def append(self, window, filename, x, y, size, num, control):
		self.num += 1
		self.array.append(Button(window, filename, x, y, size, num, self, control))

	def btnPressState(self):
		state = []
		for btn in self.array:
			if btn.press==True:
				state.append(1)
			else:
				state.append(0)
		return state

	def releaseAll(self, num):
		for i in xrange(self.num):
			if i!=num and self.array[i].press==True:
				self.array[i].released()

	def hide(self):
		for btn in self.array:
			btn.hide()

	def show(self):
		for btn in self.array:
			btn.show()

	def shiftLeft(self):
		if self.first>0:
			self.first -= 1
			for btn in self.array:
				btn.x += 160
				btn.changeBtnView()
		if self.first==0:
			return (True, False)
		elif self.first==self.num-2:
			return (False, True)
		else:
			return (False, False)

	def shiftRight(self):
		if self.first<self.num-2:
			self.first += 1
			for btn in self.array:
				btn.x -= 160
				btn.changeBtnView()
		if self.first==0:
			return (True, False)
		elif self.first==self.num-2:
			return (False, True)
		else:
			return (False, False)

class dirButton:

	def __init__(self, window, imagePath, x, y, size, type, end, labelBtns, controlBtnArrays):
		print (imagePath, x, y, size, type, end)
		self.image = cv2.imread(imagePath)
		self.x = x
		self.y = y
		self.size = size
		self.type = type
		self.end = end
		self.labelBtns = labelBtns
		self.controlBtnArrays = controlBtnArrays
		self.label = tk.Button(window, command=self.defaultCallback)

	def defaultCallback(self):
		index = self.labelBtns.nowPressed
		if index<len(self.controlBtnArrays) and index>=0:
			if self.type=='left':
				LE, RE = self.controlBtnArrays[index].shiftLeft()
				if self.end!=LE:
					self.invert()
				if self.partner.end!=RE:
					self.partner.invert()
			elif self.type=='right':
				LE, RE = self.controlBtnArrays[index].shiftRight()
				if self.end!=RE:
					self.invert()
				if self.partner.end!=LE:
					self.partner.invert()

	def registerPartner(self, btn):
		self.partner = btn

	def invert(self):
		if self.end==True:
			self.end = False
			self.notEndView()
		else:
			self.end = True
			self.endView()

	def show(self):
		self.label.pack()
		if self.end==True:
			self.endView()
		else:
			self.changeBtnView()

	def changeBtnView(self):
		img = cv2.resize(self.image, (self.size, self.size), interpolation=cv2.INTER_CUBIC)
		imgtk = functions.opencv2tkinter(img)
		self.label.imgtk = imgtk
		self.label.configure(image=imgtk)
		self.label.place(x = self.x, y = self.y)

	def endView(self):
		self.size -= 20
		self.x += 10
		self.y += 10
		self.changeBtnView()

	def notEndView(self):
		self.size += 20
		self.x -= 10
		self.y -= 10
		self.changeBtnView()