#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseActionGoal, MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus
from kobuki_ui.srv import GetStationList


from std_msgs.msg import String

queue_status = 0
name_list = []
emergency_flag = False

def move_base_callback(state, result):
    rospy.loginfo("queue_move: move_base_callback: Running move_base_callback")
    if state == actionlib.GoalStatus.SUCCEEDED:
        rospy.loginfo("queue_move: move_base_callback: Robot arrived at the goal successfully!")
        arrivegoal.publish("arrived")
    else:
        rospy.loginfo("queue_move: move_base_callback: Robot failed to reach the goal!")
    
    rospy.loginfo("queue_move: move_base_callback: Finish move_base_callback")
 


def send_goal_execute(x,y,z,qx,qy,qz,qw):
    rospy.loginfo("queue_move: running send_goal_execute")
    move_base_client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    move_base_client.wait_for_server()
    global emergency_flag
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

    move_base_client.send_goal(goal, done_cb=move_base_callback)

    rospy.loginfo("queue_move: send_goal_execute: finish send_goal_execute")

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
    rospy.loginfo('queue_move: running handle_move_list with {}'.format(data.data))
    global name_list
    station_list_dict = rospy.get_param('station_list/stations', {})
    name_list = data.data.split(':')
    name_list.pop(0)

    set_param_queue_list(name_list)
    

    while name_list:
        name = name_list[0]
        for element in station_list_dict:
            if element['name'] == name:
                rospy.loginfo('queue_move: handle_move_list: Sending {} with x={}, y={} to move_base'.format(element['name'],element['positionX'], element['positionY']))
                send_goal_execute(element['positionX'], element['positionY'], element['positionZ'], 
                                    element['orientationX'], element['orientationY'], element['orientationZ'], element['orientationW'])
                break
        name_list.pop(0)
        rospy.loginfo('queue_move: handle_move_list: Waiting for recieve_confirm')
        rospy.wait_for_message('goal/recieve_confirm', String)
        
        set_param_queue_list(name_list)
    
    rospy.loginfo("queue_move: handle_move_list: Finish handle_move_list")
            
def handle_emergency(data):
    global name_list
    # global emergency_flag
    rospy.loginfo('queue_move: handle_emergency: Running handle_emergency  ')
    # Stop all move_base action
    # emergency_flag = not emergency_flag
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.cancel_all_goals()

    # Delete all positions in the queue
    name_list = []
    set_param_queue_list(name_list)
    rospy.loginfo('queue_move: handle_emergency: Name_list now is {} and move_base status is {} '.format(name_list, client.get_state()))
    rospy.loginfo('queue_move: handle_emergency: Finish handle_emergency with ')


# def goal_recieved(data):
    # global queue_status
    # rospy.wait_for_message
    # if data.data == "recieved":
    # rospy.loginfo('queue_move: goal_recieved: Running goal_recieved')
        # queue_status = 0



if __name__ == '__main__':
  
    rospy.init_node('queue_move')
    # print("queue print")
    rospy.loginfo("Running queue_move")
    rospy.set_param('queue_list/queues', "empty")
    arrivegoal = rospy.Publisher("goal/arrive", String, queue_size=10)
    # rospy.Subscriber("goal/recieved", String, goal_recieved)
    rospy.Subscriber('goal/move', String, handle_move_list)
    rospy.Subscriber('goal/emergency', String,handle_emergency)



    rospy.spin()


