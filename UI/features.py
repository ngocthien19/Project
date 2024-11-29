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
sort_ascending_all = True # Sort all

def populate_table(table, filter_value="", filter_data ="", page=None):
    global current_page, total_pages
    
    # Đọc dữ liệu từ file CSV   
    try:
        data = pd.read_csv(r"D:\VScode\Python\Project\database\Cleaned_Animal_Dataset.csv")
    except FileNotFoundError:
        messagebox.showwarning("Exist File", "File not found")
        return

    # Nếu có bộ lọc tìm kiếm theo Weight
    if filter_value:
        # Kiểm tra nếu filter_value là một số để tìm kiếm theo cân nặng
        try:
            weight_filter = float(filter_value)  # Chuyển đổi filter_value thành số
            data = data[data["ID"] == weight_filter]  # So sánh với cột Weight (kg)
        except ValueError:
            # Nếu filter_value không phải là số, tìm kiếm theo chuỗi trong cột Weight (kg)
            data = data[data["ID"].astype(str).str.contains(filter_value, case=False, na=False)]
        
        current_page = 1  # Đặt lại trang về 1 khi có tìm kiếm
        total_pages = 1  # Hiển thị toàn bộ kết quả

    elif filter_data:
        # Kiểm tra xem người dùng có nhập số kèm theo (2) hoặc (3)
        if "(" in filter_data and ")" in filter_data:
            # Tách phần giá trị và phần loại cột (2 hoặc 3)
            value = filter_data.split("(")[0]  # Giá trị số (12)
            column_type = filter_data.split("(")[1].replace(")", "")  # Loại cột (2 hoặc 3)

            try:
                value = float(value)  # Chuyển đổi giá trị nhập vào thành số

                if column_type == "2":  # Tìm kiếm trong cột Weight (kg)
                    data = data[data["Weight (kg)"] == value]
                elif column_type == "3":  # Tìm kiếm trong cột Lifespan (years)
                    data = data[data["Lifespan (years)"] == value]
                else:
                    # Nếu giá trị trong ngoặc không phải là 2 hoặc 3, thông báo lỗi
                    messagebox.showwarning("Invalid Input", "Please enter 2 for Weight or 3 for Lifespan.")
                    return
            except ValueError:
                # Nếu không thể chuyển đổi giá trị thành số, thông báo lỗi
                messagebox.showwarning("Invalid Value", "Please enter a valid number.")
                return
        else:
            # Nếu không có kiểu (2) hoặc (3), tìm kiếm theo chuỗi trong tất cả các cột trừ ID
            columns_to_filter = [col for col in data.columns if col != "ID"]
            mask = data[columns_to_filter].apply(lambda row: row.astype(str).str.contains(filter_data, case=False, na=False).any(), axis=1)
            data = data[mask]
        
        # Cập nhật kết quả tìm kiếm vào bảng
        current_page = 1
        total_pages = 1  # Hiển thị toàn bộ kết quả
    else:
        # Cập nhật tổng số trang khi không có tìm kiếm và lọc
        total_pages = max(1, (len(data) + rows_per_page - 1) // rows_per_page)

    # Nếu không có bộ lọc, phân trang và hiển thị dữ liệu theo từng trang
    if not filter_value and not filter_data:
        # Phân trang chỉ khi không có lọc hay tìm kiếm
        start_row = (current_page - 1) * rows_per_page
        end_row = min(start_row + rows_per_page, len(data))
        page_data = data.iloc[start_row:end_row]
    else:
        # Nếu có bộ lọc, hiển thị toàn bộ dữ liệu
        page_data = data

    # Xóa dữ liệu cũ trong bảng
    table.delete(*table.get_children())

    # Điền dữ liệu cho bảng
    for index, row in page_data.iterrows():
        table.insert("", "end", values=(row["ID"], row["Animal"], row["Weight (kg)"], row["Lifespan (years)"], row["Diet"], row["Habitat"], row["Conservation Status"]))

    # Cập nhật trạng thái các nút phân trang nếu không có bộ lọc
    if not filter_value and not filter_data:
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
        current_page = new_page  # Cập nhật current_page
        populate_table(table, page=current_page)  # Cập nhật lại dữ liệu cho trang mới

def search_animals(event, entry, table):
    filter_value = entry.get()  # Lấy giá trị từ ô Entry
    populate_table(table, filter_value=filter_value)  # Cập nhật bảng với giá trị tìm kiếm và giữ nguyên trang hiện tại

    # Tự động chọn giá trị đầu tiên trong bảng 
    if table.get_children():
        table.selection_set(table.get_children()[0])  # Chọn giá trị đầu tiên

def filter_data(entry, table):
    filter_data_value = entry.get()  # Lấy giá trị từ ô Entry
    populate_table(table, filter_data=filter_data_value)  # Cập nhật bảng với giá trị lọc và giữ nguyên trang hiện tại

    # Tự động chọn giá trị đầu tiên trong bảng 
    if table.get_children():
        table.selection_set(table.get_children()[0])  # Chọn giá trị đầu tiên 

def sort_data_by_combobox(table, combobox, page):
    global sort_ascending
    # Lấy giá trị từ combobox để quyết định cột cần sắp xếp
    sort_column = combobox.get()

    # Kiểm tra xem có phải là cột hợp lệ không
    if sort_column not in ["ID", "Animal", "Weight (kg)", "Lifespan (years)", "Diet", "Habitat", "Conservation Status"]:
        messagebox.showwarning("Invalid Column", "Please select a valid column to sort.")
        return

    # Đọc dữ liệu từ file CSV (hoặc từ dataframe đã có sẵn)
    try:
        data = pd.read_csv(r"D:\VScode\Python\Project\database\Cleaned_Animal_Dataset.csv")
    except FileNotFoundError:
        messagebox.showwarning("Exist File", "File not found")
        return

    # Chỉ lấy dữ liệu của trang hiện tại
    start_row = (page - 1) * rows_per_page
    end_row = min(start_row + rows_per_page, len(data))
    page_data = data.iloc[start_row:end_row]

    # Sắp xếp dữ liệu theo cột đã chọn
    page_data = page_data.sort_values(by=sort_column, ascending=sort_ascending)

    # Xóa dữ liệu cũ trong bảng
    table.delete(*table.get_children())

    # Điền dữ liệu vào bảng
    for index, row in page_data.iterrows():
        table.insert("", "end", values=(row["ID"], row["Animal"], row["Weight (kg)"], row["Lifespan (years)"], row["Diet"], row["Habitat"], row["Conservation Status"]))

    # Đảo ngược thứ tự sắp xếp cho lần sau
    sort_ascending = not sort_ascending

def sort_all_data(table):
    global sort_ascending_all
    # Lấy giá trị từ combobox để quyết định cột cần sắp xếp
    sort_column = sort_combobox.get()

    # Kiểm tra xem có phải là cột hợp lệ không
    if sort_column not in ["ID", "Animal", "Weight (kg)", "Lifespan (years)", "Diet", "Habitat", "Conservation Status"]:
        messagebox.showwarning("Invalid Column", "Please select a valid column to sort.")
        return

    # Đọc dữ liệu từ file CSV
    try:
        data = pd.read_csv(r"D:\VScode\Python\Project\database\Cleaned_Animal_Dataset.csv")
    except FileNotFoundError:
        messagebox.showwarning("Exist File", "File not found")
        return

    # Sắp xếp dữ liệu theo cột đã chọn
    data = data.sort_values(by=sort_column, ascending=sort_ascending_all)

    # Xóa dữ liệu cũ trong bảng
    table.delete(*table.get_children())

    # Điền dữ liệu vào bảng
    for index, row in data.iterrows():
        table.insert("", "end", values=(row["ID"], row["Animal"], row["Weight (kg)"], row["Lifespan (years)"], row["Diet"], row["Habitat"], row["Conservation Status"]))

    # Đảo ngược thứ tự sắp xếp cho lần sau
    sort_ascending_all = not sort_ascending_all

    # Chọn item đầu tiên sau khi sắp xếp
    first_item = table.get_children()[0]
    table.selection_set(first_item)
    table.focus(first_item)

def sort_page(table):
    global sort_ascending
    # Gọi hàm sort_data_by_combobox với cột chọn từ combobox và trang hiện tại
    sort_data_by_combobox(table, sort_combobox, current_page)


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

    # Khung cho ô tìm kiếm, lọc, sắp xếp
    sfs_frame = tk.Frame(featuresPage, bg="#FFF")
    sfs_frame.pack(pady=(5, 20), padx=20, anchor="w")    

    # Sử dụng pack để đặt label, entry
    search_label = tk.Label(sfs_frame, text="Search ID:", bg="#FFF", fg="#2980b9", font=heading_font)
    search_label.pack(side="left") 

    # Ô Entry cho tìm kiếm
    search_entry = tk.Entry(sfs_frame, width=20, font=heading_font)
    search_entry.pack(side="left", padx=(10, 0))

    def on_focus_in(event, entry, placeholder_text):
        """Ẩn placeholder khi người dùng nhấp vào Entry"""
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)  # Xóa placeholder
            entry.config(fg='black')  # Đổi màu chữ khi bắt đầu nhập

    def on_focus_out(event, entry, placeholder_text):
        """Hiển thị placeholder khi Entry bị bỏ trống"""
        if entry.get() == '':
            entry.insert(0, placeholder_text)  # Hiển thị lại placeholder
            entry.config(fg='gray')  # Đổi màu chữ placeholder
        
    # Label lọc
    filter_label = tk.Label(sfs_frame, text="Filter:", bg="#FFF", fg="#2980b9", font=heading_font)
    filter_label.pack(side="left", padx=(35, 0))

    # Ô để lọc
    placeholder_text = "If number, 12(2) or 12(3)"  # Placeholder
    filter_entry = tk.Entry(sfs_frame, width=30, font=heading_font)
    filter_entry.pack(side="left", padx=(10, 0))

    # Label Sort
    sort_label = tk.Label(sfs_frame, text="Sort with column: ", bg="#FFF", fg="#2980b9", font=heading_font)
    sort_label.pack(side="left", padx=(35, 0))  

    # Tạo Combobox với các lựa chọn
    global sort_combobox
    sort_combobox = ttk.Combobox(sfs_frame, values=["ID", "Animal", "Weight (kg)", "Lifespan (years)", "Diet", "Habitat", "Conservation Status"], 
                                width=20, font=heading_font)
    # Đặt giá trị mặc định cho Combobox (có thể thay đổi giá trị mặc định nếu cần)
    sort_combobox.set("ID")
    # Đặt combobox vào frame
    sort_combobox.pack(side="left", padx=(10, 0))

    # Cấu hình màu chữ khi bắt đầu (màu xám cho placeholder)
    filter_entry.insert(0, placeholder_text)
    filter_entry.config(fg='gray')

    # Sự kiện khi người dùng nhấp vào Entry (focus vào)
    filter_entry.bind("<FocusIn>", lambda event: on_focus_in(event, filter_entry, placeholder_text))

    # Sự kiện khi người dùng bỏ Entry (focus ra)
    filter_entry.bind("<FocusOut>", lambda event: on_focus_out(event, filter_entry, placeholder_text))

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
    button_canvas = tk.Canvas(featuresPage, bg="#FFF", highlightthickness=0, width=800, height=60)
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
        button_canvas, 380, 10, 100, 40, 20, "Filter", 
        command=lambda: filter_data(filter_entry, table), bg_color="#2ecc71", text_color="#FFF", hover_bg_color="#27ae60", hover_text_color="#CCC"
    )

    create_rounded_button(
        button_canvas, 500, 10, 100, 40, 20, "Sort Page", 
        command=lambda: sort_page(table), bg_color="#8e44ad", text_color="#FFF", hover_bg_color="#732d91", hover_text_color="#CCC"
    )

    create_rounded_button(
        button_canvas, 620, 10, 100, 40, 20, "Sort All", 
        command=lambda: sort_all_data(table), bg_color="#6c3483", text_color="#FFF", hover_bg_color="#5b2c6f", hover_text_color="#CCC"
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