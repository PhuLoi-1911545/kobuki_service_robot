#!/bin/bash
roslaunch kobuki_gazebo my_kobuki.launch &
sleep 20
rosrun robot_pose_publisher robot_pose_publisher