import sqlite3
import tkinter as tk
import customtkinter as ctk
import pywinstyles
from Car2U_UserInfo import set_user_info
from pathlib import Path
from tkinter import messagebox,Toplevel
from PIL import ImageTk, Image

# Set up the asset path 
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Login")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def Database(): #creating connection to database and creating table
    global conn, cursor
    conn = sqlite3.connect("car2u.db")
    conn.row_factory = sqlite3.Row
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
    current_window.destroy()  # Close the login window
    signup_callback()

def open_home(current_window, home_callback):
    current_window.destroy()  # Close the login window
    home_callback()

def open_adminHome(current_window, adminHome_callback):
    current_window.destroy()  # Close the login window
    adminHome_callback()

def logingui(signup_callback,home_callback,adminHome_callback):
    # Create the main application window
    global loginFrame,email_entry,password_entry
    loginFrame = Toplevel()
    loginFrame.title("Login")
    loginFrame.geometry("1280x720")
    loginFrame.resizable(False, False)

    # Background image
    bg_image = ctk.CTkImage(Image.open(relative_to_assets("image_1.png")),size=(1073,720))
    bg_label = ctk.CTkLabel(loginFrame, image=bg_image,text="")
    bg_label.place(x=207, y=0)
    
    rectangle1_img = ctk.CTkImage(Image.open(relative_to_assets("image_2.png")),size=(527,720))
    rectangle1 = ctk.CTkLabel(loginFrame, image=rectangle1_img,text="")
    rectangle1.place(x=0, y=0)

    rectangle2_img = ctk.CTkImage(Image.open(relative_to_assets("image_3.png")),size=(880,500))
    rectangle2 = ctk.CTkLabel(loginFrame, image=rectangle2_img,text="")
    rectangle2.place(x=278, y=110)

    car_img = ctk.CTkImage(Image.open(relative_to_assets("car.png")),size=(545,545))
    car_bg = ctk.CTkLabel(loginFrame, image=car_img,text="", bg_color="#FC4F3E", fg_color="#FC4F3E")
    car_bg.place(x=192, y=270)
    pywinstyles.set_opacity(car_bg,color="#FC4F3E")

    # Return to main page
    home_image = ctk.CTkImage(Image.open(relative_to_assets("image_5.png")),size=(30,30))
    home_button = ctk.CTkButton(master=loginFrame, text="  Home", image=home_image, width=120, 
                                fg_color=("#F86544","#FA5740"), bg_color="#FA5740", text_color="#000000", 
                                font=("Tw Cen MT Condensed Extra Bold", 20),command=lambda:open_home(loginFrame,home_callback))
    home_button.place(x=30, y=20)
    pywinstyles.set_opacity(home_button,color="#FA5740")
    
    logo_img = ctk.CTkImage(Image.open(relative_to_assets("logo.png")),size=(90,45))
    logo_label = ctk.CTkLabel(master=loginFrame, text="", image=logo_img, fg_color="#FF865A", bg_color="#FF865A")
    logo_label.place(x=160, y=15)
    pywinstyles.set_opacity(logo_label,color="#FF865A")
    
    prop_image = ctk.CTkImage(Image.open(relative_to_assets("image_4.png")),size=(86,106))
    prop_label = ctk.CTkLabel(master=loginFrame, text="", image=prop_image, fg_color="#FFC739", bg_color="#FFC739")
    prop_label.place(x=900, y=145)
    pywinstyles.set_opacity(prop_label,color="#FFC739")

    # Create email and password labels and entries
    email_entry = ctk.CTkEntry(loginFrame, font=("Arial", 12), width=350, height=45, bg_color="#000001", corner_radius=45)
    email_entry.insert(0,"Enter Email")
    email_entry.place(x=700, y=250)
    email_entry.bind("<FocusIn>",removeUserPlaceholder)
    email_entry.bind("<FocusOut>",userPlaceholder)
    pywinstyles.set_opacity(email_entry,color="#000001")

    password_entry = ctk.CTkEntry(loginFrame, font=("Arial", 12), width=350, height=45, bg_color="#000001", corner_radius=45)
    password_entry.insert(0,"Enter Password")
    password_entry.place(x=700, y=310)
    password_entry.bind("<FocusIn>",removePasswPlaceholder)
    password_entry.bind("<FocusOut>",passwPlaceholder)
    pywinstyles.set_opacity(password_entry,color="#000001")

    # Create login button
    login_button = ctk.CTkButton(loginFrame, text="Login", font=("Arial", 18), width=350, height=40, 
                                 bg_color="#FFA843", fg_color=("#F47749","white"), corner_radius=50, 
                                 command=lambda:LoginAccess(email_entry.get(),password_entry.get(),home_callback,adminHome_callback))
    login_button.place(x=700, y=375)
    pywinstyles.set_opacity(login_button,color="#FFA843")

    # Create sign-up button
    signup_label = ctk.CTkLabel(loginFrame, text="New User?", bg_color="#FFA843", font=("Arial", 10, "bold"))
    signup_label.place(x=900,y=422)
    pywinstyles.set_opacity(signup_label,color="#FFA843")
    signup_button = ctk.CTkButton(loginFrame, text="Sign up", font=("Arial", 10, "bold"), width=80,
                                  bg_color="#FFA843", fg_color=("#FE1A0A","white"),command=lambda:open_signup(loginFrame,signup_callback))
    signup_button.place(x=968, y=425)
    pywinstyles.set_opacity(signup_button,color="#FFA843")

    title_label = ctk.CTkLabel(loginFrame, text="Login Your Account", font=("Cooper Black", 36), bg_color="#FFAB40")
    title_label.place(x=340, y=160)
    pywinstyles.set_opacity(title_label,color="#FFAB40")
    subtitle_label = ctk.CTkLabel(loginFrame,text="Glad to have you with us.",font=("Eras Bold ITC",24),bg_color="#FFAB40")
    subtitle_label.place(x=800,y=80)
    pywinstyles.set_opacity(subtitle_label,color="#FFAB40")

# Function to handle login button click
def LoginAccess(email,password,home_callback,adminHome_callback):
    global userid
    userid = ""
    Database()
    
    if email == "" or password == "":
        messagebox.showerror("Error", "Please complete the required fields!")
        return
    
    # Check in RentalAgency table
    cursor.execute("SELECT agencyID FROM RentalAgency WHERE `agencyEmail` = ? and `agencyPassword` = ?", (email, password))
    result = cursor.fetchone()
    
    if result:  # Check if result is not None
        userid = result[0]  # Get agencyID
        messagebox.showinfo("Success", "You Successfully Login")
        set_user_info(userid)
        open_adminHome(loginFrame, adminHome_callback)  # Call Admin Home function after successful login
        return
    
    # Check in UserDetails table
    cursor.execute("SELECT userID FROM UserDetails WHERE `email` = ? and `password` = ?", (email, password))
    result = cursor.fetchone()
    
    if result:  # Check if result is not None
        userid = result[0]  # Get userID
        messagebox.showinfo("Success", "You Successfully Login")
        set_user_info(userid)
        open_home(loginFrame, home_callback)  # Call Home function after successful login
    else:
        messagebox.showerror("Error", "Invalid Username or Password")