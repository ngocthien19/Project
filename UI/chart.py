import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from button_radius import create_rounded_button
from bieu_do.Weight import WeightChart
from bieu_do.Lifespan import LifespanChart
from bieu_do.Diet import DietChart
from bieu_do.habitat import HabitatChart
from bieu_do.con_status import ConStatusChart

def ChartPage(root):
    global chartPage, active_triangle, button_canvas
    chartPage = tk.Toplevel(root)
    chartPage.title("Chart")
    chartPage.geometry("1100x600")
    chartPage.config(bg="#FFF")

    active_triangle = None  # Biến lưu trạng thái tam giác active

    # Khung bên trái chứa các nút
    left_frame = tk.Frame(chartPage, bg="#ccc", width=250)
    left_frame.pack(side=tk.LEFT, fill=tk.Y)

    # Khung bên phải hiển thị biểu đồ
    right_frame = tk.Frame(chartPage, bg="#FFF", width=850)
    right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

    # Thêm nhãn "Show Chart" mặc định ở bên phải
    show_chart_label = tk.Label(right_frame, text="Show Chart", font=("Arial", 24, "bold"), bg="#FFF", fg="#888")
    show_chart_label.pack(expand=True)

    # Tiêu đề chính ở khung bên trái
    title_label = tk.Label(left_frame, text="CHARTS", font=("Arial", 18, "bold"), bg="#ccc", fg="#000")
    title_label.pack(pady=20)

    # Tạo Canvas cố định để chứa nút
    button_canvas = tk.Canvas(left_frame, bg="#f0f0f0", highlightthickness=0, width=250)
    button_canvas.pack(fill=tk.BOTH, expand=True)

    # Hàm hiển thị biểu đồ trong khung bên phải
    def show_chart(chart_func):
        # Xóa tất cả các widget cũ trong khung bên phải
        for widget in right_frame.winfo_children():
            widget.destroy()

        # Tạo khung chứa biểu đồ
        canvas_frame = tk.Frame(right_frame, bg="#FFF")
        canvas_frame.pack(expand=True, fill=tk.BOTH)

        # Gọi hàm biểu đồ và nhúng vào Tkinter
        fig = chart_func()
        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        
        # Căn chỉnh canvas biểu đồ chính giữa
        widget = canvas.get_tk_widget()
        widget.pack(expand=True)  # Dùng `expand=True` để căn giữa biểu đồ

    # Hàm để di chuyển tam giác đến nút đang active
    def move_triangle(y_position):
        global active_triangle

        # Xóa tam giác cũ nếu tồn tại
        if active_triangle:
            button_canvas.delete(active_triangle)

        # Vẽ tam giác tại vị trí mới
        active_triangle = button_canvas.create_polygon(
            5, y_position + 30,    # Điểm đầu bên trái
            20, y_position + 25,   # Đỉnh tam giác
            5, y_position + 20,     # Điểm cuối bên trái
            fill="#2980b9", outline=""
        )

    # Danh sách biểu đồ và các nút liên kết
    charts = [
        ("Weight Chart", WeightChart),
        ("Lifespan Chart", LifespanChart),
        ("Diet Chart", DietChart),
        ("Habitat Chart", HabitatChart),
        ("Conservation Chart", ConStatusChart),
    ]

    # Tạo các nút bo góc trên Canvas
    y_offset = 20  # Khoảng cách ban đầu từ trên xuống
    for index, (text, chart_func) in enumerate(charts):
        def on_click(cf=chart_func, offset=y_offset):
            show_chart(cf)  # Hiển thị biểu đồ
            move_triangle(offset)  # Di chuyển tam giác

        create_rounded_button(
            canvas=button_canvas,
            x=25,  # Căn lề trái
            y=y_offset,  # Khoảng cách dọc giữa các nút
            width=200,
            height=50,
            radius=15,
            text=text,
            command=on_click,
        )
        y_offset += 70  # Tăng vị trí dọc cho nút tiếp theo

    # Nút trở về màn hình chính
    create_rounded_button(
        canvas=button_canvas,
        x=25,
        y=y_offset,
        width=200,
        height=50,
        radius=15,
        text="Back to Home",
        command=lambda: chartPage.destroy(),
        bg_color="#E74C3C",
        text_color="#FFF",
        hover_bg_color="#C0392B",
        hover_text_color="#FFF"
    )
    