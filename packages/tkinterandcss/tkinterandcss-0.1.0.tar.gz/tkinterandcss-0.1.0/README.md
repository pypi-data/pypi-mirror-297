# tkinterandcss

Thư viện `tkinterandcss` cho phép bạn áp dụng các style CSS cho widget Tkinter, giúp việc tạo giao diện dễ dàng hơn.

## Cài đặt

Để cài đặt thư viện, hãy clone kho lưu trữ này và sử dụng pip:

git clone https://github.com/hqmdokkai/tkinterandcss.git
cd tkinterandcss
pip install .

Cách sử dụng
Dưới đây là cách sử dụng thư viện:

Tạo file CSS: Tạo một file style.css với nội dung như sau:

.button-primary {
    background-color: red;
    color: white;
    font-size: 16px;
    font-family: Arial;
    font-weight: bold;
    padding: 10px 20px;
    width: 150px;
    height: 50px;
    text-align: center;
    border: 2px solid black;
}
Tạo ứng dụng Tkinter: Tạo file Python (example.py) và thêm mã sau:

import tkinter as tk
from tkinterandcss import CssParser

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")

    css_parser = CssParser()
    css_parser.parse_file('style.css')

    button = tk.Button(root, text="Click Me")
    css_parser.apply_style(button, '.button-primary')
    button.pack(pady=20)

    root.mainloop()
Chạy ứng dụng: Chạy file main.py để xem giao diện với các style đã áp dụng.

Các thuộc tính hỗ trợ
Thư viện hỗ trợ một số thuộc tính CSS phổ biến:

background-color
color
font-size
font-family
font-weight
padding
width
height
text-align
border
Ghi chú
Thư viện này hỗ trợ các giá trị màu như tên màu CSS và mã hex.
Hãy đảm bảo rằng bạn đang sử dụng Python 3.6 trở lên.
Liên hệ
Nếu bạn có bất kỳ câu hỏi nào, hãy liên hệ với tôi qua email: akirasumeragi699@gmail.com