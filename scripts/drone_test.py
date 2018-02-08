#!/usr/bin/env python
import rospy
import time
import serial
import os
from mavros_msgs.msg import OverrideRCIn


ser = serial.Serial(port='/dev/ttyUSB0',baudrate = 115200)
pub = rospy.Publisher('/mavros/rc/override', OverrideRCIn, queue_size=10)
rcinput = OverrideRCIn()
rcinput.channels[0] = 0
rcinput.channels[1] = 0
rcinput.channels[2] = 0
rcinput.channels[3] = 0
rcinput.channels[4] = 0
rcinput.channels[5] = 0
rcinput.channels[6] = 0
rcinput.channels[7] = 0

def listener():
    rospy.init_node('listener', anonymous=True)
    #rospy.spin()

def printResult(sen1,sen2,sen3,sen4):
	print "here"
	os.system("clear")
	line1 = "Left Sensor : "+sen1+"     Right Sensor : "+sen3
	line2 = "Front Sensor : "+sen2+"    Back Sensor : "+sen4
	print line1
	print line2

def doWork():
	while 1:
		print "start"
		inbuff = ser.readline()
		#print inbuff
		inADCT = inbuff.split(",")
		ch1 = 1500
		ch2 = 1500
		print inbuff
    	printResult(inADCT[1],inADCT[2],inADCT[3],inADCT[4])
    	if int(inADCT[1]) >= 200 or int(inADCT[2]) >= 200 or int(inADCT[3]) >= 200 or int(inADCT[4]) >= 200:

			if int(inADCT[1]) >= 200:
				ch1 = ch1 + 120
			else:
				ch1 = ch1 + 0

			if int(inADCT[2]) >= 200:
				ch2 = ch2 - 120
			else:
				ch2 = ch2 - 0
		
			if int(inADCT[3]) >= 200:
				ch1 = ch1 - 120
			else:
				ch1 = ch1 - 0

			if int(inADCT[4]) >= 200:
				ch2 = ch2 + 120
			else:
				cha2 = ch2 + 0
			rcinput.channels[0] = ch1
			rcinput.channels[1] = ch2
			pub.publish(rcinput)
    	else:
    		rcinput.channels[0] = 0
    		rcinput.channels[1] = 0
    		pub.publish(rcinput)
    	print "end"









listener()
print "running"
if ser.isOpen == True:
	doWork()
else:
	ser.close()
	ser.open()
	doWork()


   
    
    



