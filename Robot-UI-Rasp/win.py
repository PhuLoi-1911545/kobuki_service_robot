import threading
import tkinter as tk
import serial
from tkinter import messagebox
# import pygame

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600

BUTTON_WIDTH = 10
BUTTON_HEIGHT = 3


# this is rasp
# ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
# this is ubuntu vmware
# ser = serial.Serial('/dev/ttyS1', 9600, timeout=1)
# this is window
ser = serial.Serial('COM5', 9600, timeout=1)
# ser = serial.Serial('COM1', 9600, timeout=1)

# pygame.init()
# notify_sound = pygame.mixer.Sound('notify.mp3')

function_list = ["Confirm", "Clear", "Refresh", "System", "Emergency", "Exit"]
room_list = ["Button 100", "Button 200", "Button 300", "Button 400"]
selected_rooms = []

web = 0

# def clearTextBox(textBox):
#     textBox.delete('0.0', tk.END)

def insertTextBox(textBox, msg):
    textDashBoard.yview_moveto(1.0)
    textBox.insert(tk.END, msg)

def send_serial(data):
    ser.write(data.encode('utf-8'))
    # print(data)

def read_serial():
    insertTextBox(textDashBoard,"Start recieving msg\n")
    # print("Start taking msg")
    while True:
        try:
            bytetoread = ser.in_waiting
            
            if bytetoread > 0:
                msg = ser.readline().strip().decode('utf-8')
                print(msg)
                
                if msg.startswith("addroom:"):
                    _, button_count, *new_room_list  = msg.split(":")
                    button_count = int(button_count)
                    global room_list
                    room_list = new_room_list [:button_count]
                    # room_list.sort()
                    root.after(0, draw_buttons)
                    insertTextBox(textDashBoard, "\nUpdate room list: " + " ".join(room_list) + "\n \n")
                    
                elif msg == "arrivedgoal":
                    insertTextBox(textDashBoard, "\nYour delivery has arrived \n")
                    arrive_goal()
                    
                elif msg.startswith("robot:"):
                    _, switch = msg.split(":")
                    if switch == "on":
                        insertTextBox(textDashBoard, "\nYour Robot Service is on \n")
                        messagebox.showinfo("Robot Service", "Robot Service is on")
                    else:
                        messagebox.showwarning("Robot Service", "Robot Service is already started")
                        insertTextBox(textDashBoard, "\n Robot Service is already started\n")
                        
                elif msg.startswith("web:"):
                    global web
                    _, switch = msg.split(":")
                    if switch == "on":
                        # web = 2
                        messagebox.showinfo("Web Admin", "Web Admin has started successfully")
                        insertTextBox(textDashBoard, "\nWeb Admin is on\n")
                    else:
                        messagebox.showwarning("Web Admin", "Web Admin is already started")
                        insertTextBox(textDashBoard, "\n Web Admin is already started\n")
                        # web = 0
                        # messagebox.showinfo("Web Admin", "Web Admin has turned off successfully")
                        # insertTextBox(textDashBoard, "\nWeb Admin is off\n")
            
        except serial.SerialException:
            break
        
        
