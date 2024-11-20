import tkinter as tk
import webbrowser  
from PIL import Image, ImageTk, ImageDraw, ImageOps
from tkinter import font
from button_radius import create_rounded_button

def create_rounded_image(image_path, size, radius):
    img = Image.open(image_path).convert("RGBA")
    img = img.resize(size, Image.LANCZOS)

    mask = Image.new("L", size, 0)  # Mặt nạ đen
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, size[0], size[1]], radius=radius, fill=255)  # Vẽ mặt nạ trắng cho vùng bo

    rounded_image = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    rounded_image.putalpha(mask)

    white_background = Image.new("RGBA", size, (255, 255, 255, 255))
    final_image = Image.alpha_composite(white_background, rounded_image)

    return final_image 

def on_button_click():
    url = "https://vnexpress.net/tag/the-gioi-dong-vat-837998" 
    webbrowser.open(url)

def HomePage(root):
    # Tạo khung chính
    frame = tk.Frame(root)
    frame.configure(bg='white')  # Đặt nền khung là màu trắng

    # Fonts
    label_font = font.Font(family="Arial", size=22, weight="bold")  # Font cho tiêu đề
    label_font_desc = font.Font(family="Arial", size=14, weight="normal")  # Font cho mô tả

    # Cấu trúc layout
    frame.grid_rowconfigure((0,1,2), weight=1)  # Cấu hình hàng để có trọng số
    frame.grid_columnconfigure(0, weight=1)  # Cấu hình cột 0 để có trọng số
    frame.grid_columnconfigure(1, weight=3)  # Cấu hình cột 1 để có trọng số lớn hơn

    # Khung chứa ảnh
    frame_image = tk.Frame(bg='white')

    # Đường dẫn đến hình ảnh
    image_path = "D:/VScode/Python/Project/images/home.jpg"
    size = (400, 400)  # Kích thước hình ảnh
    radius = 50  # Bán kính bo góc

    # Tạo hình ảnh bo góc
    rounded_image = create_rounded_image(image_path, size, radius)
    photo = ImageTk.PhotoImage(rounded_image)  # Chuyển đổi hình ảnh thành PhotoImage để hiển thị trong Tkinter

    # Tạo nhãn để hiển thị hình ảnh
    label_image = tk.Label(frame_image, image=photo)
    label_image.image = photo  # Giữ tham chiếu đến photo để tránh thu hồi
    label_image.grid(row=0, column=0, sticky="w", padx=10, pady=10)  # Đặt ảnh căn trái với padding

    frame_image.pack(side="left", padx=10)  # Đặt khung ảnh bên trái

    # Khung cho nội dung bên phải
    frame_content = tk.Frame(bg='white')

    # Tạo nội dung để hiển thị bên phải 
    label_text = tk.Label(frame_content, text="Animals Enrich Our World.", bg='white', font=label_font)
    label_text.grid(row=0, column=0, sticky="w", padx=10, pady=5)  # Đặt tiêu đề căn trái

    label_desc = tk.Label(
        frame_content, 
        text='Animals bring diversity, beauty, and wonder to our world, enriching our lives and ecosystems with their presence.', 
        bg='white', 
        font=label_font_desc,
        fg="#34495E",
        wraplength=500  # Giới hạn chiều dài của mô tả
    )
    label_desc.grid(row=1, column=0, columnspan=2, padx=10, pady=5)  # Đặt mô tả chiếm 2 cột

    # Tạo canvas cho nút bấm
    canvas = tk.Canvas(frame_content, width=300, height=60, bg="white", highlightthickness=0)
    canvas.grid(row=2, column=0, sticky="w", padx=10, pady=30)  # Đặt canvas

    # Tạo nút bo góc
    button, text_button = create_rounded_button(
        canvas, 
        x=5, 
        y=5, 
        width=150,  
        height=50,  
        radius=15,  
        text="Exploring",  
        command=on_button_click  
    ) 
    
    # Đặt khung nội dung bên phải khung hình ảnh
    frame_content.pack(side="left", padx=10)  # Đặt khung nội dung bên trái với khoảng cách

    return frame