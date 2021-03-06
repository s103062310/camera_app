import os
import cv2
import Tkinter as tk
from PIL import Image, ImageTk
import functions ,button, filter, sticker


# define constant
windowWidth, windowHeight = 800, 640
videoWidth, videoHeight = 640, 480
adjustNum = 3
funcBtnNum = 4
btnSize = 160
shift = 10
barLength = 200
photoDir = 'snapshot/'
imageDir = 'image/'
barInfo = [[' Contrast ', 'Brightness','Saturation'], [[0.0, 10.0, 1.0, 0.1], [-255.0, 255.0, 0.0, 1.0], [0.0, 2.0, 1.0, 0.01]]]
btnInfo = [['filter', 'sticker', 'property', 'camera'], [7, 7, 0, 0], [True, False, False, False], [0, 1, 2, -1]]

# directory and file
fileList = []
if os.path.exists(photoDir)==False:
	os.mkdir(photoDir)
photoNum = len(os.listdir(photoDir))

# load detect source
face, eye, nose, mouth = sticker.loadDetectModule()

# create camera - 640*480
cap = cv2.VideoCapture()
cap.open(0)

# create window
window = tk.Tk()
window.title("Multimedia Final Project - Team 8")
window.geometry("800x640")
window.resizable(0, 0)

# create labels
video = tk.Label(window)
video.pack()

# create trackbars
allObject = []
adjustVar = []
adjustBar = button.ScaleArray()
for i in xrange(adjustNum):
	adjustVar.append(tk.DoubleVar())
	adjustBar.append(window, btnSize*2+shift*11, btnSize*3+shift*(i*5+1), barLength, False, barInfo[1][i], barInfo[0][i], adjustVar[i])
allObject.append(adjustBar)

# create function options buttons
optionBtns = []
for j in xrange(2):
	optionBtns.append(button.ButtonArray(btnInfo[2][j]))
	for i in xrange(btnInfo[1][j]):
		filename = imageDir + btnInfo[0][j] + str(i+1) + '.jpg'
		optionBtns[j].append(window, filename, btnSize*(i+2)+shift, videoHeight+shift, btnSize-shift*2, i, False)
	allObject.append(optionBtns[j])
optionBtns.append(adjustBar)
optionBtns.append(None)

# create function buttons
funcBtns = button.ButtonArray(False)
for i in xrange(funcBtnNum):
	filename = imageDir + btnInfo[0][i] + '.png'
	funcBtns.append(window, filename, shift, btnSize*i+shift, btnSize-shift*2, btnInfo[3][i], True)
	funcBtns.array[i].show()
allObject.append(funcBtns)

# create direction buttons
leftBtn = button.dirButton(window, 'image/left.jpg', btnSize+shift, videoHeight + shift, btnSize-shift*2, False, 'left', funcBtns, optionBtns)
rightBtn = button.dirButton(window, 'image/right.jpg', btnSize*4+shift, videoHeight + shift, btnSize-shift*2, False, 'right', funcBtns, optionBtns)
leftBtn.show()
rightBtn.show()
leftBtn.registerPartner(rightBtn)
rightBtn.registerPartner(leftBtn)
allObject.append(leftBtn)
allObject.append(rightBtn)

# set function btn control
for i in xrange(funcBtnNum):
	funcBtns.array[i].appendControl(optionBtns[i])
	funcBtns.array[i].appendControl(leftBtn)
	funcBtns.array[i].appendControl(rightBtn)

# real time video callback
def show_frame():
	_, frame = cap.read()
	frame = cv2.flip(frame, 1)

	# btn effect - filters
	if funcBtns.array[0].press:
		state = functions.calOneHotIndex(optionBtns[0].btnPressState())
		if state==1:
			frame = filter.Changing_Color1(frame)
		elif state==2:
			frame = filter.Changing_Color2(frame)
		elif state==3:
			frame = filter.Changing_Color3(frame)
		elif state==4:
			frame = filter.Changing_Color4(frame)
		elif state==5:
			frame = filter.OldFashion(frame)
		elif state==6:
			frame = filter.Negative(frame)
		elif state==7:
			frame = filter.Drawing(frame)

	# btn effect - sticker
	if funcBtns.array[1].press:
		frame = sticker.allSticker(frame, optionBtns[1].btnPressState(), face, eye, nose, mouth)

	# btn effect - property
	if funcBtns.array[2].press:
		frame = filter.Contrast(frame, adjustVar[0].get())
		frame = filter.Brightness(frame, adjustVar[1].get())
		frame = filter.Saturation(frame, adjustVar[2].get())

	# btn effect - snapshot
	if funcBtns.array[3].press:
		global photoNum
		photoNum = functions.snapshot(frame, photoNum)
		functions.reset(allObject)
		functions.showImageAndPaint(photoNum-1)

	img = functions.opencv2tkinter(frame)
	video.imgtk = img
	video.configure(image=img)
	video.place(x = windowWidth-videoWidth, y = 0)
	video.after(10, show_frame)

show_frame()
window.mainloop()