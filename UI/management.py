import csv
import os
import tkinter as tk
from tkinter import font, messagebox
from button_radius import create_rounded_button

def Submit(entries):
    # Đường dẫn đến file CSV
    file_path = r"D:\VScode\Python\Project\database\Cleaned_Animal_Dataset.csv"
    file_exists = os.path.isfile(file_path)

    # Tìm ID lớn nhất trong file CSV
    next_id = 1
    if file_exists:
        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                ids = [int(row[0]) for row in reader if row and row[0].isdigit()]  # Kiểm tra xem cột ID có phải là số
                next_id = max(ids) + 1 if ids else 1  # Tìm ID lớn nhất và cộng thêm 1
        except Exception as e:
            messagebox.showwarning("Exist File", "File not found")

    # Thu thập dữ liệu từ các `Entry` (bỏ qua ID)
    data = []
    for i, entry in enumerate(entries):
        value = entry.get().strip()
        
        # Nếu trường dữ liệu trống, hiển thị thông báo và dừng việc gửi
        if not value:
            messagebox.showwarning("Warning", f"⚠️ Please fill out all fields.")
            return

        # Kiểm tra kiểu dữ liệu cho "Weight (kg)" và "Lifespan (years)"
        if i == 1 or i == 2:  # Weight và Lifespan
            try:
                value = float(value)
            except ValueError:
                messagebox.showwarning("Warning", f"⚠️ '{entries[i].get()}' must be a valid number.")
                return
        else:  # Các trường còn lại yêu cầu là chuỗi ký tự
            if not isinstance(value, str) or value.isdigit():
                messagebox.showwarning("Warning", f"⚠️ '{entries[i].get()}' must be a valid text.")
                return

        data.append(value)

    # Thêm ID vào đầu danh sách dữ liệu trước khi ghi vào CSV
    data_with_id = [next_id] + data

    try:
        # Ghi dữ liệu vào file CSV bao gồm cả ID
        with open(file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            
            # Chỉ viết tiêu đề nếu file mới
            if not file_exists:
                writer.writerow(["ID", "Animal", "Weight (kg)", "Lifespan (years)", "Diet", "Habitat", "Conservation Status"])

            writer.writerow(data_with_id)  # Ghi dữ liệu với ID vào file CSV

        # Xóa dữ liệu trong các trường Entry
        for entry in entries:
            entry.delete(0, tk.END)

        # Hiển thị thông báo thành công
        messagebox.showinfo("Success", "✅ Submit Successfully!")
        
    except Exception as e:
        messagebox.showerror("Error", f"Submitted failure! {str(e)}")

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
    fields = [
        ("Animal", "entry"), 
        ("Weight (kg)", "entry"), 
        ("Lifespan (years)", "entry"), 
        ("Diet", "entry"), 
        ("Habitat", "entry"), 
        ("Conservation Status", "entry")
    ]
    
    entries = []  # Danh sách để lưu trữ các entry
    for field in fields:
        # Tạo frame chứa label và entry với chiều cao cố định
        frame_entry = tk.Frame(frame_add, bg="white", height=40)
        frame_entry.pack(padx=20, pady=5, fill=tk.X)  # fill=tk.X để mở rộng đầy chiều rộng

        label = tk.Label(frame_entry, text=field[0] + ":", bg="white", font=label_font, width=20)
        label.pack(side=tk.LEFT)

        entry = tk.Entry(frame_entry, font=button_font, width=30)  # Tạo Entry cho tất cả các trường
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
