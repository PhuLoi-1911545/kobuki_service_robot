#!/usr/bin/env python
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseActionGoal, MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus
from kobuki_ui.srv import GetStationList
import serial
from std_msgs.msg import String

ser = serial.Serial('/dev/ttyS1', 9600, timeout=1)

def read_serial():
    while not rospy.is_shutdown():
        try:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()
                # rospy.loginfo(data)
                rospy.loginfo(data)
                if data.startswith('move:'):
                    rospy.loginfo("speaker: get data from serial: {}".format(data))
                    move_list.publish(data)
                    # handle_move_list(data)
        except serial.SerialException:
            break
                
           
def move_base_callback(state, result):
    rospy.loginfo("speaker: move_base_callback: Running move_base_callback")
    if state == actionlib.GoalStatus.SUCCEEDED:
        rospy.loginfo("speaker: move_base_callback: Robot arrived at the goal successfully!")
        arrivegoal.publish("arrived")
    else:
        rospy.loginfo("speaker: move_base_callback: Robot failed to reach the goal!")
    
    rospy.loginfo("speaker: move_base_callback: Finish move_base_callback")


def send_goal_execute(x,y,z,qx,qy,qz,qw):
    rospy.loginfo("speaker: running send_goal_execute")
    move_base_client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    move_base_client.wait_for_server()
    # global emergency_flag
    # while not emergency_flag:
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map" 
    # goal.target_pose.header.frame_id = "base_footprint" 
    goal.target_pose.header.stamp = rospy.Time.now()

    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.position.z = z

    goal.target_pose.pose.orientation.x = qx
    goal.target_pose.pose.orientation.y = qy
    goal.target_pose.pose.orientation.z = qz
    goal.target_pose.pose.orientation.w = qw

    # move_base_client.send_goal(goal, done_cb=move_base_callback)
    print(goal)

    rospy.loginfo("speaker: send_goal_execute: finish send_goal_execute")

def set_param_queue_list(name_list):
    if not name_list:
        rospy.set_param('queue_list/queues', "empty")
    else:
        queue_list = "queue"
        for element in name_list:
                queue_list = queue_list + ":" + str(element)
        rospy.set_param('queue_list/queues', queue_list)


def handle_move_list(data):
    # get_station_list = rospy.ServiceProxy('get_station_list', GetStationList)
    # response = get_station_list()
    rospy.loginfo('speaker: running handle_move_list with {}'.format(data))
    global name_list
    station_list_dict = rospy.get_param('station_list/stations', {})
    name_list = data.split(':')
    name_list.pop(0)

    set_param_queue_list(name_list)
    

    while name_list:
        name = name_list[0]
        for element in station_list_dict:
            if element['name'] == name:
                rospy.loginfo('speaker: handle_move_list: Sending {} with x={}, y={} to move_base'.format(element['name'],element['positionX'], element['positionY']))
                # send_goal_execute(element['positionX'], element['positionY'], element['positionZ'], 
                                    # element['orientationX'], element['orientationY'], element['orientationZ'], element['orientationW'])
                print(element)
                break
        name_list.pop(0)
        rospy.loginfo('speaker: handle_move_list: Waiting for recieve_confirm')
        rospy.wait_for_message('goal/recieve_confirm', String)
        
        set_param_queue_list(name_list)
    
    rospy.loginfo("speaker: handle_move_list: Finish handle_move_list")


if __name__ == '__main__':
    try:
        rospy.init_node('speaker_node')
        rospy.loginfo('Running speaker_node')
        arrivegoal = rospy.Publisher("/goal/arrive", String, queue_size=10)
        # confirm_pub = rospy.Publisher('goal/recieve_confirm', String, queue_size=10)
        move_list = rospy.Publisher('/goal/move', String,  queue_size=10)
        # emergency = rospy.Publisher('goal/emergency', String, queue_size=10)
        # rospy.Subscriber('goal/arrive', String, goal_arrived)
        
        read_serial()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass