import sqlite3
import tkinter as tk
import customtkinter as ctk
import pywinstyles
from tkinter import messagebox,StringVar,Frame,Toplevel
from PIL import ImageTk, Image

def Database(): #creating connection to database and creating table
    global conn, cursor
    conn = sqlite3.connect("car2u.db")
    cursor = conn.cursor()

def userPlaceholder(event):
    if email_entry.get() == "":
        password_entry.configure(show="normal")
        email_entry.insert(0, "Enter Email")

def removeUserPlaceholder(event):
    if email_entry.get() == "Enter Email":
        email_entry.delete(0, tk.END)

def passwPlaceholder(event):
    if password_entry.get() == "":
        password_entry.configure(show="")
        password_entry.insert(0, "Enter Password")

def removePasswPlaceholder(event):
    if password_entry.get() == "Enter Password":
        password_entry.delete(0, tk.END)
        password_entry.configure(0, show="*")

def open_signup(current_window, signup_callback):
    messagebox.showinfo("Signup", "Redirecting to Sign Up Page...")
    current_window.destroy()  # Close the login window
    signup_callback()

def logingui(signup_callback):    
    global loginFrame, bg_photo,email_entry,password_entry
    loginFrame = Toplevel()
    loginFrame.title("Login")
    loginFrame.geometry("1280x720")
    loginFrame.resizable(False, False)

    # Load and set background image
    bg_image = Image.open(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\props\loginbg.png")
    bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)  # Updated line
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Create a label to display the background image
    bg_label = tk.Label(loginFrame, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Create email and password labels and entries
    email_entry = ctk.CTkEntry(loginFrame, font=("Arial", 12), width=300, height=40, bg_color="#000001", corner_radius=45)
    email_entry.insert(0,"Enter Email")
    email_entry.place(x=600, y=250)
    email_entry.bind("<FocusIn>",removeUserPlaceholder)
    email_entry.bind("<FocusOut>",userPlaceholder)
    pywinstyles.set_opacity(email_entry,color="#000001")

    password_entry = ctk.CTkEntry(loginFrame, font=("Arial", 12), width=300, height=40, bg_color="#000001", corner_radius=45)
    password_entry.insert(0,"Enter Password")
    password_entry.place(x=600, y=320)
    password_entry.bind("<FocusIn>",removePasswPlaceholder)
    password_entry.bind("<FocusOut>",passwPlaceholder)
    pywinstyles.set_opacity(password_entry,color="#000001")

    # Create login button
    login_button = ctk.CTkButton(loginFrame, text="Login", font=("Arial", 18), width=300, height=40, 
                                 bg_color="#FFA843", fg_color=("#F47749","white"), corner_radius=50, 
                                 command=lambda:LoginAccess(email_entry.get(),password_entry.get()))
    login_button.place(x=600, y=380)
    pywinstyles.set_opacity(login_button,color="#FFA843")

    # Create sign-up button
    signup_button = ctk.CTkButton(loginFrame, text="Sign up", font=("Arial", 10, "bold"), width=80, height=25, 
                                  bg_color="#FFA843", fg_color=("#FE1A0A","white"),command=lambda:open_signup(loginFrame,signup_callback))
    signup_button.place(x=820, y=430)
    pywinstyles.set_opacity(signup_button,color="#FFA843")

    title_label = ctk.CTkLabel(loginFrame, text="Login Your Account", font=("Cooper Black", 36), bg_color="#FFAB40")
    title_label.place(x=340, y=160)
    pywinstyles.set_opacity(title_label,color="#FFAB40")
    subtitle_label = ctk.CTkLabel(loginFrame,text="Glad to have you with us.",font=("Eras Bold ITC",24),bg_color="#FFAB40")
    subtitle_label.place(x=800,y=80)
    pywinstyles.set_opacity(subtitle_label,color="#FFAB40")

# Function to handle login button click
def LoginAccess(email,password):
    Database()
    if email == "" or password == "":
        messagebox.showerror("Error", "Please complete the required field!")
    else:
        cursor.execute("SELECT * FROM CUSTUSER WHERE `email` = ? and `userPassword` = ?",(email,password))
        if cursor.fetchone() is not None:
            messagebox.showinfo("Success", "You Successfully Login")
            #Home()  # Call Home function after successful login
        else:
            messagebox.showerror("Error", "Invalid Username or password")


# Start the main loop
#root.mainloop()