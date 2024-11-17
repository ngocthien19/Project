import tkinter as tk
from button_radius import create_rounded_button
from bieu_do.Weight import WeightChart
from bieu_do.Lifespan import LifespanChart
from bieu_do.Diet import DietChart
from bieu_do.habitat import HabitatChart
from bieu_do.con_status import ConStatusChart

def ChartPage(root):
    global chartPage
    chartPage = tk.Toplevel(root)
    chartPage.title("Chart")
    chartPage.geometry("650x650")  # Tăng kích thước cửa sổ
    chartPage.config(bg="#FFF")

    # Đặt tiêu đề chính
    title_label = tk.Label(chartPage, text="CHART", font=("Arial", 22, "bold"), bg="#FFF", fg="#2980b9")
    title_label.pack(pady=(20, 10))

    # Canvas chứa các nút biểu đồ
    button_canvas = tk.Canvas(chartPage, bg="#FFF", height=400, highlightthickness=0, width=600)
    button_canvas.pack(pady=(10, 20))

    # Tạo các nút tương ứng với từng biểu đồ với 5 màu sắc khác nhau
    create_rounded_button(
        button_canvas,
        x=200,
        y=20,
        width=200,
        height=60,
        radius=15,
        text="Weight Chart",
        command=WeightChart,
        bg_color="#FF5733",  # Màu cam đậm
        text_color="#FFF",
        hover_bg_color="#C70039",  # Màu đỏ đậm
        hover_text_color="#FFF"
    )

    create_rounded_button(
        button_canvas,
        x=200,
        y=100,
        width=200,
        height=60,
        radius=15,
        text="Lifespan Chart",
        command=LifespanChart,
        bg_color="#33FF57",  # Màu xanh lá
        text_color="#FFF",
        hover_bg_color="#28B463",  # Màu xanh lá đậm
        hover_text_color="#FFF"
    )

    create_rounded_button(
        button_canvas,
        x=200,
        y=180,
        width=200,
        height=60,
        radius=15,
        text="Diet Chart",
        command=DietChart,
        bg_color="#3357FF",  # Màu xanh dương
        text_color="#FFF",
        hover_bg_color="#1F618D",  # Màu xanh dương đậm
        hover_text_color="#FFF"
    )

    create_rounded_button(
        button_canvas,
        x=200,
        y=260,
        width=200,
        height=60,
        radius=15,
        text="Habitat Chart",
        command=HabitatChart,
        bg_color="#FFC300",  # Màu vàng
        text_color="#000",
        hover_bg_color="#DAA520",  # Màu vàng đậm
        hover_text_color="#000"
    )

    create_rounded_button(
        button_canvas,
        x=200,
        y=340,
        width=200,
        height=60,
        radius=15,
        text="Conversation Chart",
        command=ConStatusChart,
        bg_color="#8E44AD",  # Màu tím
        text_color="#FFF",
        hover_bg_color="#6C3483",  # Màu tím đậm
        hover_text_color="#FFF"
    )

    # Thêm nút "Back to Home" trong một Canvas riêng
    back_canvas = tk.Canvas(chartPage, bg="#FFF", height=100, highlightthickness=0, width=600)
    back_canvas.pack(side=tk.BOTTOM, pady=10)  # Đặt Canvas ở cuối với khoảng cách padding

    # Tạo nút "Back to Home"
    create_rounded_button(
        back_canvas,
        x=200,
        y=20,
        width=200,
        height=60,
        radius=15,
        text="Back to Home",
        command=lambda: chartPage.destroy(),
        bg_color="#FFF",
        text_color="#e74c3c",
        hover_bg_color="#e74c3c",
        hover_text_color="black"
    )
