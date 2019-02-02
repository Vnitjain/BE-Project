import RPi.GPIO as io
from picamera import PiCamera
import sys,tty,termios,time
import os
import numpy as np

#init io
io.setmode(io.BOARD)

#setup pins
io.setup(3,io.OUT)
io.setup(10,io.OUT)

#Global variables
path = None
count = None

#Dimensions of image to capture
image_height = 64
image_width = 64
image_channels = 3

#No of images to capture
no_of_img = 1000

#creating numpy array for no_of_img images
img_array = np.zeros([no_of_img,image_channels,image_height,image_width])

def camera_init():
	camera = PiCamera()
	camera.resolution = (64,64)
	camera.framerate = 80
	camera.start_preview()
	time.sleep(2)
	return camera

def csv_init():
	global path
	path = os.getcwd()
	os.system("mkdir data")
	os.chdir("data")
	os.system("mkdir IMG")
	fh = open('driving_log.csv','w')
	return fh

def capture_data(cam,file_handler,steer_value,file_name):
	global img_array
	obj = np.empty((image_channels,image_height,image_width), dtype = np.uint8)
	cam.capture(obj, 'rgb',use_video_port=True)
	img_array[count] = obj
	fh.write("%s,%s\n" % ('IMG/'+str(file_name)+'.jpg',steer_value))
	print("captured")

def flush_images():
	print("Writing Images to disk")
	global img_array
	for i in range(count):
		image = img_array[i]
		np.save(str(i),image)

def getch():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd,termios.TCSADRAIN, old_settings)
	return ch

if __name__ == "__main__":
	#Init Camera
	cam = camera_init()
	
	#Init CSV File
	fh = csv_init()	
	
	global count
	count = 1
	while True:
			chr = getch()
			#print(count)
			if chr =='a':
				capture_data(cam,fh,-1,count)
			if chr =='d':
				capture_data(cam,fh,1,count)
			if chr == 'q':
				flush_images()
				fh.close()
				cam.stop_preview()
				break
			#io.output(10,io.LOW)
			#io.output(3,io.LOW)
			count += 1
	
