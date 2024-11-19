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
        messagebox.showerror("File Error", "File không tồn tại. Vui lòng kiểm tra đường dẫn.")
        return

    # Lấy danh sách ID của các hàng cần xóa từ các mục đã chọn
    selected_ids = []
    for item in selected_items:
        # Kiểm tra xem mục có tồn tại trong Treeview
        if not table.exists(item):
            print(f"Mục {item} không tồn tại trong Treeview.")
            continue
        
        # Lấy giá trị ID từ cột đầu tiên
        values = table.item(item, 'values')
        try:
            selected_ids.append(int(values[0]))  # Giả định ID nằm ở cột đầu tiên và là số nguyên
        except ValueError:
            print(f"Không thể chuyển đổi giá trị ID {values[0]} thành số nguyên.")

    # Xóa các hàng dựa vào ID trong DataFrame
    try:
        # Lọc bỏ các hàng có ID nằm trong danh sách selected_ids
        data = data[~data["ID"].isin(selected_ids)]
        data.to_csv(r"D:\VScode\Python\Project\database\Cleaned_Animal_Dataset.csv", index=False)
    except Exception as e:
        messagebox.showerror("Deletion Failed", f"Delete failed: {str(e)}")
        return

    # Xóa các hàng đã chọn khỏi Treeview
    for item in selected_items:
        if table.exists(item):
            table.delete(item)

    # Hiển thị thông báo thành công
    messagebox.showinfo("Success", "Selected items deleted successfully.")
