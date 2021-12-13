import win32gui
import win32ui
import win32con
import win32api
import time
import sys
import os
from pynput import mouse
import time
from PIL import ImageGrab
import pyautogui
def findTitle(window_title):
	hWndList = []
	win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
	for hwnd in hWndList:
		title = win32gui.GetWindowText(hwnd)
		if (title == window_title):
			break
	return hwnd
def getpos(window_title):
	return win32gui.GetWindowRect(findTitle(window_title))

T=0
op=["",0]
def on_click(u, v, button, pressed):
	global T,f
	if button.name=='left' and pressed==True:
		if T==0:
			return
		print((u-x)/w,(v-y)/h,time.time()-T,file=f)
		print((u-x)/w,(v-y)/h,u,v,time.time()-T)
	if button.name=='right' and pressed==True:
		if T==0:
			f=open(op[0],"w")
			T=time.time()
		else:
			f.close()
			print("Done.")
			os._exit(0)
def on_scroll(u, v, U, V):
	assert(U==0)
	print((u-x)/w,(v-y)/h,U/w,V/h,time.time()-T)
	print((u-x)/w,(v-y)/h,U/w,V/h,time.time()-T,file=f)
def Run(op,t):
	T=time.time()
	print("run in ",t,"s.")
	time.sleep(t)
	print("open ",op)
	f=open(op)
	In=f.readlines()
	f.close()
	for i in In:
		if len(i.split())==3:
			u,v,z=(float(j) for j in i.split())
			while time.time()-T<z:
				pass
			pyautogui.click(int(x+w*u),int(y+h*v),1,1)
		else:
			u,v,U,V,z=(float(j) for j in i.split())
			while time.time()-T<z:
				time.sleep(0.01)
			pyautogui.moveTo(int(x+w*u),int(y+h*v))
			pyautogui.scroll(round(V*w))
			print(round(V*w),int(x+w*u),int(y+h*v))
def get(u,v,out):
	In=[]
	for i in open("xy").readlines():
		In.append(i.split())
#	print(In)
	_x=[float(In[0][0]),float(In[1][0]),float(In[2][0])]
	_y=[float(In[3][0]),float(In[4][0])]
	dx,dy=float(In[5][0]),float(In[5][1])
	X,Y=_x[u]+dx,_y[v]+dy
#	print((int(x+(X-0.01)*w), int(y+(Y-0.01)*h), int(x+(X+0.01)*w), int(y+(Y+0.01)*h)))
	pic=ImageGrab.grab(bbox=(int(x+(X-0.01)*w),  int(y+(Y-0.01)*h),int(x+(X+0.01)*w), int(y+(Y+0.01)*h)))
	pic.save(out)
from PIL import Image
import math
import operator
from functools import reduce
def image_contrast(img1, img2):
    image1 = Image.open(img1)
    image2 = Image.open(img2)
    h1 = image1.histogram()
    h2 = image2.histogram()
    result = math.sqrt(reduce(operator.add,  list(map(lambda a,b: (a-b)**2, h1, h2)))/len(h1) )
    return result


title =  u'BloonsTD6'
x,y,w,h = getpos(title)
w,h=w-x,h-y
print(x,y,w,h)
hard={"bb":""}
op=["bbh",1]
if op[1]==0:
	with mouse.Listener(on_click=on_click,on_scroll=on_scroll) as listener:
		listener.join()
else:
	time.sleep(3)
	tim=0
	while True:
		tim=tim+1
		Run("st",5)
		k,flag=0,0
		while True:
			for i in [0,1,2]:
				for j in [0,1]:
					get(i,j,"1.PNG")
					if image_contrast("1.PNG","2.PNG")<=20:
						id=chr(k+ord('a'))+chr(j*3+i+ord('a'))
						if hard.__contains__(id):
							Run(id+hard[id],2)
						else:
							Run(id,2)
						flag=1
			if(flag):
				break
			Run("ne",1)
			k=1-k
		print("run ",tim," times.")
