import serial



# ser = serial.Serial('/dev/ttyS1', 9600, timeout=1)
# ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
# ser = serial.Serial('/dev/ttyUSB2', 9600, timeout=1)
ser = serial.Serial('COM3', 9600, timeout=1)



def read_serial():
    while True:
        try:
            bytetoread = ser.in_waiting
            if bytetoread > 0:
                msg = ser.readline().strip().decode('utf-8')
                # msg2 = ser.readline().strip()
                print(msg)
                # print(msg2)
                # if msg == "exit":
                    # return
        except serial.SerialException:
            break
            
            
if __name__ == "__main__":
    read_serial()
    ser.close()