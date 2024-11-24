import tkinter as tk
from tkinter import font
from home import HomePage
from management import ManagementPage
from features import FeaturesPage
from chart import ChartPage

# Thiết lập các biến cho layout
window_width = 1200
window_height = 600
sidebar_width = int(window_width * 0.18)
button_width = int(sidebar_width * 0.8)
button_height = 40
button_radius = 15
canvas_width = sidebar_width + 20 
canvas_height = 50
sidebar_padding = 8
title_padding = 10

# Biến lưu trữ tam giác active
active_triangle = None
active_button_canvas = None

# Hàm chuyển sang trang khác và hiển thị nút đang active
def show_frame(frame_name, button_canvas=None):
    global active_triangle, active_button_canvas

    # Ẩn tất cả các khung
    for f in frames.values():
        f.pack_forget()

    # Hiển thị khung cần hiển thị
    frames[frame_name].pack(fill=tk.BOTH, expand=True)
    frames[frame_name].tkraise()  # Đưa khung cần hiển thị lên trên cùng

    # Nếu là các trang khác, tạo và hiển thị
    if frame_name == "Management":
        ManagementPage(frames["Management"]) 
        show_frame("Home", button_canvas=sidebar.winfo_children()[1])    
    elif frame_name == "Feature":
        FeaturesPage(frames["Feature"])
        show_frame("Home", button_canvas=sidebar.winfo_children()[1])    
    elif frame_name == "Chart":
        ChartPage(frames["Chart"])
        show_frame("Home", button_canvas=sidebar.winfo_children()[1])    

    # Xóa tam giác active cũ nếu có
    if active_triangle and active_button_canvas:
        active_button_canvas.delete(active_triangle)
    
    # Tạo tam giác mới cho nút đang active
    if button_canvas:
        active_triangle = button_canvas.create_polygon(
            20, 25,    # Điểm trái giữa
            10, 20,   # Đỉnh tam giác (mũi tên chỉ sang phải)
            10, 30,   # Điểm phải dưới
            fill="#2980b9", outline=""
        )
        active_button_canvas = button_canvas  # Cập nhật nút active mới

# Hàm tạo nút bo góc
def create_rounded_button(canvas, x, y, width, height, radius, text="", command=None):
    # Tạo hình dạng bo góc cho nút
    points = [x + radius, y, x + width - radius, y, x + width, y, x + width, y + radius, 
              x + width, y + height - radius, x + width, y + height, x + width - radius, y + height, 
              x + radius, y + height, x, y + height, x, y + height - radius, x, y + radius, x, y]
    
    # Vẽ nút bo góc trên canvas
    button = canvas.create_polygon(points, smooth=True, fill="#FFF", outline="#FFF")

    # Gán sự kiện click vào nút nếu có lệnh
    if command:
        canvas.tag_bind(button, "<Button-1>", lambda e: command())

    # Tạo và đặt văn bản cho nút ở giữa
    text_x = x + width / 2
    text_y = y + height / 2
    canvas.create_text(text_x, text_y, text=text, fill="#3498db", font=("Arial", 10, "bold"))

    return button

# Tạo hiệu ứng đổi màu cho nút khi hover và khi active
def animate_color_and_label(target, start_color, end_color, step=0):
    # Tính toán giá trị RGB của màu mới dựa trên màu bắt đầu và kết thúc
    r = int(start_color[1:3], 16) + step * (int(end_color[1:3], 16) - int(start_color[1:3], 16)) // 10
    g = int(start_color[3:5], 16) + step * (int(end_color[3:5], 16) - int(start_color[3:5], 16)) // 10
    b = int(start_color[5:7], 16) + step * (int(end_color[5:7], 16) - int(start_color[5:7], 16)) // 10
    new_color = f"#{r:02x}{g:02x}{b:02x}"

    # Cập nhật màu cho đối tượng đích
    if isinstance(target, tk.Canvas):
        canvas_id = target.button_id
        target.itemconfig(canvas_id, fill=new_color)
    elif isinstance(target, tk.Label):
        target.configure(bg=new_color, fg="white" if new_color == "#2980b9" else "#3498db")

    # Gọi lại hàm sau một khoảng thời gian để tiếp tục hiệu ứng
    if step < 10:
        target.after(7, animate_color_and_label, target, start_color, end_color, step + 1)

