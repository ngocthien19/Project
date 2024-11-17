import matplotlib.pyplot as plt
import pandas as pd

def DietChart():
    # Đọc dữ liệu đã làm sạch từ file CSV
    data = pd.read_csv(r"D:\VScode\Python\Project\database\Cleaned_Animal_Dataset.csv")

    # Đếm tần suất của từng chế độ ăn
    diet_counts = data['Diet'].value_counts()

    # Chỉ hiển thị % nếu giá trị lớn hơn 5%
    def autopct_func(pct):
        return f'{pct:.1f}%' if pct > 5 else ''

    # Thiết lập kích thước biểu đồ vừa với màn hình
    plt.figure(figsize=(10, 6))  # Điều chỉnh chiều rộng (10) và chiều cao (6) để vừa với màn hình

    # Tạo biểu đồ tròn
    wedges, texts, autotexts = plt.pie(
        diet_counts,
        labels=None,  # Không hiển thị nhãn trực tiếp trên biểu đồ
        autopct=autopct_func,  # Hiển thị phần trăm nếu > 5%
        startangle=90,  # Xoay biểu đồ để bắt đầu từ góc 90 độ
        colors=plt.cm.Paired.colors  # Sử dụng màu sắc từ bảng màu "Paired"
    )

    # Thêm tiêu đề biểu đồ
    plt.title('Proportion of Diet Types', fontsize=14)

    # Thêm chú thích bên phải biểu đồ
    plt.legend(
        wedges,
        diet_counts.index,  # Tên của các loại chế độ ăn
        title="Diet Types",  # Tiêu đề chú thích
        loc="center left",  # Đặt chú thích ở bên trái
        bbox_to_anchor=(1, 0, 0.5, 1)  # Định vị trí chú thích
    )

    # Đảm bảo bố cục vừa khít với kích thước màn hình
    plt.tight_layout()

    # Hiển thị biểu đồ
    plt.show()