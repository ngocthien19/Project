import matplotlib.pyplot as plt
import pandas as pd

def WeightChart():
    # Đọc dữ liệu từ file csv đã làm sạch
    data = pd.read_csv(r"D:\VScode\Python\Project\database\Cleaned_Animal_Dataset.csv")

    # Thiết lập kích thước cho biểu đồ
    plt.figure(figsize=(8, 5))  # Tạo khung vẽ với chiều rộng 8 và chiều cao 5

    # Vẽ biểu đồ histogram để thể hiện phân bố cân nặng của động vật
    plt.hist(
        data['Weight (kg)'].dropna(),  # Lấy dữ liệu từ cột 'Weight (kg)' và loại bỏ các giá trị bị thiếu (NaN)
        bins=10,  # Chia dữ liệu thành 10 khoảng (bins) để vẽ biểu đồ
        color='skyblue',  
        edgecolor='black',  # Viền của các cột có màu đen
        rwidth=0.9  
    )

    # Thêm tiêu đề và nhãn cho biểu đồ
    plt.title('Distribution of Animal Weights', fontsize=14) 
    plt.xlabel('Weight (kg)', fontsize=12)  
    plt.ylabel('Frequency', fontsize=12)

    # Thêm lưới vào biểu đồ
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Thêm lưới trên trục Y với đường nét đứt và độ mờ 0.7

    # Điều chỉnh bố cục để không bị chèn các thành phần
    plt.tight_layout()  # Đảm bảo bố cục tự động điều chỉnh khoảng cách giữa các thành phần trong biểu đồ

    # Hiển thị biểu đồ
    plt.show()  
