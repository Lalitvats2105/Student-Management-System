import time
from tkinter import *
from tkinter import ttk, messagebox, Toplevel, filedialog
import ttkthemes
import pymysql
from pandas import DataFrame


def export_data():
    url = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                       filetypes=(("CSV file", "*.csv"), ("All files", "*.*")))
    indexing = studentTable.get_children()
    l = []
    for i in indexing:
        content = studentTable.item(i)["values"]
        l.append(content)

    table = DataFrame(l, columns=["Id", "Name", "Phone", "Email", "Address", "Gender", "D.O.B", "Date", "Time"])
    table.to_csv(url, index=False)
    messagebox.showinfo("Success", "Data exported successfully")


def update_data():
    query = "update student set name=%s, mobile=%s, email=%s, address=%s, gender=%s, dob=%s, date=%s, time=%s where " \
            "id=%s"
    cursor.execute(query, (
        NAme_entry.get(), PHone_entry.get(), EMail_entry.get(), ADdress_entry.get(), GEnder_entry.get(),
        DOb_entry.get(), time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"), ID_entry.get()))
    con.commit()
    messagebox.showinfo("Success", "Student updated successfully", parent=update_student_root)
    update_student_root.destroy()
    show_student()


def update_student():
    global update_student_root, NAme_entry, PHone_entry, EMail_entry, ADdress_entry, GEnder_entry, DOb_entry, ID_entry

    update_student_root = Toplevel()
    update_student_root.resizable(False, False)
    update_student_root.grab_set()

    id_label = ttk.Label(update_student_root, text="Id", font=("times new roman", 20, "bold"))
    id_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")
    ID_entry = ttk.Entry(update_student_root, font=("times new roman", 15, "bold"))
    ID_entry.grid(row=0, column=1, padx=20, pady=15)

    name_label = ttk.Label(update_student_root, text="Name", font=("times new roman", 20, "bold"))
    name_label.grid(row=1, column=0, padx=20, pady=15, sticky="w")
    NAme_entry = ttk.Entry(update_student_root, font=("times new roman", 15, "bold"))
    NAme_entry.grid(row=1, column=1, padx=20, pady=15)

    phone_label = ttk.Label(update_student_root, text="Phone No.", font=("times new roman", 20, "bold"))
    phone_label.grid(row=2, column=0, padx=20, pady=15, sticky="w")
    PHone_entry = ttk.Entry(update_student_root, font=("times new roman", 15, "bold"))
    PHone_entry.grid(row=2, column=1, padx=20, pady=15)

    email_label = ttk.Label(update_student_root, text="Email Address", font=("times new roman", 20, "bold"))
    email_label.grid(row=3, column=0, padx=20, pady=15, sticky="w")
    EMail_entry = ttk.Entry(update_student_root, font=("times new roman", 15, "bold"))
    EMail_entry.grid(row=3, column=1, padx=20, pady=15)

    address_label = ttk.Label(update_student_root, text="Address", font=("times new roman", 20, "bold"))
    address_label.grid(row=4, column=0, padx=20, pady=15, sticky="w")
    ADdress_entry = ttk.Entry(update_student_root, font=("times new roman", 15, "bold"))
    ADdress_entry.grid(row=4, column=1, padx=20, pady=15)

    gender_label = ttk.Label(update_student_root, text="Gender", font=("times new roman", 20, "bold"))
    gender_label.grid(row=5, column=0, padx=20, pady=15, sticky="w")
    GEnder_entry = ttk.Combobox(update_student_root, values=["", "Male", "Female"], state="readonly", width=30)
    GEnder_entry.grid(row=5, column=1, padx=20, pady=15)

    dob_label = ttk.Label(update_student_root, text="Date of Birth", font=("times new roman", 20, "bold"))
    dob_label.grid(row=6, column=0, padx=20, pady=15, sticky="w")
    DOb_entry = ttk.Entry(update_student_root, font=("times new roman", 15, "bold"))
    DOb_entry.grid(row=6, column=1, padx=20, pady=15)

    update_student_button = ttk.Button(update_student_root, text="Update Student", width=15, command=update_data)
    update_student_button.grid(row=7, column=0, columnspan=2, padx=20, pady=15)

    indexing = studentTable.focus()
    content = studentTable.item(indexing)
    list_data = content["values"]
    ID_entry.insert(0, list_data[0])
    NAme_entry.insert(0, list_data[1])
    PHone_entry.insert(0, list_data[2])
    EMail_entry.insert(0, list_data[3])
    ADdress_entry.insert(0, list_data[4])
    GEnder_entry.set(list_data[5])
    DOb_entry.insert(0, list_data[6])


def show_student():
    query = "select * from student"
    cursor.execute(query)
    rows = cursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for row in rows:
        studentTable.insert('', END, values=row)


def delete_student():
    indexing = studentTable.focus()
    content = studentTable.item(indexing)
    content_id = content["values"][0]
    query = "delete from student where id=%s"
    cursor.execute(query, (content_id,))
    con.commit()
    messagebox.showinfo("Success", "Student deleted successfully", parent=root)
    show_student()


def search_data():
    query = "select * from student where id=%s or name=%s or mobile=%s or email=%s or address=%s or gender=%s or dob=%s"
    cursor.execute(query, (Id_entry.get(), Name_entry.get(), Phone_entry.get(), Email_entry.get(), Address_entry.get(),
                           Gender_entry.get(), Dob_entry.get()))
    studentTable.delete(*studentTable.get_children())
    rows = cursor.fetchall()
    if len(rows) != 0:
        for row in rows:
            studentTable.insert('', END, values=row)
    else:
        messagebox.showerror("Error", "No data found", parent=search_student_root)


def search_student():
    global Id_entry, Name_entry, Phone_entry, Email_entry, Address_entry, Gender_entry, Dob_entry, search_student_root
    search_student_root = Toplevel()
    search_student_root.resizable(False, False)
    search_student_root.grab_set()

    id_label = ttk.Label(search_student_root, text="Id", font=("times new roman", 20, "bold"))
    id_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")
    Id_entry = ttk.Entry(search_student_root, font=("times new roman", 15, "bold"))
    Id_entry.grid(row=0, column=1, padx=20, pady=15)

    name_label = ttk.Label(search_student_root, text="Name", font=("times new roman", 20, "bold"))
    name_label.grid(row=1, column=0, padx=20, pady=15, sticky="w")
    Name_entry = ttk.Entry(search_student_root, font=("times new roman", 15, "bold"))
    Name_entry.grid(row=1, column=1, padx=20, pady=15)

    phone_label = ttk.Label(search_student_root, text="Phone No.", font=("times new roman", 20, "bold"))
    phone_label.grid(row=2, column=0, padx=20, pady=15, sticky="w")
    Phone_entry = ttk.Entry(search_student_root, font=("times new roman", 15, "bold"))
    Phone_entry.grid(row=2, column=1, padx=20, pady=15)

    email_label = ttk.Label(search_student_root, text="Email Address", font=("times new roman", 20, "bold"))
    email_label.grid(row=3, column=0, padx=20, pady=15, sticky="w")
    Email_entry = ttk.Entry(search_student_root, font=("times new roman", 15, "bold"))
    Email_entry.grid(row=3, column=1, padx=20, pady=15)

    address_label = ttk.Label(search_student_root, text="Address", font=("times new roman", 20, "bold"))
    address_label.grid(row=4, column=0, padx=20, pady=15, sticky="w")
    Address_entry = ttk.Entry(search_student_root, font=("times new roman", 15, "bold"))
    Address_entry.grid(row=4, column=1, padx=20, pady=15)

    gender_label = ttk.Label(search_student_root, text="Gender", font=("times new roman", 20, "bold"))
    gender_label.grid(row=5, column=0, padx=20, pady=15, sticky="w")
    Gender_entry = ttk.Combobox(search_student_root, values=["", "Male", "Female"], state="readonly", width=30)
    Gender_entry.grid(row=5, column=1, padx=20, pady=15)

    dob_label = ttk.Label(search_student_root, text="Date of Birth", font=("times new roman", 20, "bold"))
    dob_label.grid(row=6, column=0, padx=20, pady=15, sticky="w")
    Dob_entry = ttk.Entry(search_student_root, font=("times new roman", 15, "bold"))
    Dob_entry.grid(row=6, column=1, padx=20, pady=15)

    search_student_button = ttk.Button(search_student_root, text="Search Student", width=15, command=search_data)
    search_student_button.grid(row=7, column=0, columnspan=2, padx=20, pady=15)


def add_data():
    if id_entry.get() == "" or name_entry.get() == "" or phone_entry.get() == "" or email_entry.get() == "" or \
            address_entry.get() == "" or gender_entry.get() == "" or dob_entry.get() == "":
        messagebox.showerror("Error", "All fields are required!", parent=new_student_root)
    else:
        try:
            query = "insert into student values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (id_entry.get(), name_entry.get(), phone_entry.get(), email_entry.get(),
                                   address_entry.get(), gender_entry.get(), dob_entry.get(), time.strftime("%d/%m/%Y"),
                                   time.strftime("%H:%M:%S")))
            con.commit()
            result = messagebox.askyesno("Data Addition Successful",
                                         'Data added successfully.\nDo you want to add more data?',
                                         parent=new_student_root)
            if result:
                id_entry.delete(0, END)
                name_entry.delete(0, END)
                phone_entry.delete(0, END)
                email_entry.delete(0, END)
                address_entry.delete(0, END)
                gender_entry.delete(0, END)
                dob_entry.delete(0, END)
            else:
                new_student_root.destroy()

            show_student()
        except:
            messagebox.showerror("Error", "ID cannot be duplicate", parent=new_student_root)


