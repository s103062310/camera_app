import os
import cv2
import Tkinter as tk
from PIL import Image, ImageTk
import functions as fc
import button
import filter
import sticker


# define constant
windowWidth, windowHeight = 800, 640
videoWidth, videoHeight = 640, 480
funcBtnNum = 4
btnSize = 160
shift = 10
photoDir = 'snapshot/'
imageDir = 'image/'
btnInfo = [['filter', 'sticker', 'property', 'camera'], [7, 6, 0, 0], [True, False, False, False]]

# directory and file
fileList = []
if os.path.exists(photoDir)==False:
	os.mkdir(photoDir)
photoNum = len(os.listdir(photoDir))

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

filterBtns = button.ButtonArray(btnInfo[2][0])
for i in xrange(btnInfo[1][0]):
	filename = imageDir + btnInfo[0][0] + str(i+1) + '.jpg'
	filterBtns.append(window, filename, btnSize*(i+2) + shift, videoHeight + shift, btnSize-shift*2, i, None)

stickerBtns = button.ButtonArray(btnInfo[2][1])
for i in xrange(btnInfo[1][1]):
	filename = imageDir + btnInfo[0][1] + str(i+1) + '.jpg'
	stickerBtns.append(window, filename, btnSize*(i+2) + shift, videoHeight + shift, btnSize-shift*2, i, None)

optionBtns = [filterBtns, stickerBtns]
funcBtns = button.ButtonArray(False)
for i in xrange(funcBtnNum):
	filename = imageDir + btnInfo[0][i] + '.png'
	if i==3:
		funcBtns.append(window, filename, shift, btnSize*i+shift, btnSize-shift*2, -1, None)
	elif i==2:
		funcBtns.append(window, filename, shift, btnSize*i+shift, btnSize-shift*2, i, None)
	else:
		funcBtns.append(window, filename, shift, btnSize*i+shift, btnSize-shift*2, i, optionBtns[i])
	funcBtns.array[i].show()

leftBtn = button.dirButton(window, 'image/left.jpg', btnSize+shift, videoHeight + shift, btnSize-shift*2, 'left', True, funcBtns, optionBtns)
rightBtn = button.dirButton(window, 'image/right.jpg', btnSize*4+shift, videoHeight + shift, btnSize-shift*2, 'right', False, funcBtns, optionBtns)
leftBtn.show()
rightBtn.show()
leftBtn.registerPartner(rightBtn)
rightBtn.registerPartner(leftBtn)

# real time video callback
def show_frame():
	_, frame = cap.read()
	frame = cv2.flip(frame, 1)

	# btn effect
	if funcBtns.array[0].press:
		frame = filter.oldFashion(frame)
	#if funcBtns.array[2].press:
		#state = optionBtns[1].btnPressState()
		#print state
		#frame = sticker.allSticker(frame, [1,0,0,1,1,1])
	if funcBtns.array[3].press:
		global photoNum
		photoNum = fc.snapshot(photoNum, frame)
		funcBtns.array[3].defaultCallback()

	img = fc.opencv2tkinter(frame)
	video.imgtk = img
	video.configure(image=img)
	video.place(x = windowWidth-videoWidth, y = 0)
	video.after(10, show_frame)

show_frame()
window.mainloop()