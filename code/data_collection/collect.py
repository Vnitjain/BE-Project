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

path = None

def camera_init():
	camera = PiCamera()
	camera.resolution = (64,64)
	camera.framerate = 80
	camera.start_preview()
	time.sleep(2)
	camera.stop_preview()
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
	obj = np.empty((64,64,3), dtype = np.uint8)
	cam.capture(obj, 'rgb')
	#np.save(str(file_name),obj)
	fh.write("%s,%s\n" % ('IMG/'+str(file_name)+'.jpg',steer_value))
	print("captured")

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

	count = 1
	child_pid = None
	parent_pid = None
	pid = os.fork()
	read_pipe, write_pipe = os.pipe()
	while True:
			chr = getch()
			print(count)
			if chr =='a':
				capture_data(cam,fh,-1,count)
			if chr =='d':
				capture_data(cam,fh,1,count)
			if chr == 'q':
				os.kill(child_pid)
				break
			#io.output(10,io.LOW)
			#io.output(3,io.LOW)
			count += 1
	
	"""
	if pid > 0:
		#Parent
		global parent_pid
		parent_pid = os.getpid()
		os.close(read_pipe)
		w = os.fdopen(write_pipe)
		while True:
			chr = getch()
			print(count)
			if chr =='a':
				w.write("Hello")
			if chr =='d':
				capture_data(cam,fh,1,count)
			if chr == 'q':
				os.kill(child_pid)
				break
			#io.output(10,io.LOW)
			#io.output(3,io.LOW)
			count += 1
			time.sleep(1)
			

	else:
		#Chid
		global child_pid
		child_pid = os.getpid()
		os.close(write_pipe)
		r = os.fdopen(read_pipe)
		while True:
			print("da")
			str = r.read()
			if str is not None:
				print(str)
			time.sleep(1)

	"""