def new_student():
    global id_entry, name_entry, phone_entry, email_entry, address_entry, gender_entry, dob_entry, new_student_root

    new_student_root = Toplevel()
    new_student_root.resizable(False, False)
    new_student_root.grab_set()

    id_label = ttk.Label(new_student_root, text="Id", font=("times new roman", 20, "bold"))
    id_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")
    id_entry = ttk.Entry(new_student_root, font=("times new roman", 15, "bold"))
    id_entry.grid(row=0, column=1, padx=20, pady=15)

    name_label = ttk.Label(new_student_root, text="Name", font=("times new roman", 20, "bold"))
    name_label.grid(row=1, column=0, padx=20, pady=15, sticky="w")
    name_entry = ttk.Entry(new_student_root, font=("times new roman", 15, "bold"))
    name_entry.grid(row=1, column=1, padx=20, pady=15)

    phone_label = ttk.Label(new_student_root, text="Phone No.", font=("times new roman", 20, "bold"))
    phone_label.grid(row=2, column=0, padx=20, pady=15, sticky="w")
    phone_entry = ttk.Entry(new_student_root, font=("times new roman", 15, "bold"))
    phone_entry.grid(row=2, column=1, padx=20, pady=15)

    email_label = ttk.Label(new_student_root, text="Email Address", font=("times new roman", 20, "bold"))
    email_label.grid(row=3, column=0, padx=20, pady=15, sticky="w")
    email_entry = ttk.Entry(new_student_root, font=("times new roman", 15, "bold"))
    email_entry.grid(row=3, column=1, padx=20, pady=15)

    address_label = ttk.Label(new_student_root, text="Address", font=("times new roman", 20, "bold"))
    address_label.grid(row=4, column=0, padx=20, pady=15, sticky="w")
    address_entry = ttk.Entry(new_student_root, font=("times new roman", 15, "bold"))
    address_entry.grid(row=4, column=1, padx=20, pady=15)

    gender_label = ttk.Label(new_student_root, text="Gender", font=("times new roman", 20, "bold"))
    gender_label.grid(row=5, column=0, padx=20, pady=15, sticky="w")
    gender_entry = ttk.Combobox(new_student_root, values=["", "Male", "Female"], state="readonly", width=30)
    gender_entry.grid(row=5, column=1, padx=20, pady=15)

    dob_label = ttk.Label(new_student_root, text="Date of Birth", font=("times new roman", 20, "bold"))
    dob_label.grid(row=6, column=0, padx=20, pady=15, sticky="w")
    dob_entry = ttk.Entry(new_student_root, font=("times new roman", 15, "bold"))
    dob_entry.grid(row=6, column=1, padx=20, pady=15)

    add_student_button = ttk.Button(new_student_root, text="Add Student", width=15, command=add_data)
    add_student_button.grid(row=7, column=0, columnspan=2, padx=20, pady=15)


