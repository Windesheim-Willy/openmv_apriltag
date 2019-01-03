#!/usr/bin/env python
import serial
import rospy
import time
import math
from time import sleep
from std_msgs.msg import String
from geometry_msgs.msg import PoseWithCovarianceStamped

# Init ROS components
rospy.init_node('openmv_apriltag')
openmvTopic = rospy.Publisher("openmv_apriltag", String , queue_size=25)

# Init serial components
socket = serial.Serial()
socket.baudrate = 115200
socket.port = '/dev/sensor_openmv'
socket.timeout = 1
socket.open()

while not rospy.is_shutdown():
	# Read OpenMV data
	openmvMessage = socket.readline()
	openmvMessage = openmvMessage.rstrip()

	# Publish OpenMV data
	openmvTopic.publish(openmvMessage)
	print(openmvMessage)
