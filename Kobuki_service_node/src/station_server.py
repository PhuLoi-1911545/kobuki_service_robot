#!/usr/bin/env python

import rospy
from kobuki_ui.srv import GetStationList, GetStationListResponse, AddStation, AddStationResponse, DeleteStation, DeleteStationResponse
from kobuki_ui.msg import Station
import yaml

def handle_get_station_list(req):
    station_list_dict = rospy.get_param('station_list/stations', {})
    station_list = []
    for element in station_list_dict:
        station = Station()
        station.id = element['id']
        station.name = element['name']
        station.positionX = element['positionX']
        station.positionY = element['positionY']
        station.positionZ = element['positionZ']
        station.orientationX = element['orientationX']
        station.orientationY = element['orientationY']
        station.orientationZ = element['orientationZ']
        station.orientationW = element['orientationW']
        station_list.append(station)
    print("Request to service GetStationList success")
    return GetStationListResponse(station_list)

def handle_add_station(req):
    station_list_dict = rospy.get_param('station_list/stations', {})
    new_station = {
        'id': req.id,
        'name': req.name,
        'positionX': req.positionX,
        'positionY': req.positionY,
        'positionZ': req.positionZ,
        'orientationX': req.orientationX,
        'orientationY': req.orientationY,
        'orientationZ': req.orientationZ,
        'orientationW': req.orientationW
    }
    station_list = []
    for element in station_list_dict:
        station = {
                'id': element['id'],
                'name': element['name'],
                'positionX': element['positionX'],
                'positionY': element['positionY'],
                'positionZ': element['positionZ'],
                'orientationX': element['orientationX'],
                'orientationY': element['orientationY'],
                'orientationZ': element['orientationZ'],
                'orientationW': element['orientationW']
            }
        station_list.append(station)
    station_list.append(new_station)
    with open('/home/phuloi/catkin_ws/src/kobuki_ui/param/stations.yaml', 'w') as f:
        yaml.safe_dump(station_list, f)
    rospy.set_param('station_list/stations', station_list)
    print("Request to service AddStation success")
    return AddStationResponse(True)

def handle_delete_station(req):
    station_list_dict = rospy.get_param('station_list/stations', {})
    station_list = []
    found = False
    for element in station_list_dict:
        if element['id'] == req.id:
            found = True
            continue
        station = {
            'id': element['id'],
            'name': element['name'],
            'positionX': element['positionX'],
            'positionY': element['positionY'],
            'positionZ': element['positionZ'],
            'orientationX': element['orientationX'],
            'orientationY': element['orientationY'],
            'orientationZ': element['orientationZ'],
            'orientationW': element['orientationW']
        }
        station_list.append(station)
    if not found:
        return DeleteStationResponse(False)
    with open('/home/phuloi/catkin_ws/src/kobuki_ui/param/stations.yaml', 'w') as f:
        yaml.safe_dump(station_list, f)
    rospy.set_param('station_list/stations', station_list)
    print("Request to service DeleteStation success")
    return DeleteStationResponse(True)


def station_server():
    rospy.init_node('station_server')
    # Load stations from yaml file to rospram
    with open('//home/phuloi/catkin_ws/src/kobuki_ui/param/stations.yaml', 'r') as f:
        stations = yaml.safe_load(f)
    rospy.set_param('station_list/stations', stations)
    # Declare Get station list service
    s = rospy.Service('get_station_list', GetStationList, handle_get_station_list)
    # Declare Add station service
    s = rospy.Service('add_station', AddStation, handle_add_station)
    # Declare Add station service
    s = rospy.Service('delete_station', DeleteStation, handle_delete_station)
    print("Station server ready.")
    rospy.spin()

if __name__ == '__main__':
    station_server()

