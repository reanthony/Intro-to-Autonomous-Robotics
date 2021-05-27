#!/usr/bin/env python
import rospy
import time
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from random import seed
from random import randint

class ForceMapper(): 
    def __init__(self):
        self.r = rospy.Rate(250) # 250hz
        self.linear_speed = 1.0
        self.angular_speed = 0.6
        self.move_cmd = Twist()
        self.sub = rospy.Subscriber('/scan', LaserScan, self.callBack)
        self.pub_obs = rospy.Publisher('obstacle', String, queue_size=10)
        self.cmd_pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=1)
        self.start()

    def forward(self):
        self.move_cmd.linear.x = self.linear_speed

    def turn(self):
        self.move_cmd.angular.z = self.angular_speed
    
    def stop(self):
        self.move_cmd.linear.x = 0

    def behavior1(self, msg):
        size = len(msg.ranges)
        right = msg.ranges[0]
        front = msg.ranges[size/2]
        left = msg.ranges[size-1]
        print("l,f,r: ", left, front, right)
        if (front > 1.25  and left > 0.4 and right > 0.4):
            self.forward()
	#elif (front < 1.25 and left < 1.1 and right < 1.1):
	    #self.move_cmd.linear.x = 5 * -self.linear_speed
	#    self.move_cmd.angular.z = 3 * -self.angular_speed
        else:
            self.stop()
	    if(left > right): 
        	self.move_cmd.angular.z = self.angular_speed
		self.move_cmd.linear.x = -self.linear_speed 
	    elif(right > left):
                self.move_cmd.angular.z = -self.angular_speed
                self.move_cmd.linear.x = -self.linear_speed
	for _ in range(1):
	    value = randint(0, 100)
	    if (value == 5):
	        temp = self.move_cmd.angular.z
		temp1 = self.linear_speed
		self.stop()
		self.move_cmd.angular.z = self.angular_speed * -100
	        self.linear_speed = 0
		self.stop()
		time.sleep(1.6)
		self.stop()
		#self.move_cmd.angular.z = self.angular_speed * 2
	    	self.move_cmd.angular.z = temp
		self.linear_speed = temp1
		
    def start(self):
        while not rospy.is_shutdown():
            self.cmd_pub.publish(self.move_cmd)
            self.r.sleep()

    def callBack(self, msg):
        self.behavior1(msg)

def main():
    rospy.init_node('ForceMapper')
    try:
        force = ForceMapper()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()
