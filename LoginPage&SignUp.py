import sqlite3
from tkinter import *
from tkinter import messagebox
import os

# ---------------- DATABASE SETUP ----------------
DB_PATH = r"C:\Users\Chan Kok Han\Desktop\Semester 1 to 5\Software Engineering\software engineering\5001CEM-main\staff_training.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Staff_Information (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------- WINDOW SETUP ----------------
window = Tk()
window.title("Staff Training Tracking System")
window.state('zoomed')
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

# ---------------- FRAMES ----------------
login = Frame(window, bg='white')
staffhomepage = Frame(window, bg='white')
staffenrolpage = Frame(window, bg='white')

for frame in (login, staffhomepage, staffenrolpage):
    frame.grid(row=0, column=0, sticky='nsew')

def show_frame(frame):
    frame.tkraise()

show_frame(login)

# ---------------- FUNCTIONS ----------------
def on_enter():
    username = usernameEntry.get()
    password = passwordEntry.get()

    if username == "" or password == "":
        messagebox.showinfo('No blank spaces', 'Please fill up the details.')
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Staff_Information WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        messagebox.showinfo('Success', 'Login Successful')
        usernameEntry.delete(0, END)
        passwordEntry.delete(0, END)
        show_frame(staffhomepage)
    else:
        messagebox.showinfo('Failed', 'Invalid username or password')

def logout_system():
    if messagebox.askyesno('Confirmation', 'Are you sure you want to logout?'):
        show_frame(login)
        messagebox.showinfo('Logout', 'You have successfully Logged Out!')

def create_account():
    username = signup_username.get()
    password = signup_password.get()
    repassword = signup_repassword.get()

    # ---------------- Blank fields check ----------------
    if username == "" or password == "" or repassword == "":
        messagebox.showerror("Error", "All fields are required")
        return

    # ---------------- Minimum length check ----------------
    if len(username) < 8 or len(password) < 8:
        messagebox.showerror("Error", "Username and Password must be at least 8 characters long")
        return

    # ---------------- Password match check ----------------
    if password != repassword:
        messagebox.showerror("Error", "Passwords do not match. Please try again.")
        signup_password.delete(0, END)
        signup_repassword.delete(0, END)
        return

    # ---------------- Save to database ----------------
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Staff_Information (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Account created successfully!")
        signup_username.delete(0, END)
        signup_password.delete(0, END)
        signup_repassword.delete(0, END)
        show_frame(login)

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists")


# ---------------- LOGIN PAGE (Original Layout) ----------------
login.configure(bg='white')

# Left Frames
frame1 = Frame(login, bg="white")
frame2 = Frame(login, bg="white")
frame1.pack(expand=True, fill=BOTH, side=LEFT)
frame2.pack(expand=False, side=LEFT)

Label(frame1, text='Sign In', font=('Regular', 25, 'bold'), bg='white').place(x=200, y=124)
Label(frame2, text='Sign Up', font=('Regular', 25, 'bold'), bg='white').place(x=269, y=124)

# Right panel (pink)
subframe = Frame(login, bg="#E84966")
subframe.pack(expand=True, fill=BOTH, side=RIGHT)

Label(subframe, text='Welcome to', font=('Regular', 50, 'bold'),
      bg="#E84966", fg="white").place(x=125, y=364)
Label(subframe, text='Login', font=('Regular', 50, 'bold'),
      bg="#E84966", fg="white").place(x=225, y=464)

# Username
Label(login, text='Username', font=('Regular', 20, 'bold'), bg='white').place(x=116, y=268)
usernameEntry = Entry(login, width=30, font=('Microsoft Yahei UI light', 14),
                      highlightthickness=2, bd=0, bg='grey')
usernameEntry.place(x=116, y=341)

# Password
Label(login, text='Password', font=('Regular', 20, 'bold'), bg='white').place(x=116, y=469)
passwordEntry = Entry(login, width=30, font=('Microsoft Yahei UI light', 14),
                      highlightthickness=2, bd=0, bg='grey', show="*")
passwordEntry.place(x=116, y=533)

# Buttons side by side
button_frame = Frame(login, bg='white')
button_frame.place(x=116, y=664)

loginButton = Button(button_frame, text='Sign In', font=('Regular', 20, 'bold'),
                     fg='white', bg='#E84966', width=10, cursor='hand2', command=on_enter)
loginButton.grid(row=0, column=0, padx=10)

signupButton = Button(button_frame, text='Sign Up', font=('Regular', 20, 'bold'),
                      fg='white', bg='#4CAF50', width=10, cursor='hand2',
                      command=lambda: show_frame(staffenrolpage))
signupButton.grid(row=0, column=1, padx=10)

# ---------------- SIGN UP PAGE ----------------
staffenrolpage.configure(bg="white")
Label(staffenrolpage, text="Sign Up", font=('Regular', 30, 'bold'), bg='white').place(x=200, y=120)

Label(staffenrolpage, text="Username", font=('Regular', 18), bg='white').place(x=200, y=230)
signup_username = Entry(staffenrolpage, width=30, font=('Microsoft Yahei UI light', 14))
signup_username.place(x=200, y=270)

Label(staffenrolpage, text="Password", font=('Regular', 18), bg='white').place(x=200, y=330)
signup_password = Entry(staffenrolpage, width=30, font=('Microsoft Yahei UI light', 14), show="*")
signup_password.place(x=200, y=370)

Label(staffenrolpage, text="Re-enter Password", font=('Regular', 18), bg='white').place(x=200, y=430)
signup_repassword = Entry(staffenrolpage, width=30, font=('Microsoft Yahei UI light', 14), show="*")
signup_repassword.place(x=200, y=470)

Button(staffenrolpage, text="Create Account", font=('Regular', 18, 'bold'),
       bg="#4CAF50", fg="white", width=15, command=create_account).place(x=200, y=540)

Button(staffenrolpage, text="Back to Login", font=('Regular', 14),
       command=lambda: show_frame(login)).place(x=200, y=600)

# ---------------- STAFF HOME PAGE ----------------
Label(staffhomepage, text="Welcome to Staff Homepage",
      font=("Arial", 30, "bold"), bg="white").pack(pady=200)
Button(staffhomepage, text="Logout", font=("Arial", 16), command=logout_system).pack()

# ---------------- START APP ----------------
window.mainloop()
