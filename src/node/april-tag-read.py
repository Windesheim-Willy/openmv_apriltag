#!/usr/bin/env python
import serial
import rospy
from std_msgs.msg import String

# To which topic on Willy we will publish
topicName ='openmv_apriltag'

# Init ROS components
rospy.init_node('topic_publisher')
topicInstance = rospy.Publisher(topicName, String ,queue_size=25)
rate = rospy.Rate(2)
topicMessage = "Empty"

# Init serial components
socket = serial.Serial()
socket.baudrate = 115200
socket.port = '/dev/ttyACM0'
socket.timeout = 1
socket.open()


while not rospy.is_shutdown(): 
    topicMessage = socket.readline()
    topicInstance.publish(topicMessage)
    print(topicMessage)
    rate.sleep()

