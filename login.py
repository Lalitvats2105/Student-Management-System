from tkinter import *
from tkinter import messagebox
from PIL import ImageTk


def login():
    if username.get() == "" or password.get() == "":
        messagebox.showerror("Error", "Username and Password cannot be blank!")
    elif username.get() == "admin" and password.get() == "admin":
        messagebox.showinfo("Success", "Login Successful!")
        root.destroy()
        import main
    else:
        messagebox.showerror("Error", "Invalid Username or Password!")


root = Tk()
root.title("Student Management System Login")
favicon = ImageTk.PhotoImage(file="login.png")
root.iconphoto(False, favicon)
root.state('zoomed')
root.resizable(False, False)

background = ImageTk.PhotoImage(file="student_background.jpg")
Label(root, image=background).pack()

loginFrame = Frame(root)
loginFrame.place(x=550, y=200)

LoginLogoImage = PhotoImage(file="student.png")
LoginLogoLabel = Label(loginFrame, image=LoginLogoImage)
LoginLogoLabel.grid(row=0, column=0, columnspan=2, pady=20)

UserNameImage = PhotoImage(file="username.png")
UserNameLabel = Label(loginFrame, image=UserNameImage, text="Username", compound=LEFT,
                      font=("times new roman", 20, "bold"), fg="gray")
UserNameLabel.grid(row=1, column=0, pady=20, padx=20)

username = StringVar()
password = StringVar()

UserNameEntry = Entry(loginFrame, font=("times new roman", 15, "bold"), bg="lightgray", textvariable=username)
UserNameEntry.grid(row=1, column=1, pady=20, padx=20)

PasswordImage = PhotoImage(file="password.png")
PasswordImageLabel = Label(loginFrame, image=PasswordImage, text="Password", compound=LEFT,
                           font=("times new roman", 20, "bold"), fg="gray")
PasswordImageLabel.grid(row=2, column=0, pady=20, padx=20)

PasswordEntry = Entry(loginFrame, font=("times new roman", 15, "bold"), bg="lightgray", show="*", textvariable=password)
PasswordEntry.grid(row=2, column=1, pady=20, padx=20)

LoginButton = Button(loginFrame, text="Login", font=("times new roman", 20, "bold"), width=15, bg="#974589", fg="white",
                     activebackground="#000000", activeforeground="white", cursor="hand2", command=login)
LoginButton.grid(row=3, column=0, columnspan=2, pady=20, padx=20)

Button(root, text="Exit", command=lambda: messagebox.askyesno("Exit", "Do you want to exit") and root.destroy()).place(
    x=1500, y=814)

root.mainloop()
