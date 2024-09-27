from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, Toplevel
import customtkinter as ctk
import tkinter as tk
import pywinstyles
import sqlite3
from dateutil.parser import parse
from PIL import ImageTk, Image

# Connecting to database
def Database():
    global conn, cursor
    conn = sqlite3.connect("car2u.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS CUSTUSER(
                            email varchar(100) PRIMARY KEY NOT NULL,
                            name varchar(50) NOT NULL,
                            dob date NOT NULL,
                            contactNo varchar(15),
                            userPassword varchar(50) NOT NULL,
                            profilePic BLOB )""")

# Function to handle sign-up button click
def sign_up_get(name,email,dob_day,dob_month,dob_year,contact,password,cpassword):
    Database()
    dob = str(dob_year).zfill(4)+"-"+str(dob_month).zfill(2)+"-"+str(dob_day).zfill(2)
    while(True):
        try:
            DDate = parse(dob)  # Error Test parse
            break    # Break pulls you out of the loop
        except:
            print("INVALID Date: ",dob)
    # Simple validation
    if not name or not email or not dob_day or not dob_month or not dob_year or not contact or not password or not cpassword:
        messagebox.showerror("Input Error", "All fields are required!")
    elif password != cpassword:
        messagebox.showerror("Input Error", "Password and Confirm Password do not match.")
    else:
        try:
            cursor.execute("SELECT * FROM CUSTUSER WHERE `email` = ?",(str(email),))
            if cursor.fetchone() is not None:
                messagebox.showerror("Error","Email is already Registered!")
            else:
                cursor.execute(
                    "INSERT INTO CUSTUSER(email,name,dob,contactNo,userPassword) VALUES (?,?,?,?,?)",
                    (str(email),str(name),str(DDate),str(contact),str(password)))
                conn.commit()
                messagebox.showinfo("Registration Successful", "You have successfully signed up!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", "Error occurred during registration: {}".format(e))
        finally:
            conn.close()

# Function to handle login button click
def open_login(current_window, signup_callback):
    messagebox.showinfo("Login", "Redirecting to Login Page...")
    current_window.destroy()  # Close the signup window
    signup_callback()

def signupgui(login_callback):
    global RegisterFrame, background_photo
    RegisterFrame = Toplevel()
    RegisterFrame.title("Sign Up")
    RegisterFrame.geometry("1280x720")
    RegisterFrame.resizable(False, False)

    # Load and set background image
    background_image = Image.open(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\props\signupbg.png")
    background_image = background_image.resize((1280, 720), Image.Resampling.LANCZOS) 
    background_photo = ImageTk.PhotoImage(background_image)

    background_label = tk.Label(RegisterFrame, image=background_photo)
    background_label.place(relwidth=1, relheight=1)

    # Creating labels and entry fields
    name_label = ctk.CTkLabel(RegisterFrame, text="Name\t\t:", bg_color="#FFAB40", font=('Arial Bold', 16))
    name_label.place(x=250, y=200)
    pywinstyles.set_opacity(name_label,color="#FFAB40")
    name_entry = tk.Entry(RegisterFrame, font=('Lucida Console', 16))
    name_entry.place(x=410, y=200)

    email_label = ctk.CTkLabel(RegisterFrame, text="Email Address\t:", bg_color="#FFAB40", font=('Arial Bold', 16))
    email_label.place(x=250, y=250)
    pywinstyles.set_opacity(email_label,color="#FFAB40")
    email_entry = tk.Entry(RegisterFrame, font=('Lucida Console', 16))
    email_entry.place(x=410, y=250)

    dob_label = ctk.CTkLabel(RegisterFrame, text="Date Of Birth\t:", bg_color="#FFAB40", font=('Arial Bold', 16))
    dob_label.place(x=250, y=300)
    pywinstyles.set_opacity(dob_label,color="#FFAB40")
    dob_day_entry = tk.Entry(RegisterFrame, width=3, font=('Lucida Console', 16))
    dob_day_entry.place(x=410, y=300)
    dob_month_entry = tk.Entry(RegisterFrame, width=3, font=('Lucida Console', 16))
    dob_month_entry.place(x=460, y=300)
    dob_year_entry = tk.Entry(RegisterFrame, width=5, font=('Lucida Console', 16))
    dob_year_entry.place(x=510, y=300)

    contact_label = ctk.CTkLabel(RegisterFrame, text="Contact No\t:", bg_color="#FFAB40", font=('Arial Bold', 16))
    contact_label.place(x=250, y=350)
    pywinstyles.set_opacity(contact_label,color="#FFAB40")
    contact_entry = tk.Entry(RegisterFrame, font=('Lucida Console', 16))
    contact_entry.place(x=410, y=350)

    passW_label = ctk.CTkLabel(RegisterFrame, text="Password\t:", bg_color="#FFAB40", font=('Arial Bold', 16))
    passW_label.place(x=250, y=400)
    pywinstyles.set_opacity(passW_label,color="#FFAB40")
    passW_entry = tk.Entry(RegisterFrame, font=('Lucida Console', 16))
    passW_entry.place(x=410, y=400)

    cpassW_label = ctk.CTkLabel(RegisterFrame, text="Confirm Password\t:", bg_color="#FFAB40", font=('Arial Bold', 16))
    cpassW_label.place(x=250,y=450)
    pywinstyles.set_opacity(cpassW_label,color="#FFAB40")
    cpassW_entry = tk.Entry(RegisterFrame, font=('Lucida Console', 16))
    cpassW_entry.place(x=410, y=450)


    # Sign-up button
    sign_up_button = ctk.CTkButton(RegisterFrame, text="Sign Up", font=('Arial Bold', 16), width=247, height=30, 
                                   bg_color="#FFA843", fg_color=("#FC503E","white"), corner_radius=10, 
                                   command=lambda:sign_up_get(name_entry.get(),email_entry.get(),dob_day_entry.get(),dob_month_entry.get(),dob_year_entry.get(),contact_entry.get(),passW_entry.get(),cpassW_entry.get()))
    sign_up_button.place(x=410, y=500)
    pywinstyles.set_opacity(sign_up_button,color="#FFA843")

    # Log in button
    login_label = ctk.CTkLabel(RegisterFrame, text="Already registered?", bg_color="#FFAB40", font=('Arial Bold', 11))
    login_label.place(x=478,y=540)
    pywinstyles.set_opacity(login_label,color="#FFAB40")
    login_button = ctk.CTkButton(RegisterFrame, text="Log In", font=('Arial Bold', 11), bg_color="#FF7E52", fg_color=("#FE1A0A","white"), width=50,
                             corner_radius=50, command=lambda:open_login(RegisterFrame,login_callback))
    login_button.place(x=592, y=540)
    pywinstyles.set_opacity(login_button,color="#FF7E52")

    # Title and subtitle on the right
    title_label = ctk.CTkLabel(RegisterFrame, text="Register Now!", font=('Arial Bold', 32), bg_color="#FFAB40")
    title_label.place(x=750, y=280)
    pywinstyles.set_opacity(title_label,color="#FFAB40")
    subtitle_label = ctk.CTkLabel(RegisterFrame, text="Few more steps to make your trip better!", font=('Arial', 20), bg_color="#FFAB40")
    subtitle_label.place(x=700, y=320)
    pywinstyles.set_opacity(subtitle_label,color="#FFAB40")

# Start the Tkinter main loop
#root.mainloop()
