def create_rounded_button(
        canvas, x, y, width, height, radius, text="", 
        command=None, bg_color="#FFF", text_color="#3498db", hover_bg_color="#2980b9", hover_text_color="white"
    ):
    # Tính toán các điểm cho nút bo góc
    points = [x + radius, y, x + width - radius, y, x + width, y, x + width, y + radius, 
              x + width, y + height - radius, x + width, y + height, x + width - radius, y + height, 
              x + radius, y + height, x, y + height, x, y + height - radius, x, y + radius, x, y]
    
    # Vẽ nút với màu nền đã chọn
    button = canvas.create_polygon(points, smooth=True, fill=bg_color, outline=text_color)

    # Vẽ văn bản trên nút
    text_x = x + width / 2
    text_y = y + height / 2
    text_button = canvas.create_text(text_x, text_y, text=text, fill=text_color, font=("Arial", 12, "bold"))

    # Liên kết sự kiện click với nút, nếu có lệnh (command)
    if command:
        canvas.tag_bind(button, "<Button-1>", lambda e: command())
        canvas.tag_bind(text_button, "<Button-1>", lambda e: command())

    # Thay đổi màu khi di chuột vào nút
    def on_enter(e):
        canvas.itemconfig(button, fill=hover_bg_color)
        canvas.itemconfig(text_button, fill=hover_text_color)
        canvas.config(cursor="hand2")

    # Trở lại màu ban đầu khi rời chuột khỏi nút
    def on_leave(e):
        canvas.itemconfig(button, fill=bg_color)
        canvas.itemconfig(text_button, fill=text_color)
        canvas.config(cursor="")

    # Liên kết sự kiện hover với nút
    canvas.tag_bind(button, "<Enter>", on_enter)
    canvas.tag_bind(button, "<Leave>", on_leave)
    canvas.tag_bind(text_button, "<Enter>", on_enter)
    canvas.tag_bind(text_button, "<Leave>", on_leave)

    return button, text_button