def connect():
    try:
        global cursor, con
        con = pymysql.connect(host=host_entry.get(), user=username_entry.get(), password=password_entry.get())
        #con = pymysql.connect(host="localhost", user="root", password="root")
        cursor = con.cursor()
    except:
        messagebox.showerror("Error", "Connection Failed!", parent=top_level_root)
        top_level_root.destroy()
        return
    try:
        query = "create database StudentManagementSystem"
        cursor.execute(query)
        query = "use StudentManagementSystem"
        cursor.execute(query)
        query = "create table student(id int not null primary key, name varchar(50), mobile varchar(10), " \
                "email varchar(30), address varchar(100), gender varchar(20), dob varchar(20), date varchar(50), " \
                "time varchar(50));"
        cursor.execute(query)
    except:
        query = "use StudentManagementSystem"
        cursor.execute(query)
    messagebox.showinfo("Success", "Connection Successful!", parent=top_level_root)
    top_level_root.destroy()
    addStudent.config(state=NORMAL)
    searchStudent.config(state=NORMAL)
    deleteStudent.config(state=NORMAL)
    updateStudent.config(state=NORMAL)
    showStudent.config(state=NORMAL)
    exportData.config(state=NORMAL)


def exit():
    pass


def connect_database():
    global host_entry, username_entry, password_entry, top_level_root

    top_level_root = Toplevel()
    top_level_root.geometry("470x270+730+230")
    top_level_root.title("Connection to Database")
    top_level_root.resizable(False, False)
    top_level_root.grab_set()

    host_label = ttk.Label(top_level_root, text="Host Name", font=("arial", 20, "bold"))
    host_label.grid(row=0, column=0, padx=20)

    host_entry = ttk.Entry(top_level_root, font=("ariel", 15, "bold"))
    host_entry.grid(row=0, column=1, padx=40, pady=20)

    username_label = ttk.Label(top_level_root, text="User Name", font=("arial", 20, "bold"))
    username_label.grid(row=1, column=0, padx=20)

    username_entry = ttk.Entry(top_level_root, font=("ariel", 15, "bold"))
    username_entry.grid(row=1, column=1, padx=40, pady=20)

    password_label = ttk.Label(top_level_root, text="Password", font=("arial", 20, "bold"))
    password_label.grid(row=2, column=0, padx=20)

    password_entry = ttk.Entry(top_level_root, font=("ariel", 15, "bold"), show="*")
    password_entry.grid(row=2, column=1, padx=40, pady=20)

    connect_button = ttk.Button(top_level_root, text="Connect", width=10, command=connect)
    connect_button.grid(row=3, column=0, columnspan=2, pady=20)


