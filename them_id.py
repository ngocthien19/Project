import pandas as pd

# Đọc file CSV hiện có
file_path = r"D:\VScode\Python\Project\database\Cleaned_Animal_Dataset.csv"
data = pd.read_csv(file_path)

# Thêm cột ID với giá trị từ 1 đến số hàng trong DataFrame
data.insert(0, 'ID', range(1, 1 + len(data)))

# Ghi lại vào file CSV, ghi đè file cũ với cột ID mới
data.to_csv(file_path, index=False)

print("Đã thêm cột ID vào file CSV thành công.")