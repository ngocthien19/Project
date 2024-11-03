import tkinter as tk
import pandas as pd
from tkinter import messagebox 
from button_radius import create_rounded_button

def show_update_item_details(item_data, table):
    # Tạo cửa sổ modal
    modal = tk.Toplevel()
    modal.title("Update Animal Info")
    modal.geometry("600x400")
    modal.config(bg="#FFF")

    # Tiêu đề của modal
    title_label = tk.Label(modal, text="Update Animal Info", font=("Arial", 22, "bold"), bg="#FFF", fg="#2980b9")
    title_label.pack(pady=(10, 20))

    # Danh sách các label và entry tương ứng
    labels = ["Animal: ", "Weight: ", "Lifespan: ", "Diet: ", "Habitat: ", "Conservation Status: "]
    entries = []

    # Tạo các label và entry
    for i, label in enumerate(labels):
        frame = tk.Frame(modal, bg="#FFF")
        frame.pack(pady=5)

        label_widget = tk.Label(frame, text=label, bg="#FFF", width=20, font=("Arial", 14, "normal"))
        label_widget.pack(side=tk.LEFT)

        entry_widget = tk.Entry(frame, width=30, font=("Arial", 14, "normal"))
        entry_widget.pack(side=tk.LEFT)
        entry_widget.insert(0, item_data[i])  # Điền dữ liệu vào entry
        entries.append(entry_widget)  # Thêm entry vào danh sách

    def update_item():
        # Cập nhật dữ liệu trong Treeview
        updated_data = [entry.get() for entry in entries]
        
        # Chuyển đổi các giá trị trong `updated_data` thành kiểu phù hợp với DataFrame
        try:
            updated_data[1] = float(updated_data[1])  # Weight (kg) cần là float
            updated_data[2] = float(updated_data[2])  # Lifespan (years) cần là float
        except ValueError:  
            messagebox.showerror("Error", "Weight and Lifespan must be numbers.")
            return
            
        # Cập nhật dữ liệu trong CSV
        try:
            data = pd.read_csv(r"D:\VScode\Python\Project\database\Cleaned_Animal_Dataset.csv")
            index = table.index(selected_item)  # Lấy chỉ số của mục đã chọn
            data.iloc[index] = updated_data  # Cập nhật dữ liệu
            data.to_csv(r"D:\VScode\Python\Project\database\Cleaned_Animal_Dataset.csv", index=False)  # Ghi lại vào file CSV
            # Cập nhật lại dữ liệu trong Treeview
            table.item(selected_item, values=updated_data)
            modal.destroy()  # Đóng modal
            messagebox.showinfo("Success", "✅ Update Successful!")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Update Failed! {str(e)}")

    # Tạo khung cho các nút
    button_frame = tk.Frame(modal, bg="#FFF")
    button_frame.pack(pady=(10, 20), padx= 10,anchor=tk.SE)  # Đặt khung ở góc dưới bên phải

    # Tạo canvas cho nút Update
    update_canvas = tk.Canvas(button_frame, bg="#FFF", highlightthickness=0, width=100, height=50)
    update_canvas.pack(side=tk.RIGHT)  # Đặt nút Update bên phải

    create_rounded_button(
        update_canvas, 
        x=5, 
        y=5, 
        width=90, 
        height=40, 
        radius=10, 
        text="Update",
        command=update_item,  # Gọi hàm cập nhật
        bg_color="#f1c40f", text_color="#FFF", hover_bg_color="#f39c12", hover_text_color="#CCC"
    )

    # Tạo canvas cho nút Close và đặt bên phải nút Update
    canvas_close = tk.Canvas(button_frame, bg="#FFF", highlightthickness=0, width=100, height=50)
    canvas_close.pack(side=tk.RIGHT, padx=(5, 0))  # Đặt nút Close bên phải của nút Update

    create_rounded_button(
        canvas_close, 
        x=5,  
        y=5, 
        width=90, 
        height=40, 
        radius=10, 
        text="Close",
        command=modal.destroy,
        bg_color="#e74c3c", text_color="#FFF", hover_bg_color="#c0392b", hover_text_color="#CCC"
    )

def Update(table):
    # Lấy mục được chọn từ Treeview
    global selected_item
    selected_item = table.selection()
    if selected_item:
        item_values = table.item(selected_item)['values']  # Lấy giá trị của hàng đã chọn
        show_update_item_details(item_values, table)  # Hiện modal với thông tin chi tiết để cập nhật
    else:
        messagebox.showwarning("Warning", "Vui lòng chọn một mục từ danh sách.")