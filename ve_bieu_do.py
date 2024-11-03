import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu từ file CSV
df = pd.read_csv(r"D:\VScode\Python\Project\database\Cleaned_Animal_Dataset.csv")

# Tạo các khoảng cho cột "Weight (kg)"
bins = [0, 5, 10, 20, 50, 100, 200, 500]
labels = ['0-5 kg', '5-10 kg', '10-20 kg', '20-50 kg', '50-100 kg', '100-200 kg', '200-500 kg']
df['Weight Category'] = pd.cut(df['Weight (kg)'], bins=bins, labels=labels, right=False)

# Thiết lập kích thước và bố cục cho ba biểu đồ tròn
fig, axes = plt.subplots(1, 3, figsize=(30, 10))

# Danh sách các cột để vẽ biểu đồ (bao gồm cả cột mới)
columns_to_plot = ["Diet", "Weight Category", "Conservation Status"]

# Hàm tùy chỉnh để hiển thị % chỉ khi lớn hơn 5%
def custom_autopct(pct):
    return f'{pct:.1f}%' if pct >= 5 else ''

# Lặp qua từng cột để tạo biểu đồ tròn
for i, col in enumerate(columns_to_plot):
    # Tính toán số lượng giá trị cho từng loại trong cột
    value_counts = df[col].value_counts()
    
    # Vẽ biểu đồ tròn mà không có nhãn trực tiếp    
    wedges, _, autotexts = axes[i].pie(
        value_counts, labels=None, autopct=custom_autopct, startangle=90
    )
    
    # Điều chỉnh kích thước chữ của phần trăm trong biểu đồ
    for autotext in autotexts:
        autotext.set_fontsize(10)  # Tăng kích thước chữ của các % bên trong biểu đồ
    
    # Tạo legend bên dưới mỗi biểu đồ
    axes[i].legend(wedges, value_counts.index, title=col, loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=2, fontsize=12)

# Hiển thị biểu đồ
plt.tight_layout()
plt.show()
