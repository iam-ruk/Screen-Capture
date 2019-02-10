#mss for getting the pixel values
from mss import mss
#socket to establish connection and send data
import socket
import numpy as np
import cv2
#for mouse control
from pynput.mouse import Controller,Button
import sys

#A dict containg the window size
monitor={'top':0,'left':0,'width':1024,'height':768}
#creating an instance for the mss class
scc=mss()
s1=socket.socket()
#creating an instance for the Controller class
mouse=Controller()
def str2bool(v):
	return v=='True'

#for controlling the mouse
s1.connect(('localhost',9999))
#making it a non blocking socket
s1.setblocking(0)
s=socket.socket()
s.connect(('localhost',9997))
while True:
	#getting the pixel value
	xstring=np.array(scc.grab(monitor),dtype=np.uint8)
	#converting the pixel value to IMAGE TO GRAY_SCALE
	xstring=np.array(cv2.cvtColor(xstring,cv2.COLOR_BGRA2GRAY))
	s.send(xstring.tostring())
	try:
		#info about mouse movements
		data=s1.recv(1024).decode('utf-8')
		if not data:
			sys.exit(1)
		else:
			#splitting the incoming data
			l=data.split()
			for pos in l:
				#CHANGING THE POSITION VALUES
				if len(pos.split(','))==2:
					mouse.position=tuple(map(int,pos.split(',')))
				else:
					x,y,button,pressed=pos.split(',')
					print(button,pressed)
					if button=="Button.left" and str2bool(pressed):
						mouse.press(Button.left)
					elif button=="Button.left" and not str2bool(pressed):
						mouse.release(Button.left)
					elif button=="Button.right" and str2bool(pressed):
						mouse.press(Button.right)
					elif button=="Button.right" and not str2bool(pressed):
						mouse.release(Button.right)

						
	except socket.error as e:
		continue



s.close()
s1.close()
