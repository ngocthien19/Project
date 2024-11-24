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

    # Danh sách các label và entry tương ứng (bỏ qua id)
    labels = ["Animal: ", "Weight (kg): ", "Lifespan (years): ", "Diet: ", "Habitat: ", "Conservation Status: "]
    entries = []

    # Tạo các label và entry, chỉ cho phép chỉnh sửa Weight và Lifespan
    for i, label in enumerate(labels):
        frame = tk.Frame(modal, bg="#FFF")
        frame.pack(pady=5)

        label_widget = tk.Label(frame, text=label, bg="#FFF", width=20, font=("Arial", 14, "normal"))
        label_widget.pack(side=tk.LEFT)

        entry_widget = tk.Entry(frame, width=30, font=("Arial", 14, "normal"))
        entry_widget.pack(side=tk.LEFT)
        entry_widget.insert(1, item_data[i + 1])  # Điền dữ liệu vào entry, bỏ qua ID
        
        # Disable các trường ngoài Weight và Lifespan
        if i != 1 and i != 2:  # Chỉ cho phép chỉnh sửa Weight và Lifespan
            entry_widget.config(state='disabled')
        
        entries.append(entry_widget)  # Thêm entry vào danh sách

    def update_item():
        # Lấy dữ liệu cập nhật từ các trường
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

            # Lấy chỉ số của dòng trong Treeview để cập nhật DataFrame
            row_index = int(table.index(selected_item[0]))

            # Lấy `ID` của hàng đang cập nhật
            current_id = item_data[0]  # Giữ ID từ dữ liệu đã chọn

            # Cập nhật dữ liệu cho hàng tương ứng trong DataFrame
            data.iloc[row_index, 1:] = updated_data  # Cập nhật tất cả các cột trừ ID

            # Ghi lại DataFrame vào file CSV
            data.to_csv(r"D:\VScode\Python\Project\database\Cleaned_Animal_Dataset.csv", index=False)

            # Thêm ID vào đầu danh sách `updated_data` để hiển thị đầy đủ trong Treeview
            updated_data_with_id = [current_id] + updated_data

            # Cập nhật lại dữ liệu trong Treeview
            table.item(selected_item, values=updated_data_with_id)  # Cập nhật giá trị hiển thị trong Treeview
            modal.destroy()  # Đóng modal
            messagebox.showinfo("Success", "✅ Update Successful!")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Update Failed! {str(e)}")

    # Tạo khung cho các nút
    button_frame = tk.Frame(modal, bg="#FFF")
    button_frame.pack(pady=(10, 20), padx=10, anchor=tk.SE)  # Đặt khung ở góc dưới bên phải

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

    # Gắn sự kiện Enter để thực hiện cập nhật
    modal.bind('<Return>', lambda event: update_item())

def Update(table):
    # Lấy mục được chọn từ Treeview
    global selected_item
    selected_item = table.selection()
    if selected_item:
        item_values = table.item(selected_item)['values']  # Lấy giá trị của hàng đã chọn
        show_update_item_details(item_values, table)  # Hiện modal với thông tin chi tiết để cập nhật
    else:
        messagebox.showwarning("Warning", "Vui lòng chọn một mục từ danh sách.")