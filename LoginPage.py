from tkinter import *
from PIL import ImageTk, Image
import main

# Khởi tạo cửa sổ chính
window = Tk()
window.geometry('1100x700')  # Đặt kích thước cố định cho cửa sổ
window.resizable(False, False)  
window.title('Login Page')

# background image  
bg_frame = Image.open('D:/VScode/Python/Project/images/background1.png')
photo = ImageTk.PhotoImage(bg_frame)
bg_panel = Label(window, image=photo)
bg_panel.image = photo
bg_panel.pack(fill='both', expand='yes')

# Login frame
lgn_frame = Frame(window, bg='#040405', width=950, height=600)
lgn_frame.place(x=75, y=50)  # Căn giữa khung login

# header text
txt = "WELCOME"
heading = Label(lgn_frame, text=txt, font=('yu gothic ui', 25, "bold"), bg="#040405",
                fg='white', bd=5, relief=FLAT)
heading.place(x=80, y=30, width=300, height=30)

# Image Left
side_image = Image.open('D:/VScode/Python/Project/images/vector.png')
side_photo = ImageTk.PhotoImage(side_image)
side_image_label = Label(lgn_frame, image=side_photo, bg='#040405')
side_image_label.image = side_photo
side_image_label.place(x=5, y=100)

# Sign in image
sign_in_image = Image.open('D:/VScode/Python/Project/images/hyy.png')
sign_in_photo = ImageTk.PhotoImage(sign_in_image)
sign_in_image_label = Label(lgn_frame, image=sign_in_photo, bg='#040405')
sign_in_image_label.image = sign_in_photo
sign_in_image_label.place(x=620, y=130)

# label sign in
sign_in_label = Label(lgn_frame, text="Sign In", bg="#040405", fg="white",
                    font=("yu gothic ui", 17, "bold"))
sign_in_label.place(x=650, y=240)

# username
username_label = Label(lgn_frame, text="Username", bg="#040405", fg="#4f4e4d",
                    font=("yu gothic ui", 13, "bold"))
username_label.place(x=552, y=300)

username_entry = Entry(lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#FFF",
                font=("yu gothic ui", 12, "bold"), insertbackground='#6b6a69')
username_entry.place(x=580, y=335, width=270)

username_line = Canvas(lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
username_line.place(x=550, y=359)

username_icon = Image.open('D:/VScode/Python/Project/images/username_icon.png')
username_icon_photo = ImageTk.PhotoImage(username_icon)
username_icon_label = Label(lgn_frame, image=username_icon_photo, bg='#040405')
username_icon_label.image = username_icon_photo
username_icon_label.place(x=550, y=332)

# Password
password_label = Label(lgn_frame, text="Password", bg="#040405", fg="#4f4e4d",
                    font=("yu gothic ui", 13, "bold"))
password_label.place(x=550, y=380)

password_entry = Entry(lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#FFF",
                    font=("yu gothic ui", 12, "bold"), show="*", insertbackground='#6b6a69')
password_entry.place(x=580, y=416, width=244)

password_line = Canvas(lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
password_line.place(x=550, y=440)

password_icon = Image.open('D:/VScode/Python/Project/images/password_icon.png')
password_icon_photo = ImageTk.PhotoImage(password_icon)
password_icon_label = Label(lgn_frame, image=password_icon_photo, bg='#040405')
password_icon_label.image = password_icon_photo
password_icon_label.place(x=550, y=414)

# Error label
error_label = Label(lgn_frame, text="", bg="#040405", fg="red", font=("yu gothic ui", 11, "bold"))
error_label.place(x=550, y=300)

# Hàm kiểm tra đăng nhập
def attempt_login():
    username = username_entry.get()
    password = password_entry.get()
    if username == "admin" and password == "123456":  # Tài khoản mặc định
        window.destroy()  # Đóng cửa sổ đăng nhập
        main.run_main()  # Chạy trang chính
    else:
        error_label.config(text="Invalid username or password")  # Hiển thị lỗi nếu sai thông tin
        password_entry.delete(0, END)

# Gắn sự kiện Enter để thực hiện hàm attempt_login
window.bind('<Return>', lambda event: attempt_login())

# show hide password
def show_password():
    show_button.config(image=hide_image)
    password_entry.config(show='')
    show_button.config(command=hide_password)

def hide_password():
    show_button.config(image=show_image)
    password_entry.config(show='*')
    show_button.config(command=show_password)

show_image = ImageTk.PhotoImage(file='D:/VScode/Python/Project/images/show.png')
hide_image = ImageTk.PhotoImage(file='D:/VScode/Python/Project/images/hide.png')

show_button = Button(lgn_frame, image=show_image, relief=FLAT, activebackground="white",
                    borderwidth=0, background="white", cursor="hand2", command=show_password)
show_button.place(x=860, y=420)

# Login button
lgn_button = Image.open('D:/VScode/Python/Project/images/btn1.png')
lgn_button_photo = ImageTk.PhotoImage(lgn_button)
lgn_button_label = Label(lgn_frame, image=lgn_button_photo, bg='#040405')
lgn_button_label.image = lgn_button_photo
lgn_button_label.place(x=550, y=450)

Button(lgn_button_label, text='LOGIN', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
    bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=attempt_login).place(x=20, y=10)

# Forgot password
forgot_button = Button(lgn_frame, text="Forgot Password ?", font=("yu gothic ui", 13, "bold underline"),
                    fg="white", relief=FLAT, activebackground="#040405", borderwidth=0,
                    background="#040405", cursor="hand2")
forgot_button.place(x=630, y=510)

# Sign up
sign_label = Label(lgn_frame, text='No account yet?', font=("yu gothic ui", 11, "bold"),
                relief=FLAT, borderwidth=0, background="#040405", fg='white')
sign_label.place(x=550, y=560)

signup_img = ImageTk.PhotoImage(file='D:/VScode/Python/Project/images/register.png')
signup_button_label = Button(lgn_frame, image=signup_img, bg='#98a65d', cursor="hand2", borderwidth=0,
                            background="#040405", activebackground="#040405")
signup_button_label.place(x=670, y=555, width=111, height=35)

# Chạy giao diện
window.mainloop()
