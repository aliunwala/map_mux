#!/usr/bin/env python

import roslib; roslib.load_manifest('rospy_tutorials')

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int16

def talker():
    rospy.init_node('talker', anonymous=True)
    pub = rospy.Publisher('change_map', Int16)
    r = rospy.Rate(1) # 10hz
    i = 1
    while not rospy.is_shutdown():
        if i == 1:
            i = 2
        elif i == 2:
            i = 3
        elif i == 3:
            i = 1
        rospy.loginfo(i)
        pub.publish(i)
        r.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
