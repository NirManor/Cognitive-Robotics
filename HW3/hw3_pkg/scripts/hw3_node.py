#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, sqrt
import numpy as np
from turtlesim.srv import *
from std_srvs.srv import *

class TurtleBot:

    def __init__(self):
        rospy.init_node('turtlebot_controller', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel',
                                                  Twist, queue_size=10)
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose',
                                                Pose, self.update_pose)

        self.pose = Pose()
        self.rate = rospy.Rate(10)

    def update_pose(self, data):
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)
        self.pose.theta = round(self.pose.theta, 6)

    def euclidean_distance(self, goal_pose):
        return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                    pow((goal_pose.y - self.pose.y), 2))

    def go_for(self, xspeed, zspeed, T):

        self_pose = self.pose
        vel_msg = Twist()
        t0 = rospy.Time.now().to_sec()
        t1 = rospy.Time.now().to_sec()
        time_measured = t1 - t0

        while time_measured <= T:
            t1 = rospy.Time.now().to_sec()
            time_measured = t1 - t0
            if xspeed >= 0:
                vel_msg.linear.x = xspeed
            else:
                vel_msg.linear.x = -abs(xspeed)

            if zspeed >= 0:
                vel_msg.angular.z = zspeed
            else:
                vel_msg.angular.z = -abs(zspeed)

            self.velocity_publisher.publish(vel_msg)
            self.rate.sleep()

        vel_msg.linear.x = 0
        vel_msg.linear.y = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)

    def tele_turtle(self, x, y, theta):
        rospy.wait_for_service('/turtle1/teleport_absolute')
        set_pose = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
        set_pose(x, y, theta)

    def kill_turtlesim(self, turtlename):
        rospy.wait_for_service('/kill')
        kill_turtle = rospy.ServiceProxy('/kill', Kill)
        kill_turtle(turtlename)

    def spawn_turtle(self, x, y, theta, name):
        rospy.wait_for_service('/spawn')
        spawn_turtle = rospy.ServiceProxy('/spawn', Spawn)
        spawn_turtle(x, y, theta, name)
        return name

    def clear_turtlesim(self):
        rospy.wait_for_service('/clear')
        try:
            clear_background = rospy.ServiceProxy('/clear', Empty)
            clear_background()
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)

if __name__ == '__main__':
    try:
        x = TurtleBot()
        x.clear_turtlesim()
        x.kill_turtlesim('turtle1')

        # print the letter T
        x.spawn_turtle(0.2, 6, 0, 'turtle1')
        x.tele_turtle(1.6, 6, 0)
        x.tele_turtle(1.6, 5.7, 0)
        x.tele_turtle(1.05, 5.7, 0)
        x.tele_turtle(1.05, 4.7, 0)
        x.tele_turtle(0.75, 4.7, 0)
        x.tele_turtle(0.75, 5.7, 0)
        x.tele_turtle(0.2, 5.7, 0)
        x.tele_turtle(0.2, 6, 0)
        x.kill_turtlesim('turtle1')

        # print the letter E
        x.spawn_turtle(1.8, 6, 0, 'turtle1')
        x.tele_turtle(2.8, 6, 0)
        x.tele_turtle(2.8, 5.7, 0)
        x.tele_turtle(2.1, 5.7, 0)
        x.tele_turtle(2.1, 5.5, 0)
        x.tele_turtle(2.8, 5.5, 0)
        x.tele_turtle(2.8, 5.2, 0)
        x.tele_turtle(2.1, 5.2, 0)
        x.tele_turtle(2.1, 5, 0)
        x.tele_turtle(2.8, 5, 0)
        x.tele_turtle(2.8, 4.7, 0)
        x.tele_turtle(1.8, 4.7, 0)
        x.tele_turtle(1.8, 6, 0)
        x.kill_turtlesim('turtle1')

        # print the letter C
        x.spawn_turtle(4, 5.8, 0.8*np.pi, 'turtle1')
        x.go_for(0.65, 1.0, 4.3)
        x.tele_turtle(3.7426, 4.89, -0.9*np.pi)
        x.go_for(0.65, -1.58, 2.3)
        x.tele_turtle(4, 5.8, 0)
        x.kill_turtlesim('turtle1')

        # print the letter H
        x.spawn_turtle(4.3, 6, 0, 'turtle1')
        x.tele_turtle(4.3, 4.7, 0)
        x.tele_turtle(4.5, 4.7, 0)
        x.tele_turtle(4.5, 5.25, 0)
        x.tele_turtle(5, 5.25, 0)
        x.tele_turtle(5, 4.7, 0)
        x.tele_turtle(5.2, 4.7, 0)
        x.tele_turtle(5.2, 6, 0)
        x.tele_turtle(5, 6, 0)
        x.tele_turtle(5, 5.5, 0)
        x.tele_turtle(4.5, 5.5, 0)
        x.tele_turtle(4.5, 6, 0)
        x.tele_turtle(4.3, 6, 0)
        x.kill_turtlesim('turtle1')

        # print the letter N
        x.spawn_turtle(5.5, 6, 0, 'turtle1')
        x.tele_turtle(5.5, 4.7, 0)
        x.tele_turtle(5.7, 4.7, 0)
        x.tele_turtle(5.7, 5.7, 0)
        x.tele_turtle(6.3, 4.7, 0)
        x.tele_turtle(6.5, 4.7, 0)
        x.tele_turtle(6.5, 6, 0)
        x.tele_turtle(6.3, 6, 0)
        x.tele_turtle(6.3, 5.1, 0)
        x.tele_turtle(5.75, 6, 0)
        x.tele_turtle(5.5, 6, 0)
        x.kill_turtlesim('turtle1')

        # print the letter I
        x.spawn_turtle(6.8, 6, 0, 'turtle1')
        x.tele_turtle(7.8, 6, 0)
        x.tele_turtle(7.8, 5.8, 0)
        x.tele_turtle(7.4, 5.8, 0)
        x.tele_turtle(7.4, 4.9, 0)
        x.tele_turtle(7.8, 4.9, 0)
        x.tele_turtle(7.8, 4.7, 0)
        x.tele_turtle(6.8, 4.7, 0)
        x.tele_turtle(6.8, 4.9, 0)
        x.tele_turtle(7.2, 4.9, 0)
        x.tele_turtle(7.2, 5.8, 0)
        x.tele_turtle(6.8, 5.8, 0)
        x.tele_turtle(6.8, 6, 0)
        x.kill_turtlesim('turtle1')

        # print the letter O
        x.spawn_turtle(8.6, 6, np.pi, 'turtle1')
        x.go_for(1.0, 1.6, 4)
        x.kill_turtlesim('turtle1')
        x.spawn_turtle(8.6, 5.8, np.pi, 'turtle1')
        x.go_for(1.0, 2.35, 3)
        x.kill_turtlesim('turtle1')

        # print the letter N
        x.spawn_turtle(9.5, 6, 0, 'turtle1')
        x.tele_turtle(9.5, 4.7, 0)
        x.tele_turtle(9.7, 4.7, 0)
        x.tele_turtle(9.7, 5.7, 0)
        x.tele_turtle(10.3, 4.7, 0)
        x.tele_turtle(10.5, 4.7, 0)
        x.tele_turtle(10.5, 6, 0)
        x.tele_turtle(10.3, 6, 0)
        x.tele_turtle(10.3, 5.1, 0)
        x.tele_turtle(9.75, 6, 0)
        x.tele_turtle(9.5, 6, 0)
        x.kill_turtlesim('turtle1')

        x.spawn_turtle(0.2, 6, 0, 'turtle1')
    except rospy.ROSInterruptException:
        pass
