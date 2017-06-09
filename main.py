import os
import cv2
import Tkinter as tk
from PIL import Image, ImageTk
import functions as fc
import button
import filter3


# define constant
windowWidth, windowHeight = 800, 640
videoWidth, videoHeight = 640, 480
funcBtnNum = 4
btnSize = 160
shift = 10
photoDir = 'snapshot/'
imageDir = 'image/'
btnInfo = [['filter', 'sticker', 'paint', 'camera'], [0, 6, 0, 0], [True, False, True, False]]

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

funcBtns = button.ButtonArray(False)
for i in xrange(funcBtnNum):
	if i==3:
		num = -1
	else:
		num = i
	filename = imageDir + btnInfo[0][i] + '.png'
	funcBtns.append(window, filename, shift, btnSize*i+shift, btnSize-shift*2, num)
	funcBtns.array[i].show()

optionBtns = []
for i in xrange(funcBtnNum):
	optionBtns.append(button.ButtonArray(btnInfo[2][i]))
	for j in xrange(btnInfo[1][i]):
		filename = imageDir + btnInfo[0][i] + str(j+1) + '.jpg'
		optionBtns[i].append(window, filename, btnSize*(j+2) + shift, videoHeight + shift, btnSize-shift*2, j)

# real time video callback
def show_frame():
	_, frame = cap.read()
	frame = cv2.flip(frame, 1)

	# btn effect
	if funcBtns.array[0].press:
		frame = filter3.Changing_Color(frame)
	if funcBtns.array[3].press:
		global photoNum
		photoNum = fc.snapshot(photoNum, frame)
		funcBtns.array[3].defaultCallback()
	for i in xrange(funcBtnNum-1):
		if i==funcBtns.nowPressed:
			optionBtns[i].show()
		else:
			optionBtns[i].hide()

	img = fc.opencv2tkinter(frame)
	video.imgtk = img
	video.configure(image=img)
	video.place(x = windowWidth-videoWidth, y = 0)
	video.after(10, show_frame)

show_frame()
window.mainloop()