def clock():
    date = time.strftime("%d/%m/%Y")
    time1 = time.strftime("%H:%M:%S")
    DateTimeLabel.config(text=f"   Date: {date}\nTime: {time1}")
    DateTimeLabel.after(1000, clock)


root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme("radiance")

root.state('zoomed')
root.resizable(False, False)
root.title("Student Management System")


# root.protocol("WM_DELETE_WINDOW", exit)
# root.overrideredirect(True)


def __CancelCommand():
    pass


root.protocol('WM_DELETE_WINDOW', __CancelCommand)

Label(root, text="Student Management System", font=("times new roman", 40, "bold", "italic", "underline")).pack()

DateTimeLabel = Label(root, font=("times new roman", 19, "bold"))
DateTimeLabel.place(x=0, y=0)
clock()

connectButton = ttk.Button(root, text="Connect Database", cursor="hand2", command=connect_database)
connectButton.place(x=1300, y=10)

leftFrame = Frame(root)
leftFrame.place(x=10, y=100, width=450, height=700)

logo = PhotoImage(file="students.png")
logoLabel = Label(leftFrame, image=logo, bg="white")
logoLabel.grid(row=0, column=1)

addStudent = ttk.Button(leftFrame, text="Add Student", cursor="hand2", width=25, state=DISABLED, command=new_student)
addStudent.grid(row=1, column=1, pady=20)

