import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from button_radius import create_rounded_button

def ChartPage(root):
    global chartPage
    chartPage = tk.Toplevel(root)
    chartPage.title("Chart")
    chartPage.attributes("-fullscreen", True)
    chartPage.config(bg="#FFF")

    # Đặt tiêu đề chính
    title_label = tk.Label(chartPage, text="CHART", font=("Arial", 22, "bold"), bg="#FFF", fg="#2980b9")
    title_label.pack(pady=(20, 0))

    # Đọc dữ liệu từ file CSV
    df = pd.read_csv(r"D:\VScode\Python\Project\database\Cleaned_Animal_Dataset.csv")

    # Tạo các khoảng cho cột "Weight (kg)"
    bins = [0, 5, 10, 20, 50, 100, 200, 500]
    labels = ['0-5 kg', '5-10 kg', '10-20 kg', '20-50 kg', '50-100 kg', '100-200 kg', '200-500 kg']
    df['Weight Category'] = pd.cut(df['Weight (kg)'], bins=bins, labels=labels, right=False)

    # Tạo Figure và Axes cho biểu đồ
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))  # Giảm kích thước chiều cao

    # Danh sách các cột để vẽ biểu đồ
    columns_to_plot = ["Diet", "Weight Category", "Conservation Status"]

    # Hàm tùy chỉnh để hiển thị % chỉ khi lớn hơn 5%
    def custom_autopct(pct):
        return f'{pct:.1f}%' if pct >= 5 else ''

    # Lặp qua từng cột để tạo biểu đồ tròn
    for i, col in enumerate(columns_to_plot):
        value_counts = df[col].value_counts()
        
        # Vẽ biểu đồ tròn
        wedges, _, autotexts = axes[i].pie(
            value_counts, labels=None, autopct=custom_autopct, startangle=90
        )
        
        # Điều chỉnh kích thước chữ của phần trăm trong biểu đồ
        for autotext in autotexts:
            autotext.set_fontsize(10)
        
        # Tạo legend bên dưới mỗi biểu đồ
        axes[i].legend(
            wedges, 
            value_counts.index, 
            title=col, 
            loc="upper center", 
            bbox_to_anchor=(0.5, -0.02),  # Điều chỉnh vị trí chú thích để gần biểu đồ hơn
            ncol=2, 
            fontsize=12
        )

    # Nhúng Figure vào trong Tkinter, căn giữa theo chiều dọc
    canvas = FigureCanvasTkAgg(fig, master=chartPage)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=(0, 5))  # Khoảng cách phía dưới để chừa chỗ cho nút Back

    # Tạo canvas và nút "Back to Home" đặt ở dưới cùng
    canvas_back = tk.Canvas(chartPage, width=150, height=70, bg="white", highlightthickness=0)
    canvas_back.pack(side=tk.BOTTOM, pady=10)  # Đặt nút ở dưới cùng với khoảng cách

    create_rounded_button(
        canvas_back, 
        x=5, 
        y=5, 
        width=140, 
        height=60,  
        radius=15,  
        text="Back to Home",
        command=lambda: chartPage.destroy(),
        bg_color="#FFF", 
        text_color="#e74c3c", 
        hover_bg_color="#e74c3c", 
        hover_text_color="black"
    )

    # Ngăn ChartPage điều chỉnh kích thước các widget con, đảm bảo đủ không gian cho nút Back
    chartPage.pack_propagate(False)