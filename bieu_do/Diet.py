import matplotlib.pyplot as plt
import pandas as pd

def DietChart():
    # Đọc dữ liệu đã làm sạch từ file CSV
    data = pd.read_csv(r"D:\VScode\Python\Project\database\Cleaned_Animal_Dataset.csv")

    # Đếm tần suất của từng chế độ ăn
    diet_counts = data['Diet'].value_counts()

    # Hàm hiển thị tỷ lệ nếu lớn hơn 5%
    def autopct_func(pct):
        return f'{pct:.1f}%' if pct > 5 else ''

    # Tạo biểu đồ tròn
    plt.figure(figsize=(8, 8))

    # Vẽ biểu đồ tròn
    wedges, texts, autotexts = plt.pie(
        diet_counts,
        labels=None,  # Xóa nhãn khỏi biểu đồ
        autopct=autopct_func,
        startangle=90,
        colors=plt.cm.Paired.colors
    )

    # Tiêu đề
    plt.title('Proportion of Diet Types', fontsize=14)

    # Chú thích bên tay phải (vẫn giữ nguyên)
    plt.legend(
        wedges,
        diet_counts.index,
        title="Diet Types",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1)
    )

    # Thêm hiệu ứng hover để hiển thị chú thích cho vùng dưới 5%
    def on_hover(event):
        for wedge, label in zip(wedges, diet_counts.index):
            if wedge.contains(event)[0]:
                # Hiển thị chú thích cho vùng dưới 5% khi hover
                if diet_counts[label] < 5:
                    plt.gca().set_title(f"Hovering over: {label} ({diet_counts[label]}%)", fontsize=14)
                else:
                    plt.gca().set_title('Proportion of Diet Types', fontsize=14)
                break  # Chỉ hiển thị một lần khi di chuột vào vùng này
        plt.draw()

    # Thiết lập sự kiện hover
    plt.gcf().canvas.mpl_connect('motion_notify_event', on_hover)

    plt.tight_layout()
    plt.show()