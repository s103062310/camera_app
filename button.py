import cv2
import Tkinter as tk
from PIL import Image, ImageTk
import functions

class Scale:

	def __init__(self, window, x, y, length, showForever, value, name, var):
		self.x = x
		self.y = y
		self.var = var;
		self.initialValue = value[2]
		self.var.set(self.initialValue)
		self.visible = False
		self.showForever = showForever
		self.text = tk.Label(window, text=name)
		self.label = tk.Scale(window, length=length, from_=value[0], to=value[1], resolution=value[3], variable=var, orient=tk.HORIZONTAL)

	def hide(self):
		if self.visible==True:
			self.label.pack()
			self.text.pack()
			self.label.pack_forget()
			self.text.pack_forget()
			self.visible = False

	def show(self):
		if self.visible==False:
			self.label.pack()
			self.text.pack()
			self.changeBtnView()
			self.visible = True

	def changeBtnView(self):
		self.label.place(x = self.x, y = self.y)
		self.text.place(x = self.x-90, y = self.y+20)

	def reset(self):
		self.var.set(self.initialValue)
		if self.showForever==False:
			self.hide()

class ScaleArray:

	def __init__(self):
		self.array = []

	def append(self, window, x, y, length, showForever, value, name, var):
		self.array.append(Scale(window, x, y, length, showForever, value, name, var))

	def hide(self):
		for scale in self.array:
			scale.hide()

	def show(self):
		for scale in self.array:
			scale.show()

	def reset(self):
		for scale in self.array:
			scale.reset()

class Button:

	def __init__(self, window, imagePath, x, y, size, num, showForever, belong):
		self.image = cv2.imread(imagePath)
		self.x = x
		self.y = y
		self.init_x = x
		self.init_y = y
		self.size = size
		self.num = num
		self.press = False
		self.visible = False
		self.showForever = showForever
		self.belong = belong
		self.control = []
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
			for obj in self.belong.array[self.belong.nowPressed].control:
				if obj!=None:
					obj.hide()
			self.belong.nowPressed = self.num
			for obj in self.control:
				if obj!=None:
					obj.show()
		self.changeBtnView()

	def released(self):
		self.press = False
		self.size += 20
		self.x -= 10
		self.y -= 10
		self.changeBtnView()

	def reset(self):
		if self.press==True:
			self.released()
		if self.showForever==False:
			self.hide()
		self.x = self.init_x
		self.y = self.init_y

	def appendControl(self, obj):
		self.control.append(obj)

class ButtonArray:

	def __init__(self, mutual):
		self.array = []
		self.num = 0
		self.mutual = mutual
		self.nowPressed = -1
		self.first = 0

	def append(self, window, filename, x, y, size, num, showForever):
		self.num += 1
		self.array.append(Button(window, filename, x, y, size, num, showForever, self))

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

	def reset(self):
		self.nowPressed = -1
		self.first = 0
		for btn in self.array:
			btn.reset()

class dirButton:

	def __init__(self, window, imagePath, x, y, size, end, type, labelBtns, controlBtnArrays):
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
		if index<2 and index>=0:
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

	def hide(self):
		pass

	def show(self):
		self.label.pack()
		self.changeBtnView()
		index = self.labelBtns.nowPressed
		if index==-1 or index==2:
			if self.end==False:
				self.invert()
		else:
			if self.type=='left':
				if self.end==False and self.controlBtnArrays[index].first==0:
					self.invert()
				elif self.end==True and self.controlBtnArrays[index].first!=0:
					self.invert()
			elif self.type=='right':
				if self.end==False and self.controlBtnArrays[index].first==self.controlBtnArrays[index].num-2:
					self.invert()
				elif self.end==True and self.controlBtnArrays[index].first!=self.controlBtnArrays[index].num-2:
					self.invert()

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

	def reset(self):
		if self.type=='left' and self.end!=True:
			self.invert()
		elif self.type=='right' and self.end!=False:
			self.invert()