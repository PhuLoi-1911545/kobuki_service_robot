#!/usr/bin/env python

import rospy
import serial
from nav_msgs.msg import OccupancyGrid

def map_callback(data):
    # Chuyển đổi dữ liệu map thành chuỗi để gửi qua cổng serial
    map_data_str = occupancy_grid_to_string(data)

    # Gửi dữ liệu qua cổng serial
    ser.write(map_data_str)

def occupancy_grid_to_string(occupancy_grid):
    # Chuyển đổi dữ liệu OccupancyGrid thành chuỗi phù hợp
    # Bạn cần xác định cách mã hóa dữ liệu sao cho phù hợp với ứng dụng Tkinter trên Raspberry Pi
    # Ví dụ: mã hóa dữ liệu dưới dạng base64
    map_data_str = base64.b64encode(occupancy_grid.data)
    return map_data_str

if __name__ == '__main__':
    rospy.init_node('send_map_data_node')

    # Cấu hình thông số cổng serial
    serial_port = rospy.get_param('~serial_port', '/dev/ttyUSB0')
    baud_rate = rospy.get_param('~baud_rate', 9600)
    ser = serial.Serial(serial_port, baud_rate)

    # Đăng ký callback với topic `/map`
    rospy.Subscriber('/map', OccupancyGrid, map_callback)

    rospy.spin()

