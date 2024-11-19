import csv
import os
import tkinter as tk
from tkinter import font, messagebox, ttk
from features import Table
from button_radius import create_rounded_button

def get_unique_values(file_path, column_name):
    """Hàm để lấy các giá trị duy nhất từ một cột trong file CSV."""
    values = set()
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                values.add(row[column_name].strip())
    except Exception as e:
        messagebox.showwarning("Exist File", "File not found")
    return sorted(values)  # Sắp xếp giá trị duy nhất để dễ nhìn

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

    # Thu thập dữ liệu từ các `Entry` và `Combobox` (bỏ qua ID)
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

    # Kiểm tra trùng lặp trước khi thêm vào file CSV
    if file_exists:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)  # Đọc toàn bộ file vào một danh sách
            
            # Chuẩn hóa dữ liệu đầu vào để so sánh chính xác hơn
            normalized_data = [str(value).strip().lower() for value in data]
            
            for row in rows[1:]:  # Bỏ qua dòng tiêu đề
                # Chuẩn hóa hàng dữ liệu từ CSV
                normalized_row = [str(cell).strip().lower() for cell in row[1:]]  # Bỏ qua ID
                
                if normalized_row == normalized_data:
                    messagebox.showwarning("Warning", "⚠️ Entry already exists. Please enter different information.")
                    return

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

        # Xóa dữ liệu trong các trường Entry và đặt Combobox về trạng thái mặc định
        for entry in entries:
            entry_type = type(entry)
            if entry_type == tk.Entry:
                entry.delete(0, tk.END)
            elif entry_type == ttk.Combobox:
                entry.set("")  # Đặt về trạng thái rỗng

        # Thêm dữ liệu vào Treeview
        Table().insert("", "0", values=data_with_id)  # Thêm dữ liệu mới vào Treeview

        # Hiển thị thông báo thành công
        messagebox.showinfo("Success", "✅ Submit Successfully!")
        
    except Exception as e:
        messagebox.showwarning("Warning", f"Submitted successfully. But please open the Feature window for better observation!")

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
    
    # Đường dẫn đến file CSV
    file_path = r"D:\VScode\Python\Project\database\Cleaned_Animal_Dataset.csv"

    # Lấy các giá trị duy nhất cho các combobox
    diet_options = get_unique_values(file_path, "Diet")
    habitat_options = get_unique_values(file_path, "Habitat")
    conservation_options = get_unique_values(file_path, "Conservation Status")

    # Các trường nhập liệu
    fields = [
        ("Animal", "entry"), 
        ("Weight (kg)", "entry"), 
        ("Lifespan (years)", "entry"), 
        ("Diet", "combobox", diet_options), 
        ("Habitat", "combobox", habitat_options), 
        ("Conservation Status", "combobox", conservation_options)
    ]
    
    entries = []  # Danh sách để lưu trữ các entry và combobox
    for field in fields:
        # Tạo frame chứa label và entry với chiều cao cố định
        frame_entry = tk.Frame(frame_add, bg="white", height=40)
        frame_entry.pack(padx=20, pady=5, fill=tk.X)  # fill=tk.X để mở rộng đầy chiều rộng

        label = tk.Label(frame_entry, text=field[0] + ":", bg="white", font=label_font, width=20)
        label.pack(side=tk.LEFT)

        if field[1] == "entry":
            entry = tk.Entry(frame_entry, font=button_font, width=30)  # Đặt width cho entry
        elif field[1] == "combobox":
            entry = ttk.Combobox(frame_entry, values=field[2], font=button_font, width=28, state="readonly")
        
        entry.pack(side=tk.LEFT, padx=(10, 0))
        entries.append(entry)  # Thêm entry hoặc combobox vào danh sách

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