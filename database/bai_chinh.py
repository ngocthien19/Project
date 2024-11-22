import pandas as pd
import os
data = pd.read_csv(r"D:\VScode\Python\Project\database\Animal Dataset.csv")
selected_columns = ['Animal', 'Weight (kg)', 'Lifespan (years)', 'Diet', 'Habitat', 'Conservation Status']
selected_data = data[selected_columns]
# 1. loại bỏ các hàng có giá trị trống
selected_data = selected_data.dropna(how='any')
# 2. Chuẩn hóa các khoảng trắng
selected_data = selected_data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
# 3. Chuẩn hóa định dạng cột 'Weight (kg)' và 'Lifespan (years)' (giả sử có thể có khoảng giá trị)
#    Chỉ giữ giá trị trung bình của các khoảng giá trị
def clean_range(value):
    if isinstance(value, str):
        # Loại bỏ dấu phẩy nếu có
        value = value.replace(',', '').strip()
        if '-' in value:
            try:
                low, high = value.split('-')
                return (float(low) + float(high)) / 2
            except ValueError:
                return None
        if 'week' in value.lower():
            try:
                return float(value.split()[0]) / 52  # 1 năm có 52 tuần
            except ValueError:
                return None
        elif 'month' in value.lower():
            try:
                return float(value.split()[0]) / 12  # 1 năm có 12 tháng
            except ValueError:
                return None
        elif 'year' in value.lower():
            try:
                return float(value.split()[0])  # Chuyển đổi trực tiếp số năm
            except ValueError:
                return None
        
        # Nếu là giá trị số hợp lệ, chuyển sang float
        try:
            return float(value)
        except ValueError:
            return None  # Nếu không hợp lệ, trả về None
    return value
# hàm làm sạch cho các cột
selected_data['Weight (kg)'] = selected_data['Weight (kg)'].apply(clean_range)
selected_data['Lifespan (years)'] = selected_data['Lifespan (years)'].apply(clean_range)
#Loại bỏ các hàng trùng lặp (nếu có)
selected_data = selected_data.drop_duplicates()
# Lưu dataframe mới vào tệp CSV đã làm sạch
output_path = 'D:\VScode\Python\Project\database\Cleaned_Animal_Dataset.csv'
directory = os.path.dirname(output_path)
# Tạo thư mục nếu nó không tồn tại
if not os.path.exists(directory):
    os.makedirs(directory)
# Lưu dữ liệu đã làm sạch
# Loại bỏ các hàng trùng lặp (nếu cós) và loại bỏ hàng trống thêm lần nữa sau chuẩn hóa
selected_data = selected_data.dropna().drop_duplicates()
selected_data.to_csv(output_path, index=False)
print(f"Tệp đã được làm sạch và lưu tại: {output_path}")
