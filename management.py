import csv
import os
import tkinter as tk
from tkinter import font, messagebox 
from features import Table
from button_radius import create_rounded_button


def Submit(entries):
    data = [entry.get() for entry in entries]

    file_path = r"D:\VScode\Python\Project\database\Cleaned_Animal_Dataset.csv"

    # Kiểm tra xem file CSV đã tồn tại hay chưa
    file_exists = os.path.isfile(file_path)

    try:
        # Ghi vào file CSV
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Chỉ viết tiêu đề nếu file mới
            if not file_exists:
                writer.writerow(["Animal", "Weight (kg)", "Lifespan (years)", "Diet", "Habitat", "Conservation Status"])

            writer.writerow(data)  # Ghi từng dòng dữ liệu vào file CSV

        # Xóa các mục sau khi gửi
        for entry in entries:
            entry.delete(0, tk.END)

        # Cập nhật bảng (Treeview)
        Table().insert("", "0", values=data)  # Thêm dữ liệu mới vào Table

        # Hiển thị thông báo thành công
        messagebox.showinfo("Success", "✅ Submit Successfully!")
        

    except Exception as e:
        # Hiển thị thông báo thất bại nếu có lỗi
        messagebox.showerror("Error", "❌ Submit Failure!" + str(e))

def back_to_home():
    managementPage.destroy()
    
def ManagementPage(root):
    # Tạo khung chính
    global managementPage
    managementPage = tk.Toplevel()
    managementPage.title("Animal Management")
    managementPage.geometry("900x500")
    managementPage.configure(bg='#ECF0F1')  

    # Fonts
    header_font = font.Font(family="Arial", size=22, weight="bold")  
    label_font = font.Font(family="Arial", size=14, weight="normal")
    button_font = font.Font(family="Arial", size=14, weight="normal")

    # Tiêu đề của management page
    title_label = tk.Label(managementPage, text="ANIMAL MANAGEMENT", bg="#ECF0F1", fg="#2980b9", font=header_font)
    title_label.pack(pady=(5, 30)) 

    # Tạo frame 
    frame_add = tk.Frame(managementPage, width=800, height=250, bg="#FFF")
    frame_add.pack(pady=10) 
    
    # Các trường nhập liệu
    fields = [("Animal", ""), 
              ("Weight (kg)", ""), 
              ("Lifespan (years)", ""), 
              ("Diet", ""), 
              ("Habitat", ""), 
              ("Conservation Status", "")]
    
    entries = []  # Danh sách để lưu trữ các entry
    for field in fields:
        # Tạo frame chứa label và entry với chiều cao cố định
        frame_entry = tk.Frame(frame_add, bg="white", height=40)
        frame_entry.pack(padx=20, pady=5, fill=tk.X)  # fill=tk.X để mở rộng đầy chiều rộng

        label = tk.Label(frame_entry, text=field[0] + ":", bg="white", font=label_font, width=20)
        label.pack(side=tk.LEFT)

        entry = tk.Entry(frame_entry, font=button_font, width=30)  # Đặt width cho entry
        entry.pack(side=tk.LEFT, padx=(10, 0))
        
        entries.append(entry)  # Thêm entry vào danh sách

    # Thêm nút Add
    canvas_add = tk.Canvas(frame_add, width=100, height=50, bg="#FFF", highlightthickness=0)
    canvas_add.pack(pady=(10, 5), side=tk.RIGHT)  # Căn chỉnh nút ở góc phải dưới cùng

    # Tạo nút bo góc
    create_rounded_button(
        canvas_add, 
        x=5, 
        y=5, 
        width=90, 
        height=40, 
        radius=10, 
        text="➕ Add",
        command=lambda: Submit(entries)
    )


    # Tạo canvas và nút "Back Home" 
    canvas_back = tk.Canvas(managementPage, width=150, height=70, bg="white", highlightthickness=0)
    canvas_back.pack(pady=(30, 10))  # Căn chỉnh nút ở giữa

    # Nút "Back Home" với kích thước lớn hơn
    create_rounded_button(
        canvas_back, 
        x=5, 
        y=5, 
        width=140, 
        height=60,  
        radius=15,  
        text="Back to Home",
        command=back_to_home,
        bg_color="#FFF", 
        text_color="#e74c3c", 
        hover_bg_color="#e74c3c", 
        hover_text_color="black"
    )
    # Sự kiện enter để Submit
    managementPage.bind('<Return>', lambda event: Submit(entries))
