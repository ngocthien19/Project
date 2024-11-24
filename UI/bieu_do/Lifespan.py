import matplotlib.pyplot as plt
import pandas as pd

def LifespanChart():
    # Đọc dữ liệu từ file CSV đã làm sạch
    data = pd.read_csv(r"D:\VScode\Python\Project\database\Cleaned_Animal_Dataset.csv")

    # Thiết lập kích thước biểu đồ
    plt.figure(figsize=(8, 5))  

    # Vẽ biểu đồ histogram để thể hiện phân bố tuổi thọ của động vật
    plt.hist(
        data['Lifespan (years)'].dropna(),  # Lấy dữ liệu từ cột 'Lifespan (years)' và loại bỏ giá trị NaN
        bins=10,  # Chia dữ liệu thành 10 nhóm (bins)
        color='lightgreen', 
        edgecolor='black',  # Viền của các cột có màu đen
        rwidth=0.9  
    )

    # Thêm tiêu đề và nhãn trục cho biểu đồ
    plt.title('Distribution of Animal Lifespan', fontsize=14) 
    plt.xlabel('Lifespan (years)', fontsize=12)  
    plt.ylabel('Frequency', fontsize=12) 

    # Thêm lưới dọc cho biểu đồ
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Lưới trên trục Y với đường nét đứt, độ mờ 0.7

    # Đảm bảo bố cục biểu đồ không bị chèn
    plt.tight_layout()  # Sử dụng `tight_layout` để tự động điều chỉnh khoảng cách giữa các thành phần

    # Hiển thị biểu đồ
    plt.show() 
