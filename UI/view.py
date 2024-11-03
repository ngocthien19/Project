import tkinter as tk
from tkinter import messagebox 
from button_radius import create_rounded_button

def show_item_details(item_data):
    # Tạo cửa sổ modal
    modal = tk.Toplevel()
    modal.title("Animal Info")
    modal.geometry("600x400")
    modal.config(bg="#FFF")

    # Tiêu đề của modal
    title_label = tk.Label(modal, text="Animal Info", font=("Arial", 22, "bold"), bg="#FFF", fg="#2980b9")
    title_label.pack(pady=(10, 10))

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
        entry_widget.config(state=tk.DISABLED)  # Vô hiệu hóa entry để không cho phép chỉnh sửa
        entries.append(entry_widget)

    canvas = tk.Canvas(modal, bg="#FFF", highlightthickness=0, width=100, height=50)
    canvas.pack(padx=10, pady=(10, 5), side=tk.RIGHT)

    create_rounded_button(
        canvas, 
        x=5, 
        y=5, 
        width=90, 
        height=40, 
        radius=10, 
        text="Close",
        command=lambda: modal.destroy(),
        bg_color="#e74c3c", text_color="#FFF", hover_bg_color="#c0392b", hover_text_color="#CCC"
    )

def View(table):
    # Lấy mục được chọn từ Treeview
    selected_item = table.selection()
    if selected_item:
        item_values = table.item(selected_item)['values']  # Lấy giá trị của hàng đã chọn
        show_item_details(item_values)  # Hiện modal với thông tin chi tiết
    else:
        messagebox.showwarning("Warning", "Vui lòng chọn một mục từ danh sách.")