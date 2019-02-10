from mss import mss
from mss.tools import to_png
import socket
import cv2
from sys import getsizeof
from pynput.mouse import Listener
import numpy as np

s1=socket.socket()
s1.bind(('',9999))
s=socket.socket()
s.bind(('',9997))
s.listen(0)
s1.listen(0)
conn,addr=s.accept()
conn1,addr1=s1.accept()
print('accepted')
data=conn.recv(1024*64)
img_data=data
def on_move(x,y):
    conn1.send(f'{x},{y} '.encode('utf-8'))

def on_click(x,y,button,pressed):
    conn1.send(f'{x},{y},{button},{pressed} '.encode('utf-8'))
with Listener(on_move=on_move,on_click=on_click) as l:
    while True:
        if not data:
            break
        else:

            data=conn.recv(1024*64)
            img_data+=data
            if len(img_data)>=(768*1024)-1:
                img1 = np.fromstring(img_data[:(1024*768)], dtype=np.uint8)
                img1 = img1.reshape((768, 1024))
                cv2.imshow('output', img1)
                img_data=img_data[1024*768:]
            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break

conn.close()
conn1.close()
s.close()
s1.close()