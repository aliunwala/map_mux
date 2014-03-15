#!/usr/bin/env python

import roslib; roslib.load_manifest("map_mux")

import rospy
import time
from std_msgs.msg import String
from std_msgs.msg import Int16
from nav_msgs.msg import OccupancyGrid
map1 = None
map2 = None
map3 = None
change_map = None
# Subscribe to
    # TOPIC : 3 maps
    # SERVICE : Change map
    #
# Send out
    # TOPIC: /map
    # SERVICE : /static_map
    # /inital_pose
    # /clear_cosmaps

# assume maps are loaded to topics map1, map2, map3

def map_mux():
    rospy.init_node("map_mux", anonymous=True)
    rospy.Subscriber("map1", OccupancyGrid, addMap1)
    rospy.Subscriber("map2", OccupancyGrid, addMap2)
    rospy.Subscriber("map3", OccupancyGrid, addMap3)
    rospy.Subscriber("change_map", Int16 , changeMap)
    topic = rospy.resolve_name("map")
    pub = rospy.Publisher("map", OccupancyGrid)
    #pub = rospy.Publisher("map", Int16)
    r = rospy.Rate(10)

    while not rospy.is_shutdown():
        if (change_map == 1 and map1 != None):
            rospy.loginfo("changing to 1")
            pub.publish(map1)
        if (change_map == 2 and map2 != None):
            rospy.loginfo("changing to 2")
            pub.publish(map2)
        if (change_map == 3 and map3 != None):
            rospy.loginfo("changing to 3")
            pub.publish(map3)
        r.sleep()
    #rospy.spin()


def addMap1(data):
    #rospy.loginfo( type(data.data))
    rospy.loginfo("1")
    global map1
    map1 = data
def addMap2(data):
    rospy.loginfo("2" )
    global map2
    map2 = data
def addMap3(data):
    rospy.loginfo("3" )
    global map3
    map3 = data
def changeMap( data):
    global change_map
    change_map = data.data

if __name__ == '__main__':
    try:
        map_mux()
    except rospy.ROSInterruptException: pass
    rospy.spin()
