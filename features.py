import tkinter as tk
import pandas as pd
from tkinter import font
from tkinter import ttk
from view import View
from update import Update
from delete import Delete
from button_radius import create_rounded_button

def populate_table(table, filter_value="", sort_by_weight=False):
    # Đọc dữ liệu từ file CSV
    try:
        data = pd.read_csv(r"D:\VScode\Python\Project\database\Cleaned_Animal_Dataset.csv")
    except FileNotFoundError:
        print("File không tồn tại. Vui lòng kiểm tra đường dẫn.")
        return
    
    if sort_by_weight:
        data = data.sort_values(by="Weight (kg)", ascending=True)

    # Xóa dữ liệu cũ trong bảng
    table.delete(*table.get_children())
    
    # Điền dữ liệu vào bảng, lọc theo giá trị nếu có
    for index, row in data.iterrows():
        if filter_value.lower() in row["Animal"].lower():
            table.insert("", "end", values=(index + 1, row["Animal"], row["Weight (kg)"], row["Lifespan (years)"], row["Diet"], row["Habitat"], row["Conservation Status"]))

def search_animals(event, entry, table):
    filter_value = entry.get()  # Lấy giá trị từ ô Entry
    populate_table(table, filter_value)  # Cập nhật bảng với giá trị tìm kiếm

    # Tự động chọn giá trị đầu tiên trong bảng nếu có
    if table.get_children():
        table.selection_set(table.get_children()[0])  # Chọn giá trị đầu tiên

def sort_by_weight(table):
    # Gọi hàm populate_table với sắp xếp theo cân nặng tăng dần
    populate_table(table, sort_by_weight=True)

def Table():
    return table

def back_to_home():
    featuresPage.destroy()

def FeaturesPage(root):
    global featuresPage
    featuresPage = tk.Toplevel()  
    featuresPage.title("Features")
    featuresPage.geometry("1300x600")
    featuresPage.config(bg="#FFF")

    # Fonts
    header_font = font.Font(family="Arial", size=22, weight="bold")  
    heading_font = font.Font(family="Arial", size=14, weight="bold")

    # Tiêu đề của management page
    title_label = tk.Label(featuresPage, text="ANIMAL LIST", bg="#FFF", fg="#2980b9", font=header_font)
    title_label.pack(pady=(5, 20)) 

    # Tạo khung cho bảng và thanh cuộn với grid layout
    frame = tk.Frame(featuresPage, width=1250, height=300)  # Chiều rộng cố định là 1150 và chiều cao cố định là 300
    frame.grid_propagate(False)  # Ngăn khung tự động điều chỉnh theo nội dung
    frame.pack(pady=(5, 20), padx=20)

    # Cho phép frame hiển thị theo chiều rộng cố định
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    
    # Tạo Treeview với số hàng cố định
    global table
    table = ttk.Treeview(frame, columns=("ID", "Animal", "Weight", "Lifespan", "Diet", "Habitat", "Conservation Status"), show="headings", height=10)

    # Khung cho ô tìm kiếm và nút search
    search_frame = tk.Frame(featuresPage, bg="#FFF")
    search_frame.pack(pady=(5, 20), padx=20, anchor="center")    

    # Sử dụng grid để đặt label, entry và button nằm trên cùng một dòng
    search_label = tk.Label(search_frame, text="Search Animal:", bg="#FFF", fg="#2980b9", font=heading_font)
    search_label.pack(side="left")  # Align to the west (left)

    # Ô Entry cho tìm kiếm
    search_entry = tk.Entry(search_frame, width=30, font=heading_font)
    search_entry.pack(side="left", padx=(10, 0))

    # Gắn sự kiện key release cho ô Entry
    search_entry.bind("<KeyRelease>", lambda event: search_animals(event, search_entry, table)) 

    # Cấu hình Treeview với phông chữ
    style = ttk.Style()
    style.configure("Treeview.Heading", font=heading_font, padding=(0, 5))  # Đặt font cho tiêu đề bản
    style.configure("Treeview", rowheight=25)  # Đặt khoảng cách chiều cao mỗi hàng cho nội dung bảng

    # Độ dài mỗi cột
    column_widths = {
        "ID": 50,
        "Animal": 200,
        "Weight": 150,
        "Lifespan": 150,
        "Diet": 200,
        "Habitat": 200,
        "Conservation Status": 200,
    }

    # Cấu hình Treeview
    for column, width in column_widths.items():
        table.column(column, width=width)
        table.heading(column, text=column, anchor="center")

    # Tạo thanh cuộn
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
    table.configure(yscroll=scrollbar.set)

    # Điền dữ liệu vào bảng
    populate_table(table)

    # Đặt bảng và thanh cuộn vào khung
    table.grid(row=0, column=0, sticky="nsew")  # Đặt trong grid và cho phép co giãn
    scrollbar.grid(row=0, column=1, sticky="ns")  # Thanh cuộn thẳng hàng với Treeview

    # Tạo nút CRUD
    button_canvas = tk.Canvas(featuresPage, bg="#FFF", highlightthickness=0, width=540, height=60)
    button_canvas.pack(pady=5, anchor="e")

    create_rounded_button(
        button_canvas, 20, 10, 100, 40, 20, "View", 
        command=lambda: View(table), bg_color="#3498db", text_color="#FFF", hover_bg_color="#2980b9", hover_text_color="#CCC"
    )
    create_rounded_button(
        button_canvas, 140, 10, 100, 40, 20, "Update", 
        command=lambda: Update(table), bg_color="#f1c40f", text_color="#FFF", hover_bg_color="#f39c12", hover_text_color="#CCC"
    )
    create_rounded_button(
        button_canvas, 260, 10, 100, 40, 20, "Delete", 
        command=lambda: Delete(table), bg_color="#e74c3c", text_color="#FFF", hover_bg_color="#c0392b", hover_text_color="#CCC"
    )
    create_rounded_button(
        button_canvas, 380, 10, 120, 40, 20, "Sort(Weight)", 
        command=lambda: sort_by_weight(table), bg_color="#8e44ad", text_color="#FFF", hover_bg_color="#732d91", hover_text_color="#CCC"
    )

    # Tạo canvas và nút "Back Home" 
    canvas_back = tk.Canvas(featuresPage, width=150, height=70, bg="white", highlightthickness=0)
    canvas_back.pack(pady=10)  # Căn chỉnh nút ở giữa

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