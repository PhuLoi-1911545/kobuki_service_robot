#!/usr/bin/env python

import rospy
import serial
import subprocess
import threading
from std_msgs.msg import String
from kobuki_ui.srv import GetStationList, GetStationListRequest




process = None
#ser = serial.Serial('/dev/ttyS1', 9600, timeout=1)
ser = serial.Serial('/dev/ttyUSB2', 9600, timeout=1)

robot = False
web = False

def send_serial(data):
    ser.write(data.encode())

def read_serial():
    while not rospy.is_shutdown():
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            # rospy.loginfo(data)
            rospy.loginfo(data)
            if data.startswith('move:'):
                handle_send_station_list(data)
            elif data == "updatelist":
                handle_update_list()
            elif data == "webon":
                handle_web_on()
            # elif data == "weboff":
            #     handle_web_off()
            elif data == "recieved":
                handle_recieve_confirm()
            elif data == "emergency":
                handle_emergency()
            elif data == "robotstart":
                startup()
                


# hanle read serial data 
def handle_send_station_list(data):
    rospy.loginfo("serial_node: handle_send_station_list: running ")
    data = data.split(':')
    num_stations = int(data[1])
    stations =[]
    stations = data[2:]
    name_list = str(num_stations)
    for element in stations:
            name_list = name_list + ":" + str(element)
    rospy.loginfo('serial_node: handle_send_station_list: Received {} position : {}'.format(num_stations, stations))
    rospy.loginfo('serial_node: handle_send_station_list: Send room list: {}   to topic goal/move'.format(name_list))
    move_list.publish(name_list)
    rospy.loginfo("serial_node: handle_send_station_list: Finish handle_send_station_list")
  

# update danh sach rooms cho man hinh
def handle_update_list():
    rospy.loginfo("serial_node: handle_update_list: Running handle_update_list")
    rospy.wait_for_service('get_station_list')
    rospy.loginfo("serial_node: handle_update_list: Found service get_station_list")

    try:
        station_list = rospy.get_param('station_list/stations', {})
        rospy.loginfo("serial_node: handle_update_list: Got data from param service station_list/stations")
        name_list = "addroom:" + str(len(station_list))
        # print(name_list)
        for element in station_list:
            name_list = name_list + ":" + str(element['name'])
            # print(name_list)
        send_serial(name_list)

        rospy.loginfo("serial_node: handle_update_list: Finish handle_update_list")
        
    except rospy.ServiceException as e:
        print("update station failed: ", e)


# khoi chay trang web
def handle_web_on():
    global process
    global web
    if not web:
        rospy.loginfo('serial_node: handle_web_on: Web is starting')
        process = subprocess.Popen(['roslaunch', 'rosbridge_server', 'rosbridge_websocket.launch'])
        web = True
        send_serial("web:on")
    else:
        rospy.loginfo('serial_node: handle_web_on: Web is already running')
        send_serial("web:already")

def handle_web_off():
    global process
    rospy.loginfo('serial_node: turning off web')
    # process = subprocess.Popen(['pkill', '-f', 'node'])
    process.terminate()
    process = None
    send_serial("web:off")

def startup():
    global robot
    if not robot:
        rospy.loginfo('serial_node: startup: Robot service is starting')
        # process = subprocess.call(["~/catkin_ws/src/kobuki_ui/launch/startup.sh"])
        process = subprocess.call(['/bin/bash', '/home/khadas/catkin_ws/src/kobuki_ui/launch/startup.sh'])
        send_serial("robot:on")
        robot = True
    else:
        rospy.loginfo('serial_node: startup: Robot service is already started')
        send_serial("robot:already")


def handle_recieve_confirm():
    rospy.loginfo("serial_node: handle_recieve_confirm: Running handle_recieve_confirm")
    confirm_pub.publish("recieved")


def handle_emergency():
    rospy.loginfo('serial_node: handle_emergency: Runing handle_emergency')
    emergency.publish('emergency')





# handle write serial data
def goal_arrived(data):
    # if data.data == "arrived":
    rospy.loginfo("serial_node: goal_arrived: Running goal_arrived")
    # ser.write("arrivedgoal".encode())
    send_serial("arrivedgoal")

    rospy.loginfo("serial_node: goal_arrived: Finish goal_arrived")
   



 

if __name__ == '__main__':
    try:
        rospy.init_node('serial_node')
        rospy.loginfo('Running serial_node')
        confirm_pub = rospy.Publisher('goal/recieve_confirm', String, queue_size=10)
        move_list = rospy.Publisher('goal/move', String,  queue_size=10)
        emergency = rospy.Publisher('goal/emergency', String, queue_size=10)
        rospy.Subscriber('goal/arrive', String, goal_arrived)
        
        read_serial()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
