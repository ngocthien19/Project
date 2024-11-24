import tkinter as tk
import webbrowser  
from PIL import Image, ImageTk, ImageDraw, ImageOps
from tkinter import font
from button_radius import create_rounded_button

def create_rounded_or_circle_image(image_path, size, radius=None):
    # Hàm tạo ảnh bo góc (chữ nhật) hoặc ảnh tròn.
    img = Image.open(image_path).convert("RGBA")
    img = img.resize(size, Image.LANCZOS)

    # Tạo mặt nạ
    mask = Image.new("L", size, 0)  # Mặt nạ đen
    draw = ImageDraw.Draw(mask)

    if radius is None:  # Nếu radius là None, vẽ ảnh tròn
        draw.ellipse((0, 0, size[0], size[1]), fill=255)  # Mặt nạ hình tròn
    else:  # Nếu radius có giá trị, vẽ ảnh bo góc chữ nhật
        draw.rounded_rectangle([0, 0, size[0], size[1]], radius=radius, fill=255)

    # Áp dụng mặt nạ
    rounded_image = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    rounded_image.putalpha(mask)

    # Tạo nền trắng
    white_background = Image.new("RGBA", size, (255, 255, 255, 255))
    final_image = Image.alpha_composite(white_background, rounded_image)

    return final_image
    
def on_button_click():
    url = "https://vnexpress.net/tag/the-gioi-dong-vat-837998" 
    webbrowser.open(url)

def HomePage(root):
    # Tạo khung chính
    frame = tk.Frame(root, bg='white')
    frame.pack(fill="both", expand=True)  # Đặt khung chính

    # Fonts
    label_font = font.Font(family="Arial", size=22, weight="bold")  # Font cho tiêu đề
    label_font_desc = font.Font(family="Arial", size=14, weight="normal")  # Font cho mô tả

    # --------------------- Vùng phủ bao gồm frame_top_right và modal ---------------------
    hover_area = tk.Frame(frame, bg="white") 
    hover_area.place(relx=1.0, rely=0.01, anchor="ne", relwidth=0.2, relheight=0.3)

    # --------------------- frame góc phải trên cùng ---------------------
    frame_top_right = tk.Frame(hover_area, bg='white')
    frame_top_right.pack(side="top", anchor="ne", pady=5)

    # Đường dẫn hình ảnh góc phải trên cùng
    sign_in_image_path = "D:/VScode/Python/Project/images/admin.png"
    size = (20, 20)  # Kích thước hình ảnh tròn

    # Tạo ảnh tròn
    circle_image = create_rounded_or_circle_image(sign_in_image_path, size)  # Gọi hàm để tạo ảnh tròn
    sign_in_photo = ImageTk.PhotoImage(circle_image)

    # Hiển thị hình ảnh tròn ở góc phải
    sign_in_image_label = tk.Label(frame_top_right, image=sign_in_photo, bg='white')
    sign_in_image_label.image = sign_in_photo  # Lưu tham chiếu để tránh thu hồi
    sign_in_image_label.pack(side="left", padx=5)

    # Thêm label bên cạnh hình ảnh
    label_top_right = tk.Label(
        frame_top_right,
        text="Administration",
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#2C3E50"
    )
    label_top_right.pack(side="left", padx=(0, 25))

    # --------------------- Modal ---------------------
    modal = tk.Frame(hover_area, bg="white", relief="solid", bd=1)
    modal.place_forget()  # Modal ban đầu được ẩn đi

    # Tạo danh sách các mục trong modal
    modal_items = ["My account", "Policies", "Security", "Log out"]

    # Hàm thêm hiệu ứng hover
    def add_hover_effect(widget):
        # Đổi màu khi hover
        def on_enter(event):
            widget.config(bg="#f0f0f0")  # Đổi màu nền khi hover
        def on_leave(event):
            widget.config(bg="white")  # Trả lại màu nền ban đầu khi rời chuột

        # Gắn sự kiện
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    # Thêm các mục vào modal và gắn hiệu ứng hover
    for item in modal_items:
        label = tk.Label(modal, text=item, font=("Arial", 10), bg="white", fg="black", anchor="w", cursor="hand2")
        label.pack(fill="x", ipadx=3, ipady=3)  # Để label chiếm toàn bộ chiều dài
        add_hover_effect(label)

    # --------------------- Vẽ hình tam giác nối ---------------------
    triangle_canvas = tk.Canvas(hover_area, width=20, height=10, bg="white", highlightthickness=0)
    triangle_canvas.create_polygon(
        0, 10,   # Điểm góc trái
        20, 10,  # Điểm góc phải
        10, 0,   # Điểm trên cùng (đỉnh tam giác)
        fill="white", outline="#000"
    )
    triangle_canvas.place_forget()  # Ban đầu ẩn tam giác

    # --------------------- Hàm xử lý hover ---------------------
    def show_modal(event):
        modal.place(relx=0, rely=0.3, relwidth=0.8)  # Hiển thị modal tại đúng vị trí dưới hover_area
        triangle_canvas.place(relx=0.5, rely=0.25, anchor="n")  # Hiển thị tam giác

    def hide_modal(event):
        modal.place_forget()  # Ẩn modal
        triangle_canvas.place_forget()  # Ẩn tam giác

    # Gắn sự kiện hover vào vùng hover_area
    hover_area.bind("<Enter>", show_modal)
    hover_area.bind("<Leave>", hide_modal)

    # --------------------- Khung chứa ảnh chính ---------------------
    frame_image = tk.Frame(frame, bg='white')
    frame_image.pack(side="left", padx=10, pady=10)

    # Đường dẫn đến hình ảnh chính
    image_path = "D:/VScode/Python/Project/images/home.jpg"
    size = (400, 400)  # Kích thước hình ảnh
    radius = 50  # Bán kính bo góc

    # Tạo hình ảnh bo góc
    rounded_image = create_rounded_or_circle_image(image_path, size, radius)
    photo = ImageTk.PhotoImage(rounded_image)

    # Hiển thị hình ảnh chính
    label_image = tk.Label(frame_image, image=photo, bg='white')
    label_image.image = photo  # Giữ tham chiếu đến photo để tránh thu hồi
    label_image.pack()

    # --------------------- Khung nội dung ---------------------
    frame_content = tk.Frame(frame, bg='white')
    frame_content.pack(side="left", padx=10, pady=10)

    # Tiêu đề
    label_text = tk.Label(frame_content, text="Animals Enrich Our World.", bg='white', font=label_font)
    label_text.pack(anchor="w", pady=5)

    # Mô tả
    label_desc = tk.Label(
        frame_content,
        text="Animals bring diversity, beauty, and wonder to our world, enriching our lives and ecosystems with their presence.",
        bg='white',
        font=label_font_desc,
        fg="#34495E",
        wraplength=500
    )
    label_desc.pack(anchor="w", pady=5)

    # Nút Exploring
    canvas = tk.Canvas(frame_content, width=300, height=70, bg="white", highlightthickness=0)
    canvas.pack(anchor="w", pady=30)

    create_rounded_button(
        canvas,
        x=5,
        y=5,
        width=150,
        height=60,
        radius=15,
        text="Exploring",
        command=on_button_click
    )

    return frame