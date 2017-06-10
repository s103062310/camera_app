import cv2
import numpy as np
import Tkinter as tk
from PIL import Image, ImageTk, ImageGrab
import button


def opencv2tkinter(src):
	dst = cv2.cvtColor(src, cv2.COLOR_BGR2RGBA)
	dst = Image.fromarray(dst)
	dst = ImageTk.PhotoImage(image=dst)
	return dst

def snapshot(src, num):
	filename = 'snapshot/photo' + str(num) + '.jpg'
	cv2.imwrite(filename, src)
	return num + 1

def calOneHotIndex(array):
	index = np.array(range(len(array)))
	index += 1
	return index.dot(array)

def reset(objArray):
	for obj in objArray:
		obj.reset()

def polygon_star(canvas, x, y, p, t, outline, fill, width):
	points = []
	for i in (1, -1):
		points.extend((x, y + i*p))
		points.extend((x + i*t, y + i*t))
		points.extend((x + i*p, y))
		points.extend((x + i*t, y - i * t))
	canvas.create_polygon(points, outline=outline, fill=fill, width=width)

def showImageAndPaint(num):

	# define constant
	windowWidth, windowHeight = 640, 700
	videoWidth, videoHeight = 640, 480
	btnSize = 160
	shift = 10
	penNum = 6

	# create window
	filename = 'snapshot/photo' + str(num) + '.jpg'
	window = tk.Toplevel(width=windowWidth, height=1000)
	window.title(filename)
	window.geometry("640x700")
	window.resizable(0, 0)

	# create canvas
	object = tk.Canvas(window, width=videoWidth, height=videoHeight)
	object.pack()
	src = Image.open(filename)
	src = ImageTk.PhotoImage(src)
	object.image = src
	object.create_image(videoWidth/2, videoHeight/2, image=src)

	# canvas callback
	def paint(event):
		x1, y1 = ( event.x - 3 ), ( event.y - 3 )
		x2, y2 = ( event.x + 3 ), ( event.y + 3 )
		pen = calOneHotIndex(optionBtns.btnPressState())
		if pen==1:		# red
			object.create_oval( x1, y1, x2, y2, outline='red', fill='red', width=2)
		elif pen==2:	# blue
			object.create_oval( x1, y1, x2, y2, outline='blue', fill='blue', width=2)
		elif pen==3:	# blue
			object.create_oval( x1, y1, x2, y2, outline='green', fill='green', width=2)
		elif pen==4:	# star
			polygon_star(object, x1, y1, 9, 2, outline='gold', fill='gold', width=2)
		elif pen==5:	# cross
			polygon_star(object, x1, y1, 5, 0, outline='white', fill='white', width=2)
		elif pen==6:	# tilted cross
			polygon_star(object, x1, y1, 2, 5, outline='white', fill='white', width=2)
		#big square
		#polygon_star(w,x1,y1,9,10,outline='gold',fill='blue', width=2)
		#small square
		#polygon_star(w,x1,y1,3,4,outline='gold',fill='blue', width=2)
	object.bind( "<B1-Motion>", paint)

	# create option btns
	optionBtns = button.ButtonArray(True)
	for i in xrange(penNum):
		filename = 'image/pen' + str(i+1) + '.jpg'
		optionBtns.append(window, filename, btnSize*(i+1)+shift, videoHeight+shift*2+btnSize/4, btnSize-2*shift, i, True, None)
		optionBtns.array[i].show()

	# create function btns
	funcBtns = button.ButtonArray(False)
	funcBtns.nowPressed = 0

	# create direction btns
	leftBtn = button.dirButton(window, 'image/left.jpg', shift, videoHeight+shift*2+btnSize/4, btnSize-shift*2, True, 'left', funcBtns, [optionBtns])
	rightBtn = button.dirButton(window, 'image/right.jpg', btnSize*3+shift, videoHeight+shift*2+btnSize/4, btnSize-shift*2, False, 'right', funcBtns, [optionBtns])
	leftBtn.show()
	rightBtn.show()
	leftBtn.registerPartner(rightBtn)
	rightBtn.registerPartner(leftBtn)

	# create save btn
	def save():
		x = window.winfo_rootx()
		y = window.winfo_rooty()
		filename = 'snapshot/photo' + str(num) + '_paint.jpg'
		ImageGrab.grab().crop((x, y, x+videoWidth, y+videoHeight)).save(filename)
		window.destroy()
	saveBtn = tk.Button(window, command=save)
	img = cv2.imread('image/save.jpg')
	img = cv2.resize(img, (windowWidth-shift*2, btnSize/4), interpolation=cv2.INTER_CUBIC)
	imgtk = opencv2tkinter(img)
	saveBtn.imgtk = imgtk
	saveBtn.configure(image=imgtk)
	saveBtn.pack()
