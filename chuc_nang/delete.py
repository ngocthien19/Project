import tkinter as tk
import pandas as pd
from tkinter import messagebox 

def Delete(table):

    # Hiển thị hộp thoại xác nhận
    confirm = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete the selected items?")
    if not confirm:
        return  # Nếu người dùng chọn "No", thoát khỏi hàm
    
    # Lấy các hàng đang được chọn trong Treeview
    selected_items = table.selection()
    
    if not selected_items:
        messagebox.showwarning("No Selection", "No items selected for deletion.")
        return
    
    # Đọc dữ liệu từ file CSV
    try:
        data = pd.read_csv(r"D:\VScode\Python\Project\database\Cleaned_Animal_Dataset.csv")
    except FileNotFoundError:
        print("File không tồn tại. Vui lòng kiểm tra đường dẫn.")
        return

    # Tìm các chỉ số của các hàng cần xóa dựa vào các mục đã chọn trong bảng
    selected_rows = []
    for item in selected_items:
        # Kiểm tra xem mục có tồn tại trước khi truy xuất giá trị
        if not table.exists(item):
            print(f"Mục {item} không tồn tại trong Treeview.")
            continue
        
        # Lấy giá trị từ hàng đang được chọn
        values = table.item(item, 'values')
        
        # Tìm hàng trong DataFrame trùng với giá trị của mục đã chọn
        row = data[(data["Animal"] == values[1]) & 
                   (data["Weight (kg)"] == float(values[2])) & 
                   (data["Lifespan (years)"] == float(values[3])) & 
                   (data["Diet"] == values[4]) & 
                   (data["Habitat"] == values[5]) & 
                   (data["Conservation Status"] == values[6])]

        # Lấy chỉ số và thêm vào danh sách các hàng đã chọn để xóa
        if not row.empty:
            selected_rows.append(row.index[0])

    # xóa các hàng đã chọn từ DataFrame và lưu lại vào CSV
    try:
        data.drop(selected_rows, inplace=True)
        data.to_csv(r"D:\VScode\Python\Project\database\Cleaned_Animal_Dataset.csv", index=False)
    except Exception as e:
        messagebox.showerror("Deletion Failed", f"Delete failed: {str(e)}")
        return

    # Xóa các hàng đã chọn khỏi Treeview sau khi hoàn tất việc cập nhật
    for item in selected_items:
        if table.exists(item):
            table.delete(item)

    messagebox.showinfo("Success", "Selected items deleted successfully.")