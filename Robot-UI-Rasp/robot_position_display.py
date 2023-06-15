import tkinter as tk
from PIL import Image, ImageTk
import serial
import base64

class RobotPositionApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Robot Position")
        self.geometry("800x600")

        self.image_label = tk.Label(self)
        self.image_label.pack(fill=tk.BOTH, expand=True)

        self.serial_port = '/dev/ttyUSB0'
        self.baud_rate = 9600
        self.ser = serial.Serial(self.serial_port, self.baud_rate)

        self.update_image()

    def update_image(self):
        # Đọc dữ liệu từ cổng serial
        try:
            serial_data = self.ser.readline().strip()
            if serial_data:
                self.serial_data = serial_data
        except:
            pass

        # Giả sử hàm 'get_image_from_serial_data' trả về một đối tượng PIL.Image
        image = self.get_image_from_serial_data(self.serial_data)
        if image:
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo
        # Lặp lại hàm update_image sau mỗi 100ms
        self.after(100, self.update_image)

    def get_image_from_serial_data(self, serial_data):
    # Xử lý dữ liệu từ cổng serial và trả về hình ảnh tương ứng
    # Ở đây, bạn cần viết mã xử lý để chuyển đổi dữ liệu serial thành một đối tượng PIL.Image
    # Giả sử dữ liệu serial đã được mã hóa dưới dạng base64
    try:
        # Giải mã dữ liệu base64
        occupancy_grid_data = base64.b64decode(serial_data)

        # Chuyển đổi dữ liệu OccupancyGrid thành hình ảnh
        # Sử dụng mã xử lý phù hợp với định dạng hình ảnh mà bạn muốn hiển thị
        image = occupancy_grid_to_image(occupancy_grid_data)
        return image
    except:
                return None

def occupancy_grid_to_image(self, occupancy_grid_data):
    # Chuyển đổi dữ liệu OccupancyGrid thành đối tượng PIL.Image
    # Bạn cần viết mã xử lý để chuyển đổi dữ liệu thành hình ảnh phù hợp
    # Ví dụ: chuyển đổi dữ liệu thành hình ảnh grayscale
    width =  # Chiều rộng của bản đồ
    height =  # Chiều cao của bản đồ

    # Chuyển đổi dữ liệu thành mảng 2D
    data_2d = np.reshape(occupancy_grid_data, (height, width))

    # Chuẩn hóa dữ liệu về đoạn [0, 255]
    normalized_data = (data_2d - data_2d.min()) / (data_2d.max() - data_2d.min()) * 255

    # Tạo đối tượng PIL.Image từ mảng 2D
    image = Image.fromarray(np.uint8(normalized_data), mode='L')

    return image


if __name__ == '__main__':
    app = RobotPositionApp()
    app.mainloop()

