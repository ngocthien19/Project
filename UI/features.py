import tkinter as tk
import pandas as pd
from tkinter import font, ttk, messagebox
from chuc_nang.view import View
from chuc_nang.update import Update
from chuc_nang.delete import Delete
from button_radius import create_rounded_button

# Thêm các biến phân trang
rows_per_page = 10  # Số dòng hiển thị trên mỗi trang
current_page = 1  # Trang hiện tại
total_pages = 1  # Tổng số trang (sẽ được cập nhật dựa trên dữ liệu)

# Thêm khai báo biến toàn cục
sort_ascending = True  # Mặc định sắp xếp tăng dần

def populate_table(table, filter_value="", sort_by_weight=False, page=None):
    global current_page, total_pages
    
    # Đọc dữ liệu từ file CSV   
    try:
        data = pd.read_csv(r"D:\VScode\Python\Project\database\Cleaned_Animal_Dataset.csv")
    except FileNotFoundError:
        messagebox.showwarning("Exist File", "File not found")
        return

    # Áp dụng lọc nếu có
    if filter_value:
        data = data[data["Animal"].str.contains(filter_value, case=False, na=False)]
        current_page = 1  # Đặt lại trang hiện tại về trang 1 khi tìm kiếm
    else:
        # Chỉ cập nhật total_pages nếu không có filter_value
        total_pages = max(1, (len(data) + rows_per_page - 1) // rows_per_page)

    # Đặt lại trang hiện tại nếu không có giá trị page được cung cấp
    if page is not None:
        current_page = page

    # Chia trang dữ liệu
    start_row = (current_page - 1) * rows_per_page
    end_row = min(start_row + rows_per_page, len(data))

    # Nếu tìm kiếm, hiển thị toàn bộ kết quả, nếu không, chỉ hiển thị theo trang
    page_data = data if filter_value else data.iloc[start_row:end_row]

    # Sắp xếp dữ liệu của trang hiện tại nếu có yêu cầu
    if sort_by_weight:
        page_data = page_data.sort_values(by="Weight (kg)", ascending=sort_ascending)

    # Xóa dữ liệu cũ trong bảng
    table.delete(*table.get_children())

    # Điền dữ liệu cho trang hiện tại
    for index, row in page_data.iterrows():
        table.insert("", "end", values=(row["ID"], row["Animal"], row["Weight (kg)"], row["Lifespan (years)"], row["Diet"], row["Habitat"], row["Conservation Status"]))
    
    # Cập nhật trạng thái nút phân trang chỉ khi không có tìm kiếm
    if not filter_value:
        update_pagination_buttons()

def update_pagination_buttons():
    # Xóa các nút cũ nếu có
    for widget in pagination_frame.winfo_children():
        widget.destroy()

    # Tạo Canvas cho các nút phân trang
    pagination_canvas = tk.Canvas(pagination_frame, bg="#FFF", height=50, width=550, highlightthickness=0)
    pagination_canvas.pack(fill="x", pady=10)

    # Nút "Previous"
    create_rounded_button(
        pagination_canvas,
        x=10,
        y=10,
        width=80,
        height=30,
        radius=15,
        text="Previous",
        command=lambda: change_page(-1),
        bg_color="#3498db",
        text_color="#FFF",
        hover_bg_color="#2980b9",
        hover_text_color="#CCC"
    )

    # Các nút số trang
    max_display_pages = 3  # Số trang hiển thị liền kề
    if current_page <= max_display_pages:
        display_pages = list(range(1, max_display_pages + 1)) + ["..."] + [total_pages]
    elif current_page >= total_pages - max_display_pages + 1:
        display_pages = [1, "..."] + list(range(total_pages - max_display_pages + 1, total_pages + 1))
    else:
        display_pages = [1, "..."] + list(range(current_page - 1, current_page + 2)) + ["..."] + [total_pages]

    # Xếp các nút trang với khoảng cách đều nhau
    x_offset = 100  # Khoảng cách bắt đầu từ bên phải nút "Previous"
    for page in display_pages:
        if page == "...":
            # Điều chỉnh để dấu "..." không tạo khoảng giữa các nút
            pagination_canvas.create_text(x_offset, 25, text=page, fill="#3498db", font=("Arial", 12, "bold"))
            x_offset += 40  # khoảng cách cho "..." để sát vào giữa các nút
        else:
            create_rounded_button(
                pagination_canvas,
                x=x_offset,
                y=10,
                width=40,
                height=30,
                radius=15,
                text=str(page),
                command=lambda p=page: populate_table(table, page=p),
                bg_color="#FFF" if page != current_page else "#bdc3c7",
                text_color="#3498db" if page != current_page else "#000",
                hover_bg_color="#bdc3c7",
                hover_text_color="#000"
            )
            x_offset += 55  # Khoảng cách giữa các nút trang để tạo sự cân đối

    # Nút "Next"
    create_rounded_button(
        pagination_canvas,
        x=x_offset + 10,
        y=10,
        width=80,
        height=30,
        radius=15,
        text="Next",
        command=lambda: change_page(1),
        bg_color="#3498db",
        text_color="#FFF",
        hover_bg_color="#2980b9",
        hover_text_color="#CCC"
    )

def change_page(direction):
    global current_page
    new_page = current_page + direction
    if 1 <= new_page <= total_pages:
        populate_table(table, page=new_page)

def search_animals(event, entry, table):
    filter_value = entry.get()  # Lấy giá trị từ ô Entry
    populate_table(table, filter_value=filter_value)  # Cập nhật bảng với giá trị tìm kiếm và giữ nguyên trang hiện tại

    # Tự động chọn giá trị đầu tiên trong bảng 
    if table.get_children():
        table.selection_set(table.get_children()[0])  # Chọn giá trị đầu tiên

def sort_by_weight(table):
    global sort_ascending
    # Gọi hàm populate_table với sắp xếp theo cân nặng tăng dần
    populate_table(table, sort_by_weight=True, page=current_page)
    sort_ascending = not sort_ascending

def back_to_home():
    featuresPage.destroy()

def FeaturesPage(root):
    global featuresPage
    featuresPage = tk.Toplevel()  
    featuresPage.title("Features")
    featuresPage.geometry("1300x700")
    featuresPage.config(bg="#FFF")

    # Fonts
    header_font = font.Font(family="Arial", size=22, weight="bold")  
    heading_font = font.Font(family="Arial", size=14, weight="bold")

    # Tiêu đề của management page
    title_label = tk.Label(featuresPage, text="ANIMAL LIST", bg="#FFF", fg="#2980b9", font=header_font)
    title_label.pack(pady=(5, 20)) 

    # Tạo khung cho bảng với grid layout
    frame = tk.Frame(featuresPage, width=1250, height=300)
    frame.grid_propagate(False)
    frame.pack(pady=(5, 20), padx=20)

    # Cho phép frame hiển thị theo chiều rộng cố định
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    
    # Tạo Treeview với số hàng cố định
    global table
    table = ttk.Treeview(frame, columns=("ID", "Animal", "Weight", "Lifespan", "Diet", "Habitat", "Conservation Status"), 
                         show="headings", height=10)

    # Thêm frame phân trang vào giao diện
    global pagination_frame
    pagination_frame = tk.Frame(featuresPage, bg="#FFF")
    pagination_frame.pack(pady=5, anchor="center")  

    # Khung cho ô tìm kiếm và nút search
    search_frame = tk.Frame(featuresPage, bg="#FFF")
    search_frame.pack(pady=(5, 20), padx=20, anchor="center")    

    # Sử dụng pack để đặt label, entry
    search_label = tk.Label(search_frame, text="Search Animal:", bg="#FFF", fg="#2980b9", font=heading_font)
    search_label.pack(side="left") 

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

    # Điền dữ liệu vào bảng
    populate_table(table)

    # Đặt bảng vào khung
    table.grid(row=0, column=0, sticky="nsew")  # Đặt trong grid và cho phép co giãn

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