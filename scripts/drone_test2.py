#!/usr/bin/env python
import rospy
import time
import serial
import os
from mavros_msgs.msg import OverrideRCIn


ser = serial.Serial(port='/dev/ttyUSB0',baudrate = 115200)

def sender():
	pub = rospy.Publisher('/mavros/rc/override', OverrideRCIn, queue_size=10)
	rospy.init_node('listener', anonymous=True)
	rcinput = OverrideRCIn()
	rcinput.channels[0] = 0
	rcinput.channels[1] = 0
	rcinput.channels[2] = 0
	rcinput.channels[3] = 0
	rcinput.channels[4] = 1500
	rcinput.channels[5] = 1500
	rcinput.channels[6] = 1500
	rcinput.channels[7] = 1500
	if ser.isOpen() == False:
		ser.close()
		ser.open()
	rate = rospy.Rate(25)
	while not rospy.is_shutdown():
		inbuff = ser.readline()
		inADCT = inbuff.split(",")
		rcch1 = 1500
		rcch2 = 1500
		if len(inADCT) > 3:
			printResult(inADCT[1],inADCT[2],inADCT[3],inADCT[4])
			if int(inADCT[1]) >= 200 or int(inADCT[2]) >= 200 or int(inADCT[3]) >= 200 or int(inADCT[4]) >= 200:
				if int(inADCT[1]) >= 200:
					rcch1 = rcch1 + 120
					
				else:
					rcch1 = rcch1 + 0

				if int(inADCT[2]) >= 200:
					rcch2 = rcch2 - 120
				else:
					rcch2 = rcch2 - 0

				if int(inADCT[3]) >= 200:
					rcch1 = rcch1 - 120
				else:
					rcch1 = rcch1 - 0

				if int(inADCT[4]) >= 200:
					rcch2 = rcch2 + 120
				else:
					rcch2 = rcch2 - 0
				rcinput.channels[0] = rcch1
				rcinput.channels[1] = rcch2
				pub.publish(rcinput)
			else:
				rcinput.channels[0] = 1500
				rcinput.channels[1] = 1500
				rcinput.channels[2] = 1000
				rcinput.channels[3] = 2000
				pub.publish(rcinput)
			print rcinput.channels[0]







def printResult(sen1,sen2,sen3,sen4):
	print "here"
	os.system("clear")
	line1 = "Left Sensor : "+sen1+"     Right Sensor : "+sen3
	line2 = "Front Sensor : "+sen2+"    Back Sensor : "+sen4
	print line1
	print line2
	#print rcinput.channels[0]
	#print rcinput.channels[1] 



sender()
print "running"


   
    
    



