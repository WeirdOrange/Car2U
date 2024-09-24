from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
import customtkinter as ctk
import tkinter as tk
import pywinstyles
from PIL import ImageTk, Image

# Function to handle sign-up button click
def sign_up():
    name = name_entry.get()
    email = email_entry.get()
    age = age_entry.get()
    dob_day = dob_day_entry.get()
    dob_month = dob_month_entry.get()
    dob_year = dob_year_entry.get()
    contact = contact_entry.get()

    # Simple validation
    if not name or not email or not age or not dob_day or not dob_month or not dob_year or not contact:
        messagebox.showerror("Input Error", "All fields are required!")
    else:
        messagebox.showinfo("Registration Successful", "You have successfully signed up!")

# Function to handle login button click
def log_in():
    messagebox.showinfo("Login", "Redirecting to Login Page...")

# Create main application window
root = tk.Tk()
root.title("Sign Up")
root.geometry("1280x720")
root.resizable(False, False)

# Load and set background image
background_image = Image.open(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\props\signupbg.png")
background_image = background_image.resize((1280, 720), Image.Resampling.LANCZOS) 
background_photo = ImageTk.PhotoImage(background_image)

background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Creating labels and entry fields
name_label = ctk.CTkLabel(root, text="Name\t\t:", bg_color="#FFAB40", font=('Arial Bold', 16))
name_label.place(x=250, y=200)
pywinstyles.set_opacity(name_label,color="#FFAB40")
name_entry = tk.Entry(root, font=('Arial', 16))
name_entry.place(x=410, y=200)

email_label = ctk.CTkLabel(root, text="Email Address\t:", bg_color="#FFAB40", font=('Arial Bold', 16))
email_label.place(x=250, y=250)
pywinstyles.set_opacity(email_label,color="#FFAB40")
email_entry = tk.Entry(root, font=('Arial', 16))
email_entry.place(x=410, y=250)

dob_label = ctk.CTkLabel(root, text="Date Of Birth\t:", bg_color="#FFAB40", font=('Arial Bold', 16))
dob_label.place(x=250, y=300)
pywinstyles.set_opacity(dob_label,color="#FFAB40")
dob_day_entry = tk.Entry(root, width=3, font=('Arial', 16))
dob_day_entry.place(x=410, y=300)
dob_month_entry = tk.Entry(root, width=3, font=('Arial', 16))
dob_month_entry.place(x=460, y=300)
dob_year_entry = tk.Entry(root, width=5, font=('Arial', 16))
dob_year_entry.place(x=510, y=300)

contact_label = ctk.CTkLabel(root, text="Contact No\t:", bg_color="#FFAB40", font=('Arial Bold', 16))
contact_label.place(x=250, y=350)
pywinstyles.set_opacity(contact_label,color="#FFAB40")
contact_entry = tk.Entry(root, font=('Arial', 16))
contact_entry.place(x=410, y=350)

passW_label = ctk.CTkLabel(root, text="Password\t:", bg_color="#FFAB40", font=('Arial Bold', 16))
passW_label.place(x=250, y=400)
pywinstyles.set_opacity(passW_label,color="#FFAB40")
passW_entry = tk.Entry(root, font=('Arial', 16))
passW_entry.place(x=410, y=400)

cpassW_label = ctk.CTkLabel(root, text="Confirm Password\t:", bg_color="#FFAB40", font=('Arial Bold', 16))
cpassW_label.place(x=250,y=450)
pywinstyles.set_opacity(cpassW_label,color="#FFAB40")
cpassW_entry = tk.Entry(root, font=('Arial', 16))
cpassW_entry.place(x=410, y=450)

# Sign-up button
sign_up_button = ctk.CTkButton(root, text="Sign Up", font=('Arial', 16), width=247, height=30, bg_color="#FFAB40", corner_radius=10, command=sign_up)
sign_up_button.place(x=410, y=500)
pywinstyles.set_opacity(sign_up_button,color="#FFAB40")

# Log in button
login_label = ctk.CTkLabel(root, text="Already registered?", bg_color="#FFAB40", font=('Arial Bold', 10))
login_label.place(x=510,y=540)
pywinstyles.set_opacity(login_label,color="#FFAB40")
login_button = tk.Button(root, text="Log In", font=('Arial', 10), bg="red", fg="white", command=log_in)
login_button.place(x=610, y=540)

# Title and subtitle on the right
title_label = ctk.CTkLabel(root, text="Register Now!", font=('Arial Bold', 32), bg_color="#FFAB40")
title_label.place(x=750, y=280)
pywinstyles.set_opacity(title_label,color="#FFAB40")
subtitle_label = ctk.CTkLabel(root, text="Few more steps to make your trip better!", font=('Arial', 20), bg_color="#FFAB40")
subtitle_label.place(x=700, y=320)
pywinstyles.set_opacity(subtitle_label,color="#FFAB40")

# Start the Tkinter main loop
root.mainloop()
