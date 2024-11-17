import matplotlib.pyplot as plt
import pandas as pd

def ConStatusChart():
    # Đọc dữ liệu từ file CSV đã làm sạch
    data = pd.read_csv("Cleaned_Animal_Dataset.csv")

    # Đếm tần suất của từng trạng thái bảo tồn
    status_counts = data["Conservation Status"].value_counts()

    # Hàm hiển thị phần trăm chỉ khi giá trị lớn hơn 5%
    def autopct_func_status(pct):
        return f'{pct:.1f}%' if pct > 5 else ''  # Hiển thị 1 chữ số thập phân nếu > 5%

    # Tạo biểu đồ tròn
    plt.figure(figsize=(10, 6))  # Điều chỉnh kích thước hợp lý với chiều rộng 10 và chiều cao 6
    wedges, texts, autotexts = plt.pie(
        status_counts,
        labels=None,  # Không hiển thị nhãn trực tiếp trên biểu đồ
        autopct=autopct_func_status,  # Hiển thị % cho các phần có giá trị lớn hơn 5%
        startangle=90,  # Xoay biểu đồ để bắt đầu từ góc 90 độ
        colors=plt.cm.tab20.colors  # Sử dụng bảng màu 'tab20'
    )

    # Thêm tiêu đề biểu đồ
    plt.title('Proportion of Conservation Status', fontsize=14)

    # Thêm chú thích bên phải biểu đồ
    plt.legend(
        wedges,  # Truyền các phần (wedges) vào chú thích
        status_counts.index,  # Tên của các trạng thái bảo tồn
        title="Conservation Status",  # Tiêu đề của chú thích
        loc="center left",  # Đặt chú thích ở bên trái
        bbox_to_anchor=(1, 0, 0.5, 1)  # Định vị trí của chú thích
    )

    # Tự động điều chỉnh bố cục để không bị chèn lấn
    plt.tight_layout()

    # Hiển thị biểu đồ
    plt.show()