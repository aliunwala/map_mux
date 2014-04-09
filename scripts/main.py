#!/usr/bin/env python

from map_mux.srv import *
import rospy
import time
from std_msgs.msg import String
from std_msgs.msg import Int16
from nav_msgs.msg import OccupancyGrid
from nav_msgs.srv import GetMap
from nav_msgs.msg import MapMetaData
#from map_mux.srv import ChangeMap
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
    #rospy.Subscriber("change_map", Int16 , changeMap)
    s = rospy.Service('change_map', ChangeMap, changeMapfunc)
    s = rospy.Service('static_map', GetMap, staticMapfunc)
    #s = rospy.Service('add_two_ints', AddTwoInts, handle_add_two_ints)
    topic = rospy.resolve_name("map")
    pub = rospy.Publisher("map", OccupancyGrid)
    pub_metadata = rospy.Publisher("map_metadata", MapMetaData)
    #pub = rospy.Publisher("map", Int16)
    r = rospy.Rate(10)
    old_change_map = 0;

    while not rospy.is_shutdown():
        if( map1 == None  and map2 == None and map3 == None):
            print "you need to provide 3 maps on topics map1 map2 map3 from a launch file."
        if (change_map != old_change_map):
            if (change_map == 1 and map1 != None):
                rospy.loginfo("changing to 1")
                pub.publish(map1)
                pub_metadata.publish(map1.info)
            if (change_map == 2 and map2 != None):
                rospy.loginfo("changing to 2")
                pub.publish(map2)
                pub_metadata.publish(map2.info)
            if (change_map == 3 and map3 != None):
                rospy.loginfo("changing to 3")
                pub.publish(map3)
                pub_metadata.publish(map3.info)
        old_change_map = change_map
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
def changeMapfunc( data):
    global change_map
    change_map = data.data
    return 1
def staticMapfunc( data):
    global change_map
    return change_map

if __name__ == '__main__':
    try:
        map_mux()
    except rospy.ROSInterruptException: pass
    rospy.spin()

#def handle_add_two_ints(req):
    #print "Returning [%s + %s = %s]"%(req.a, req.b, (req.a + req.b))
    #return AddTwoIntsResponse(req.a + req.b)

#def add_two_ints_server():
    #rospy.init_node('add_two_ints_server')
    #s = rospy.Service('add_two_ints', AddTwoInts, handle_add_two_ints)
    #print "Ready to add two ints."
    #rospy.spin()

#if __name__ == "__main__":
    #add_two_ints_server()