searchStudent = ttk.Button(leftFrame, text="Search Student", cursor="hand2", width=25, state=DISABLED,
                           command=search_student)
searchStudent.grid(row=2, column=1, pady=20)

deleteStudent = ttk.Button(leftFrame, text="Delete Student", cursor="hand2", width=25, state=DISABLED,
                           command=delete_student)
deleteStudent.grid(row=3, column=1, pady=20)

updateStudent = ttk.Button(leftFrame, text="Update Student", cursor="hand2", width=25, state=DISABLED,
                           command=update_student)
updateStudent.grid(row=4, column=1, pady=20)

showStudent = ttk.Button(leftFrame, text="Show Student", cursor="hand2", width=25, state=DISABLED, command=show_student)
showStudent.grid(row=5, column=1, pady=20)

exportData = ttk.Button(leftFrame, text="Export Data", cursor="hand2", width=25, state=DISABLED, command=export_data)
exportData.grid(row=6, column=1, pady=20)

exitButton = ttk.Button(leftFrame, text="Exit", cursor="hand2", width=25,
                        command=lambda: messagebox.askyesno("Exit", "Do you want to exit?") and root.destroy())
exitButton.grid(row=7, column=1, pady=20)

rightFrame = Frame(root)
rightFrame.place(x=500, y=100, width=1030, height=700)

scrollbarHorizontal = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollbarHorizontal.pack(side=BOTTOM, fill=X)

scrollbarVertical = Scrollbar(rightFrame, orient=VERTICAL)
scrollbarVertical.pack(side=RIGHT, fill=Y)

studentTable = ttk.Treeview(rightFrame, columns=("ID", "Name", "Mobile No", "Email", "Address", "Gender", "D.O.B",
                                                 "Added Date", "Added Time"), xscrollcommand=scrollbarHorizontal.set,
                            yscrollcommand=scrollbarVertical.set)
studentTable.pack(fill=BOTH, expand=1)

scrollbarHorizontal.config(command=studentTable.xview)
scrollbarVertical.config(command=studentTable.yview)

studentTable.config(show="headings")

studentTable.heading("ID", text="ID")
studentTable.heading("Name", text="Name")
studentTable.heading("Mobile No", text="Mobile No")
studentTable.heading("Email", text="Email")
studentTable.heading("Address", text="Address")
studentTable.heading("Gender", text="Gender")
studentTable.heading("D.O.B", text="D.O.B")
studentTable.heading("Added Date", text="Added Date")
studentTable.heading("Added Time", text="Added Time")

studentTable.column("ID", width=50, anchor=CENTER)
studentTable.column("Name", width=300)
studentTable.column("Mobile No", width=200)
studentTable.column("Email", width=300)
studentTable.column("Address", width=400)
studentTable.column("Gender", width=100)
studentTable.column("D.O.B", width=100)
studentTable.column("Added Date", width=100)
studentTable.column("Added Time", width=100)

style = ttk.Style()
style.configure("Treeview.Heading", font=("times new roman", 15, "bold"), rowheight=40)
style.configure("Treeview", font=("ariel", 12), rowheight=30, background="white")

root.mainloop()