def run_main():
    # Tạo cửa sổ chính
    window = tk.Tk()
    window.title('Animals')
    window.geometry(f"{window_width}x{window_height}")
    window.configure(bg="white")

    # Các font chữ
    title_font = font.Font(family="Arial", size=14, weight="bold")
    button_font = font.Font(family="Arial", size=12, weight="normal")
    header_font = font.Font(family="Arial", size=18, weight="bold")

    # Khung sidebar
    global sidebar
    sidebar = tk.Frame(window, bg="#3498db", width=sidebar_width)
    sidebar.pack(side="left", fill="y")

    # Tiêu đề của sidebar
    title_label = tk.Label(sidebar, text="ANIMALS", bg="#2980b9", fg="white", font=header_font)
    title_label.pack(pady=(0, 20), ipady=title_padding, ipadx=(70))

    # Danh sách các nút bên sidebar
    buttons = [
        ("Home", "🏠", "#3498db"),
        ("Management", "🐾", "#3498db"),
        ("Feature", "🔄", "#3498db"),
        ("Chart", "📊", "#3498db"),
    ]

    # Tạo các trang nội dung
    global frames
    frames = {}
    for page in ["Home", "Management", "Feature", "Chart"]:
        frame = tk.Frame(window, bg="white")
        frame.pack(fill=tk.BOTH, expand=True)
        frames[page] = frame

    # Tạo trang Home và thêm vào frames
    HomePage(frames["Home"])

    # Tạo các nút trên sidebar
    for text, icon, color in buttons:
        # Canvas cho nút bo góc
        canvas = tk.Canvas(sidebar, width=canvas_width, height=canvas_height, bg="#3498db", highlightthickness=0)
        canvas.pack(pady=sidebar_padding)

        # Tạo nút bo góc
        button_id = create_rounded_button(
            canvas, 
            x=30, 
            y=5, 
            width=button_width, 
            height=button_height, 
            radius=button_radius, 
            text="",
            command=lambda t=text, c=canvas: show_frame(t, c)  # Truyền tên trang vào show_frame
        )
        
        # Lưu id của nút vào canvas
        canvas.button_id = button_id

        # Tạo nhãn chứa biểu tượng và văn bản
        button_label = tk.Label(canvas, text=f"{icon} {text}", bg="#FFF", fg=color, font=button_font)
        button_label.place(x=35, y=12)

        # Sự kiện click vào button_label để kích hoạt trang và hiệu ứng active
        button_label.bind("<Button-1>", lambda e, t=text, c=canvas: show_frame(t, c))

        # Hiệu ứng hover cho nút
        def on_enter(e, button_label=button_label, canvas=canvas):
            animate_color_and_label(canvas, "#ECF0F1", "#2980b9")
            animate_color_and_label(button_label, "#ECF0F1", "#2980b9")
            button_label.config(cursor="hand2")
            canvas.config(cursor="hand2")
            button_label.place(x=45, y=10)

        def on_leave(e, button_label=button_label, canvas=canvas):
            animate_color_and_label(canvas, "#2980b9", "#ECF0F1")
            animate_color_and_label(button_label, "#2980b9", "#ECF0F1")
            button_label.config(cursor="")
            canvas.config(cursor="")
            button_label.place(x=35, y=10)

        # Gán sự kiện hover cho nhãn
        button_label.bind("<Enter>", on_enter)
        button_label.bind("<Leave>", on_leave)
        canvas.tag_bind(button_id, "<Enter>", on_enter)
        canvas.tag_bind(button_id, "<Leave>", on_leave)

    # Hiển thị trang đầu tiên (Home)
    show_frame("Home", button_canvas=sidebar.winfo_children()[1])

    # Chạy ứng dụng
    window.mainloop()