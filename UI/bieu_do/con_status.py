import matplotlib.pyplot as plt
import pandas as pd

def ConStatusChart():
    # Chọn dữ liệu khi đã làm sạch để vẽ biểu đồ
    data = pd.read_csv(r"D:\VScode\Python\Project\database\Cleaned_Animal_Dataset.csv")

    # Đếm tần suất của từng trạng thái bảo tồn
    status_counts = data["Conservation Status"].value_counts()

    # Hàm hiển thị tỷ lệ nếu lớn hơn 5%
    def autopct_func_status(pct):
        return f'{pct:.1f}%' if pct > 5 else ''

    # Tạo đối tượng Figure
    fig, ax = plt.subplots(figsize=(6, 6))

    # Vẽ biểu đồ tròn
    wedges, texts, autotexts = plt.pie(
        status_counts,
        labels=None,  # Xóa nhãn khỏi biểu đồ
        autopct=autopct_func_status,
        startangle=90,
        colors=plt.cm.tab20.colors
    )

    # Tiêu đề
    plt.title('Proportion of Conservation Status', fontsize=14)

    # Chú thích bên tay phải (vẫn giữ nguyên)
    plt.legend(
        wedges,
        status_counts.index,
        title="Conservation Status",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1)
    )

    # Thêm hiệu ứng hover để hiển thị chú thích cho vùng dưới 5%
    def on_hover(event):
        for wedge, label in zip(wedges, status_counts.index):
            if wedge.contains(event)[0]:
                # Hiển thị chú thích cho vùng dưới 5% khi hover
                if status_counts[label] < 5:
                    plt.gca().set_title(f"Hovering over: {label} ({status_counts[label]}%)", fontsize=14)
                else:
                    plt.gca().set_title('Proportion of Conservation Status', fontsize=14)
                break  # Chỉ hiển thị một lần khi di chuột vào vùng này
        plt.draw()

    # Thiết lập sự kiện hover
    plt.gcf().canvas.mpl_connect('motion_notify_event', on_hover)

    # Điều chỉnh lề để tránh tràn nội dung
    plt.tight_layout()  # Tự động điều chỉnh các thành phần trong Figure để tránh bị cắt

    # Trả về đối tượng Figure
    return fig