def draw_buttons():
  
    for widget in middle_frame.winfo_children():
        widget.destroy()
        
    col = 0
    row = 0
    for _, button_name in enumerate(room_list):
        button = tk.Button(middle_frame, text=button_name, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        button.grid(row=row, column=col, pady=10, padx=3)
        button.config(command=lambda name=button_name: select_button(name))
        row += 1
        if row > 5:
            col += 1
            row = 0
        
def arrive_goal():
    notify_sound.play()
    messagebox.showinfo("Delivery Notification", "Please recieve your delivery")
    send_serial("recieved")
    
    
    
    
    # xu ly cac FUNCTION BUTTON
    
def select_button(button_name):
    global selected_rooms
    if button_name not in selected_rooms:
        if len(selected_rooms) == 0:
            insertTextBox(textDashBoard, "\nSelect rooms:"  + "\n")
        selected_rooms.append(button_name)
        insertTextBox(textDashBoard, "Room: " + button_name + "\n")
    else:
        messagebox.showerror("Error", "This room has been selected")


def confirm_send():
    global selected_rooms
    if len(selected_rooms) == 0:
        messagebox.showerror("Error", "No room is selected.")
        return
    rooms = "\n".join(selected_rooms)
    confirm = messagebox.askokcancel("Confirm", "Do you want to send the selected rooms ?\n" + rooms)
    if confirm:
        send_room_list()
        insertTextBox(textDashBoard, "\nThe selected rooms have been sent \n")
    
    
def send_room_list():
    global selected_rooms
    button_count = len(selected_rooms)
    button_list_msg = "move:{}:{}".format(button_count, ":".join(selected_rooms))
    send_serial(button_list_msg)
    selected_rooms = []
    messagebox.showinfo("Success", "The selected rooms have been sent.")
    
    
def clear_list():
    global selected_rooms 
    selected_rooms = []
    messagebox.showinfo("Success", "The selected rooms have been cleared.")
    insertTextBox(textDashBoard, "\nThe selected rooms have been cleared\n")
    
    
def refresh_list():
    send_serial("updatelist")
    insertTextBox(textDashBoard, "\nUpdating room list\n")


def popup():
    popup_window = tk.Toplevel()
    # popup_window.geometry(f"{popup_width}x{popup_height}")
    popup_window.geometry("400x200")
    popup_window.title("Robot System")
    
    button_width = int(400*0.03)
    button_height = int( 200*0.01)

    label = tk.Label(popup_window, text="Robot System Switches\n Robot Service: start robot auto service\n Web: Turn on Web connection for Admin")
    label.pack(pady=(2, 0), anchor="center")

    button_frame = tk.Frame(popup_window)
    button_frame.pack(side="top", fill="both")

    RobotService = tk.Button(button_frame, text="Robot Service", command=lambda: (robot_switch(), popup_window.destroy()), width=button_width, height=button_height)
    RobotService.pack(side="left", padx=10, pady=2)

    Web = tk.Button(button_frame, text="Web", command=lambda: (web_switch(), popup_window.destroy()), width=button_width, height=button_height)
    Web.pack(side="left", padx=10, pady=2)

    exit_button = tk.Button(button_frame, text="Exit", command=popup_window.destroy, width=button_width, height=button_height)
    exit_button.pack(side="left", padx=10, pady=2)
    
    
    
def robot_switch():
    confirm = messagebox.askokcancel(" Robot Service", "Do you want to turn on Robot Service ?\n" )
    if confirm:
        send_serial("robotstart")
        messagebox.showinfo(" Robot Service", " Robot Service is turning on")
        insertTextBox(textDashBoard, "\n Robot Service is starting\n")



def web_switch():
    confirm = messagebox.askokcancel("Web Admin", "Do you want to turn on Web Admin ?\n" )
    if confirm:
        send_serial("webon")
        messagebox.showinfo("Web Admin", "Web Admin is turning on")
        insertTextBox(textDashBoard, "\nWeb Admin is turning on\n")
        
        
    # global web
    # if web == 0:
    #     confirm = messagebox.askokcancel("Web Admin", "Do you want to turn on Web Admin ?\n" )
    #     if confirm:
    #         send_serial("webon")
    #         messagebox.showinfo("Web Admin", "Web Admin is turning on")
    #         insertTextBox(textDashBoard, "\nWeb Admin is turning on\n")
    #         web = 1
    # elif web == 1:
    #     messagebox.showinfo("Web Admin", "Web Admin is starting")
        
    # elif web == 2:
    #     # messagebox.showerror("Error", "Web Admin is running")
    #     confirm = messagebox.askokcancel("Web Admin", "Do you want to turn off Web Admin ?\n" )
    #     if confirm:
    #         send_serial("weboff")
    #         messagebox.showinfo("Web Admin", "Web Admin is turning off")
    #         insertTextBox(textDashBoard, "\nWeb Admin is turning off\n")
    #         web = 3

    # else: 
    #     messagebox.showinfo("Web Admin", "Web Admin is turning off")
    #     insertTextBox(textDashBoard, "\nWeb Admin is turning off\n")


def emergency():
    global selected_rooms 
    selected_rooms = []
    messagebox.showwarning("Emergency", "All tasks will be stop")
    insertTextBox(textDashBoard, "\nAll tasks will be stop \nThe selected room list has been clear\n")
    send_serial("emergency")
        
def exit():
    root.destroy()
    
   
def draw_function():
    for i, button_name in enumerate(function_list):
        button = tk.Button(right_frame, text=button_name, width=BUTTON_WIDTH*2, height=BUTTON_HEIGHT)
        # button.pack(side = "top", pady=10)
        button.grid(row=i, column=0, padx=20,pady=10)
        button.config(command=lambda name=button_name: run_function(name))
        button.config( borderwidth=7, relief="raised")


def run_function(name):
    if name == function_list[0]:
        confirm_send()
    elif name == function_list[1]:
        clear_list()
    elif name == function_list[2]:
        refresh_list()
    elif name == function_list[3]:
        popup()
    elif name == function_list[4]:
        emergency()
    elif name == function_list[5]:
        exit()
    else:
        messagebox.showerror("Error", "Nofunction here" + name)
        return

# Khởi tạo cửa sổ chính
root = tk.Tk()
root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
# root.attributes('-fullscreen',True)
frame_width = root.winfo_screenwidth()/3
frame_height = root.winfo_screenheight()/3


# Tạo khung chứa phần trái
left_frame = tk.Frame(root, width=frame_width, height=frame_height)
left_frame.pack(side="left", fill="y")

# Tạo khung chứa phần giữa
middle_frame = tk.Frame(root, width=frame_width, height=frame_height)
middle_frame.pack(side="left", fill="y")

# Tạo khung chứa phần phải
right_frame = tk.Frame(root, width=frame_width, height=frame_height)
right_frame.pack(side="right", fill="y")


# Tạo widget Text để hiển thị thông tin 
textDashBoard = tk.Text(left_frame, wrap="word", width=30, height=30)
textDashBoard.grid(row=0, column=0)
scrollbar = tk.Scrollbar(left_frame, command=textDashBoard.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
textDashBoard.config(yscrollcommand=scrollbar.set)
# textDashBoard.yview_moveto(1.0)
# textDashBoard.see("end")


# Bắt đầu đọc dữ liệu serial trong một thread
serial_thread = threading.Thread(target=read_serial)
serial_thread.start()

# Vẽ các button và danh sách button ban đầu
draw_buttons()
draw_function()

# Bắt đầu vòng lặp chạy chương trình
root.mainloop()
# Đóng kết nối serial khi chương trình kết thúc
ser.close()
