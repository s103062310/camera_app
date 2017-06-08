import cv2
import Tkinter as tk
from PIL import Image, ImageTk
import functions as fc
import button
import filter


# define constant
windowWidth, windowHeight = 800, 640
videoWidth, videoHeight = 640, 480
funcBtnNum = 4
btnSize = 160
shift = 10
imageFile = ['image/filter.png', 'image/sticker.png', 'image/paint.png', 'image/camera.png']

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
btns = []
for i in xrange(funcBtnNum):
	btns.append(button.Button(window, imageFile[i], shift, btnSize*i+shift, btnSize-shift*2))
	btns[i].label.pack()

# real time video callback
def show_frame():
	_, frame = cap.read()
	frame = cv2.flip(frame, 1)
	if btns[0].press:
		frame = filter.oldFashion(frame)
	if btns[3].press:
		btns[3].press = 0
		cv2.imwrite('snapshot/photo.jpg', frame)
	img = fc.opencv2tkinter(frame)
	video.imgtk = img
	video.configure(image=img)
	video.place(x = windowWidth-videoWidth, y = 0)
	video.after(10, show_frame)

def show_button(btn):
	img = cv2.resize(btn.image, (btn.size, btn.size), interpolation=cv2.INTER_CUBIC)
	imgtk = fc.opencv2tkinter(img)
	btn.label.imgtk = imgtk
	btn.label.configure(image=imgtk)
	btn.label.place(x = btn.x, y = btn.y)
	btn.label.after(10, show_button)

show_frame()
for i in xrange(funcBtnNum):
	show_button(btns[i])

window.mainloop()