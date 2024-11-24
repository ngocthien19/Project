from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

# Mảng để quản lý dữ liệu người dùng
user_data = []
 
# Hàm tải dữ liệu từ file vào mảng
def load_user_data():
    try:
        with open('D:/VScode/Python/Project/database/user_data.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split(',')
                user_data.append({"username": username, "password": password})
    except FileNotFoundError:
        # Nếu file không tồn tại, tạo file mới
        with open('D:/VScode/Python/Project/database/user_data.txt', 'w') as file:
            pass

# Hàm lưu dữ liệu từ mảng vào file
def save_user_data(username, password):
    with open('D:/VScode/Python/Project/database/user_data.txt', 'a') as file:
        file.write(f"{username},{password}\n")

def SignupPage(open_login_callback):
    signup_window = Tk()
    signup_window.geometry('1100x700')  
    signup_window.resizable(False, False)
    signup_window.title('Sign Up Page')

    # Background image
    signup_bg_frame = Image.open('D:/VScode/Python/Project/images/background1.png')
    signup_photo = ImageTk.PhotoImage(signup_bg_frame)
    signup_bg_panel = Label(signup_window, image=signup_photo)
    signup_bg_panel.image = signup_photo
    signup_bg_panel.pack(fill='both', expand='yes')

    # Signup frame
    signup_frame = Frame(signup_window, bg='#040405', width=950, height=600)
    signup_frame.place(x=75, y=50)

    # Header text
    signup_heading = Label(signup_frame, text="CREATE ACCOUNT", font=('yu gothic ui', 25, "bold"), 
                           bg="#040405", fg='white', bd=5, relief=FLAT)
    signup_heading.place(x=80, y=30, width=400, height=30)

    # Left image
    signup_side_image = Image.open('D:/VScode/Python/Project/images/vector.png')
    signup_side_photo = ImageTk.PhotoImage(signup_side_image)
    signup_side_image_label = Label(signup_frame, image=signup_side_photo, bg='#040405')
    signup_side_image_label.image = signup_side_photo
    signup_side_image_label.place(x=5, y=100)

    # Right image
    signup_user_image = Image.open('D:/VScode/Python/Project/images/hyy.png')
    signup_user_photo = ImageTk.PhotoImage(signup_user_image)
    signup_user_image_label = Label(signup_frame, image=signup_user_photo, bg='#040405')
    signup_user_image_label.image = signup_user_photo
    signup_user_image_label.place(x=620, y=100)

    # Label Signup
    signup_label = Label(signup_frame, text="Sign Up", bg="#040405", fg="white",
                         font=("yu gothic ui", 17, "bold"))
    signup_label.place(x=650, y=220)

    # Username
    signup_username_label = Label(signup_frame, text="Username", bg="#040405", fg="#4f4e4d",
                                  font=("yu gothic ui", 13, "bold"))
    signup_username_label.place(x=550, y=270)

    signup_username_entry = Entry(signup_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#FFF",
                                  font=("yu gothic ui", 12, "bold"), insertbackground='#6b6a69')
    signup_username_entry.place(x=580, y=300, width=250)

    signup_username_line = Canvas(signup_frame, width=250, height=2.0, bg="#bdb9b1", highlightthickness=0)
    signup_username_line.place(x=580, y=325)

    signup_username_icon = Image.open('D:/VScode/Python/Project/images/username_icon.png')
    signup_username_icon_photo = ImageTk.PhotoImage(signup_username_icon)
    signup_username_icon_label = Label(signup_frame, image=signup_username_icon_photo, bg='#040405')
    signup_username_icon_label.image = signup_username_icon_photo
    signup_username_icon_label.place(x=550, y=300)

    # Password
    signup_password_label = Label(signup_frame, text="Password", bg="#040405", fg="#4f4e4d",
                                  font=("yu gothic ui", 13, "bold"))
    signup_password_label.place(x=550, y=340)

    signup_password_entry = Entry(signup_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#FFF",
                                  font=("yu gothic ui", 12, "bold"), show="*", insertbackground='#6b6a69')
    signup_password_entry.place(x=580, y=370, width=250)

    signup_password_line = Canvas(signup_frame, width=250, height=2.0, bg="#bdb9b1", highlightthickness=0)
    signup_password_line.place(x=580, y=395)

    signup_password_icon = Image.open('D:/VScode/Python/Project/images/password_icon.png')
    signup_password_icon_photo = ImageTk.PhotoImage(signup_password_icon)
    signup_password_icon_label = Label(signup_frame, image=signup_password_icon_photo, bg='#040405')
    signup_password_icon_label.image = signup_password_icon_photo
    signup_password_icon_label.place(x=550, y=370)

    # Confirm Password
    signup_confirm_password_label = Label(signup_frame, text="Confirm Password", bg="#040405", fg="#4f4e4d",
                                          font=("yu gothic ui", 13, "bold"))
    signup_confirm_password_label.place(x=550, y=410)

    signup_confirm_password_entry = Entry(signup_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#FFF",
                                          font=("yu gothic ui", 12, "bold"), show="*", insertbackground='#6b6a69')
    signup_confirm_password_entry.place(x=580, y=440, width=250)

    signup_confirm_password_line = Canvas(signup_frame, width=250, height=2.0, bg="#bdb9b1", highlightthickness=0)
    signup_confirm_password_line.place(x=580, y=465)

    signup_confirm_password_icon = Image.open('D:/VScode/Python/Project/images/password_icon.png')
    signup_confirm_password_icon_photo = ImageTk.PhotoImage(signup_confirm_password_icon)
    signup_confirm_password_icon_label = Label(signup_frame, image=signup_confirm_password_icon_photo, bg='#040405')
    signup_confirm_password_icon_label.image = signup_confirm_password_icon_photo
    signup_confirm_password_icon_label.place(x=550, y=440)

    # Hàm xử lý đăng ký
    def attempt_signup():
        username = signup_username_entry.get()
        password = signup_password_entry.get()
        confirm_password = signup_confirm_password_entry.get()

        if username == "" or password == "" or confirm_password == "":
            messagebox.showerror("Error", "Please fill out all fields!")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        # Kiểm tra tài khoản đã tồn tại
        for user in user_data:
            if user['username'] == username:
                messagebox.showerror("Error", "Username already exists!")
                return

        # Thêm thông tin vào mảng user_data và lưu vào file
        user_data.append({"username": username, "password": password})
        save_user_data(username, password)
        messagebox.showinfo("Success", "Account created successfully!")
        signup_window.destroy()
        open_login_callback()

    # Signup button
    signup_button = Button(signup_frame, text="Sign Up", font=("yu gothic ui", 13, "bold"), width=25,
                           bd=0, bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', 
                           command=attempt_signup)
    signup_button.place(x=580, y=500)

    # Label Back
    signup_back_label = Label(signup_frame, text="Back", font=("yu gothic ui", 12, "bold underline"), 
                              bg="#040405", fg="white", cursor="hand2")
    signup_back_label.place(x=550, y=540)

    # Gắn sự kiện click cho Label Back
    signup_back_label.bind("<Button-1>", lambda e: [signup_window.destroy(), open_login_callback()])

    # Gắn sự kiện Enter để thực hiện hàm attempt_signup
    signup_window.bind('<Return>', lambda event: attempt_signup())

    signup_window.mainloop()

# Load dữ liệu khi chương trình khởi động
load_user_data()
