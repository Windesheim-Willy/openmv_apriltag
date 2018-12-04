#!/usr/bin/env python
import serial
import rospy
import time
import math
from time import sleep
from std_msgs.msg import String
from geometry_msgs.msg import PoseWithCovarianceStamped

# Init ROS components
rospy.init_node('topic_publisher')
openmvTopic = rospy.Publisher("openmv_apriltag", String , queue_size=25)
poseTopic = rospy.Publisher("initialpose", PoseWithCovarianceStamped, queue_size=25)


# Init serial components
socket = serial.Serial()
socket.baudrate = 115200
socket.port = '/dev/ttyACM1'
socket.timeout = 1
socket.open()

# Init global components
aprilTag = tuple()

# Build tag location dictionary
tagLocations = {
1:(13.489720850756148, 60.59727947971955, 0.0),
2:(15.934169265195797, 60.933202561559746, 0.0),
3:(20.810319786490506, 60.41751882276302, 0.0),
4:(24.50055443446291, 60.43755116603776, 0.0),
5:(28.07578804452108, 60.138835332979674, 0.0),
6:(31.72803700360133, 60.21433696281538, 0.0),
7:(35.079547458633726, 60.144928942058925, 0.0),
8:(38.86555094259316, 60.061022359125516, 0.0),
9:(42.76742784387715, 60.18446581588793, 0.0),
10:(46.17944236172726, 59.43959194286109, 0.0),
11:(44.86658591585901, 54.932326361019605, 0.0),
12:(41.56825528354129, 55.081602467414015, 0.0),
13:(37.76570212962082, 55.165675939740616, 0.0),
14:(34.22908972386625, 55.347169977516856, 0.0),
15:(30.58898019154235, 55.07027803761846, 0.0),
16:(26.932984917133314, 55.11965596266801, 0.0),
17:(23.205978661221213, 55.18059190272544, 0.0),
18:(19.743041561789195, 55.347504401255364, 0.0),
19:(16.299067248414662, 55.46434990288788, 0.0),
20:(12.100164063844309, 55.42996574075256, 0.0),
21:(9.65735918277374, 55.445542959329764, 0.0),
24:(10.65735918277374, 55.445542959329764, 0.0),
528:(43.65193339638883, 60.123809610098775, 0.0)
}


while not rospy.is_shutdown():
	# Read OpenMV data
	openmvMessage = socket.readline()
	openmvMessage = openmvMessage.rstrip()
	aprilTag = tuple((
	float(openmvMessage.split(",")[0]),
	float(openmvMessage.split(",")[1]),
	openmvMessage.split(",")[2]
	))

	# Publish OpenMV data
	openmvTopic.publish(openmvMessage)
	print(openmvMessage)

	# Publish pose data
	if aprilTag[0] > 0:
		tagLocation = tagLocations.get(aprilTag[0], (0.0, 0.0, 0.0))
		poseMessage = PoseWithCovarianceStamped()

		poseMessage.header.seq = 0
		poseMessage.header.frame_id = "map"
		poseMessage.header.stamp.secs = rospy.get_rostime().secs
		poseMessage.header.stamp.nsecs = rospy.get_rostime().nsecs
		poseMessage.pose.pose.position.x = tagLocation[0]
		poseMessage.pose.pose.position.y = tagLocation[1]
		poseMessage.pose.pose.position.z = 0.0
		
		radians = (math.pi/180)* aprilTag[1]
		poseMessage.pose.pose.orientation.x = 0.0
		poseMessage.pose.pose.orientation.y = 0.0
		poseMessage.pose.pose.orientation.z = 0.999994075137
		poseMessage.pose.pose.orientation.w = math.cos(radians/2);

		#poseMessage.pose.covariance = [0.024762087464210936, -0.0014523279406830625, 0.0, 0.0, 0.0, 0.0, -0.0014523279407967493, 0.013989804469929368, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.004313379282554443]

		poseMessage.pose.covariance = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]




		poseTopic.publish(poseMessage)
		print(poseMessage)
		sleep(0)
