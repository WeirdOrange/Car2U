import sqlite3
import tkinter as tk
import customtkinter as ctk
import pywinstyles
from tkinter import messagebox,StringVar
from PIL import ImageTk, Image

def Database(): #creating connection to database and creating table
    global conn, cursor
    conn = sqlite3.connect("db_member.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, "
        "password TEXT, firstname TEXT, lastname TEXT)")

# Function to handle login button click
def login():
    username = username_entry.get()
    password = password_entry.get()

    # Add your login logic here (e.g., check credentials)
    if username == "admin" and password == "password":
        messagebox.showinfo("Login Successful", "Welcome, Admin!")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def Login():
    Database()
    if username_entry.get() == "" or password_entry.get() == "":
        messagebox.showerror("Error", "Please complete the required field!")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ? and `password` = ?",
                        (username_entry.get(), password_entry.get()))
        if cursor.fetchone() is not None:
            messagebox.showinfo("Success", "You Successfully Login")
            #Home()  # Call Home function after successful login
        else:
            messagebox.showerror("Error", "Invalid Username or password")

def username_onclick(event):
    username_entry.configure(state="normal")
    username_entry.delete(0,"end")
def password_onclick(event):
    password_entry.configure(state="normal", show='*')
    password_entry.delete(0,"end")

def placeholder_return(entry,place):
    if entry.get() == "":
        entry.insert(0,place)
     
def clear_placeholder(self,place):
        self.delete("0", "end")
def add_placeholder():
        if username_entry.get == "":
            username_entry.insert("0", "Enter Username")
        elif password_entry.get == "":
             password_entry.insert(0,"Enter Password")

# Create the main window
root = tk.Tk()
root.title("Login")
root.geometry("1280x720")
root.resizable(False, False)

# Creating Variables
conn = None   #connection to database
cursor = None  #use to execute the sql queries and fetch results from db

# Load and set background image
bg_image = Image.open(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\props\loginbg.png")
bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)  # Updated line
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label to display the background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create username and password labels and entries
username_entry = ctk.CTkEntry(root, font=("Arial", 12), width=300, height=40, bg_color="#000001", corner_radius=45)
userN_P = username_entry.insert(0,"Enter Your Name")
username_entry.place(x=600, y=250)
username_entry.bind("<FocusIn>",username_onclick)
pywinstyles.set_opacity(username_entry,color="#000001")

password_entry = ctk.CTkEntry(root, font=("Arial", 12), width=300, height=40, bg_color="#000001", corner_radius=45)
passW_P = password_entry.insert(0,"Enter Password")
password_entry.place(x=600, y=320)
password_entry.bind("<FocusIn>",password_onclick)
pywinstyles.set_opacity(password_entry,color="#000001")

# Create login button
login_button = ctk.CTkButton(root, text="Login", font=("Arial", 18), width=300, height=40, bg_color="#000001", fg_color=("#F47749","white"), corner_radius=50, command=login)
login_button.place(x=600, y=380)
pywinstyles.set_opacity(login_button,color="#000001")

# Create sign-up button
signup_button = ctk.CTkButton(root, text="Sign up", font=("Arial", 10, "bold"), width=80, height=25, bg_color="#000001", fg_color=("red","white"))
signup_button.place(x=820, y=430)
pywinstyles.set_opacity(signup_button,color="#000001")

# Start the main loop
root.mainloop()