import customtkinter as ctk
import tkinter as tk
import pywinstyles
import sqlite3
import smtplib
import ssl
import easygui
import random, string
import hashlib
from datetime import date
from dateutil.parser import parse
from PIL import Image
from email.message import EmailMessage
from pathlib import Path
from tkinter import messagebox, Toplevel

# Set up the asset path (same as original)
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Main-SignUp")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Connecting to database
def Database():
    global conn, cursor
    conn = sqlite3.connect("car2u.db")
    cursor = conn.cursor()

# Function to handle sign-up button click
def sign_up_get(login_callback,name,email,dob_day,dob_month,dob_year,contact,password,cpassword):
    global otp
    Database()
    dob_year = str(dob_year).zfill(4)
    dob_month = str(dob_month).zfill(2)
    dob_day = str(dob_day).zfill(2)
        
    # Validation
    while True:
        if not name or not email or not dob_day or not dob_month or not dob_year or not contact or not password or not cpassword:
            messagebox.showerror("Input Error", "All fields are required!")
        elif password != cpassword:
            messagebox.showerror("Input Error", "Password and Confirm Password do not match.")
        elif len(str(password[0])) < 8:
            messagebox.showerror("Invalid Password","Passwords are required to have at least 8 letters. Please try again.")
        else:
            password = hashlib.sha256(str(password).encode()).hexdigest()
            while(True):
                try:
                    dob = ""
                    dob = date(int(dob_year),int(dob_month),int(dob_day))
                    print(dob)
                    break    # Break pulls you out of the loop
                
                except ValueError:  # Handle invalid date input
                    print("INVALID Date: ", dob_year, dob_month, dob_day)
                    messagebox.showerror("Input Error", "Invalid Date. Please enter a valid date.")
                    break  # Optionally break the loop if you want to stop after invalid input
            try:
                cursor.execute("SELECT * FROM UserDetails WHERE `email` = ?",(str(email),))
                if cursor.fetchone() is not None:
                    messagebox.showerror("Error","Email is already Registered!")
                else:
                    # Sending OTP to user
                    subject = 'Car2U: OTP to verify your identity'
                    body = f"""Hi {name},\nYour OTP is : {otp}\nNever Share this code to others. If this is not your actions, please contact our customer service.
                            \n\nCar2U contact: 016-407 5284 or email via this account"""
                    emailNotif(email,subject,body)
                    conn.close()

                    # Validate email    
                    while True:
                        userotp = easygui.enterbox("Enter OTP (Press cancel to request for another OTP): ","Check Your Email for OTP")
                        
                        if userotp == otp: # If OTP is enter correctly
                            Database()
                            cursor.execute("INSERT INTO UserDetails(email,name,dob,contactNo,password) VALUES (?,?,?,?,?)",
                                            (str(email),str(name),dob,str(contact),str(password)))
                            conn.commit()
                            messagebox.showinfo("Registration Successful", "You have successfully signed up!")
                            
                            # Notify user through email as well
                            subject = 'Registration Completed!'
                            body = f"""Someone has registered this email account in the Car2U application.
                                \nName: {name}\nEmail: {email}\nBirth Date: {dob}\nContact No: {contact}
                                \nIf this is not you, please contact Car2U as soon as possible. 
                                \nPlease ignore this message if this was you.\n\nCar2U contact: 016-407 5284"""
                            emailNotif(email,subject,body)
                            open_login(RegisterFrame,login_callback)
                            break

                        elif userotp is None:  # If the user clicks "Cancel" (user_input will be None)
                            # Display the buttonbox with options
                            choice = easygui.buttonbox("You clicked Cancel. What would you like to do next?", "Options", 
                                                    choices=["Back", "Resend OTP", "Cancel"])
                            
                            if choice == "Back":
                                # Return back to the enterbox (loop continues)
                                continue  # This goes back to the beginning of the loop
                            
                            elif choice == "Resend OTP":
                                otp = ""
                                for x in range(5):
                                    otp = otp + str(random.choice(string.ascii_letters))
                                
                                easygui.msgbox("Resending OTP.", "Do check your email for an OTP. (Delay might happen)")
                                
                                # Sending OTP to user
                                subject = 'Car2U: OTP to verify your identity'
                                body = f"""Hi {name},\nYour OTP is : {otp}\nNever Share this code to others. If this is not your actions, please contact our customer service.
                                \n\nCar2U contact: 016-407 5284 or email via this account"""
                                emailNotif(email,subject,body)
                                continue
                            
                            elif choice == "Cancel":
                                easygui.msgbox(f"Registration Terminated", "Press the 'Sign Up' button again to register")
                            break  # Exit the loop if the user doesn't want to continue
                        else:
                            easygui.msgbox(f"Wrong OTP Value", "The entered OTP is incorrect. Check if you had entered a space?")
                            continue
                            
            except sqlite3.Error as e:
                messagebox.showerror("Error", "Error occurred during registration: {}".format(e))
            finally:
                conn.close()
    
# Email notification
def emailNotif(email_receiver,subject,body):
    # Define email sender and receiver
    email_sender = 'cartwoyouofficial@gmail.com'
    email_password = 'asjy kqjh eizl wgnu'

    # Set up the email
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

# Function to handle login button click
def open_login(current_window, login_callback):
    current_window.destroy()  # Close the signup window
    login_callback()
    
def open_home(current_window, home_callback):
    current_window.destroy()  # Close the login window
    home_callback()

def signupgui(login_callback, home_callback):
    global RegisterFrame
    RegisterFrame = Toplevel()
    RegisterFrame.title("Sign Up")
    RegisterFrame.geometry("1280x720")
    RegisterFrame.resizable(False, False)

    # For signup verification
    global otp
    otp = ""
    for x in range(5):
        otp = otp + str(random.choice(string.ascii_letters))

    # Load and set background image
    bg_image = ctk.CTkImage(Image.open(relative_to_assets("image_1.png")),size=(1073,720))
    bg_label = ctk.CTkLabel(RegisterFrame, image=bg_image,text="")
    bg_label.place(x=207, y=0)
    
    rectangle1_img = ctk.CTkImage(Image.open(relative_to_assets("image_2.png")),size=(527,720))
    rectangle1 = ctk.CTkLabel(RegisterFrame, image=rectangle1_img,text="")
    rectangle1.place(x=0, y=0)

    rectangle2_img = ctk.CTkImage(Image.open(relative_to_assets("image_3.png")),size=(930,520))
    rectangle2 = ctk.CTkLabel(RegisterFrame, image=rectangle2_img,text="")
    rectangle2.place(x=210, y=100)

    car_img = ctk.CTkImage(Image.open(relative_to_assets("image_4.png")),size=(500,500))
    car_bg = ctk.CTkLabel(RegisterFrame, image=car_img,text="", bg_color="#FC4F3E", fg_color="#FC4F3E")
    car_bg.place(x=780, y=320)
    pywinstyles.set_opacity(car_bg,color="#FC4F3E")

    home_image = ctk.CTkImage(Image.open(relative_to_assets("image_5.png")),size=(30,30))
    home_button = ctk.CTkButton(master=RegisterFrame, text="  Home", image=home_image, width=120, fg_color=("#F86544","#FA5740"), bg_color="#FA5740", text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20),command=lambda:open_home(RegisterFrame,home_callback))
    home_button.place(x=30, y=20)
    pywinstyles.set_opacity(home_button,color="#FA5740")
    
    logo_img = ctk.CTkImage(Image.open(relative_to_assets("logo.png")),size=(90,45))
    logo_label = ctk.CTkLabel(master=RegisterFrame, text="", image=logo_img, fg_color="#FF865A", bg_color="#FF865A")
    logo_label.place(x=160, y=15)
    pywinstyles.set_opacity(logo_label,color="#FF865A")

    # Creating labels and entry fields
    name_label = ctk.CTkLabel(RegisterFrame, text="Name\t\t:", bg_color="#FFAB40", font=('Arial Bold', 16))
    name_label.place(x=250, y=200)
    pywinstyles.set_opacity(name_label,color="#FFAB40")
    name_entry = tk.Entry(RegisterFrame, font=('Lucida Console', 10))
    name_entry.place(x=410, y=200, width=270, height=30)

    email_label = ctk.CTkLabel(RegisterFrame, text="Email Address\t:", bg_color="#FFAB40", font=('Arial Bold', 16))
    email_label.place(x=250, y=250)
    pywinstyles.set_opacity(email_label,color="#FFAB40")
    email_entry = tk.Entry(RegisterFrame, font=('Lucida Console', 10))
    email_entry.place(x=410, y=250, width=270, height=30)

    dobInfo = ctk.CTkLabel(RegisterFrame,text="Note: Enter Date of Birth as  DD-MM-YYYY", font=('Lucida Console', 10), bg_color="#FFAB40")
    dobInfo.place(x=410, y=325)
    pywinstyles.set_opacity(dobInfo,color="#FFAB40")

    dob_label = ctk.CTkLabel(RegisterFrame, text="Date Of Birth\t:", bg_color="#FFAB40", font=('Arial Bold', 16))
    dob_label.place(x=250, y=300)
    pywinstyles.set_opacity(dob_label,color="#FFAB40")
    dob_day_entry = tk.Entry(RegisterFrame, width=3, font=('Lucida Console', 10))
    dob_day_entry.place(x=410, y=300, height=30)
    dob_month_entry = tk.Entry(RegisterFrame, width=3, font=('Lucida Console', 10))
    dob_month_entry.place(x=460, y=300, height=30)
    dob_year_entry = tk.Entry(RegisterFrame, width=5, font=('Lucida Console', 10))
    dob_year_entry.place(x=510, y=300, height=30)

    contact_label = ctk.CTkLabel(RegisterFrame, text="Contact No\t:", bg_color="#FFAB40", font=('Arial Bold', 16))
    contact_label.place(x=250, y=350)
    pywinstyles.set_opacity(contact_label,color="#FFAB40")
    contact_entry = tk.Entry(RegisterFrame, font=('Lucida Console', 10))
    contact_entry.place(x=410, y=350, width=270, height=30)

    passW_label = ctk.CTkLabel(RegisterFrame, text="Password\t:", bg_color="#FFAB40", font=('Arial Bold', 16))
    passW_label.place(x=250, y=400)
    pywinstyles.set_opacity(passW_label,color="#FFAB40")
    passW_entry = tk.Entry(RegisterFrame, font=('Lucida Console', 10), show="*")
    passW_entry.place(x=410, y=400, width=270, height=30)

    cpassW_label = ctk.CTkLabel(RegisterFrame, text="Confirm Password\t:", bg_color="#FFAB40", font=('Arial Bold', 16))
    cpassW_label.place(x=250,y=450)
    pywinstyles.set_opacity(cpassW_label,color="#FFAB40")
    cpassW_entry = tk.Entry(RegisterFrame, font=('Lucida Console', 10), show="*")
    cpassW_entry.place(x=410, y=450, width=270, height=30)

    passInfo = ctk.CTkLabel(RegisterFrame,text="Note: Passwords are required to have at least 8 letters.", font=('Lucida Console', 10), bg_color="#FFAB40")
    passInfo.place(x=410, y=325)
    pywinstyles.set_opacity(dobInfo,color="#FFAB40")

    # Sign-up button
    sign_up_button = ctk.CTkButton(RegisterFrame, text="Sign Up", font=('Arial Bold', 16), width=270, height=30, 
                                   bg_color="#FFA843", fg_color=("#FC503E","white"), corner_radius=10, 
                                   command=lambda:sign_up_get(login_callback,name_entry.get(),email_entry.get(),dob_day_entry.get(),dob_month_entry.get(),dob_year_entry.get(),contact_entry.get(),passW_entry.get(),cpassW_entry.get()))
    sign_up_button.place(x=410, y=500)
    pywinstyles.set_opacity(sign_up_button,color="#FFA843")

    # Log in button
    login_label = ctk.CTkLabel(RegisterFrame, text="Already registered?", bg_color="#FFAB40", font=('Arial Bold', 11))
    login_label.place(x=490,y=540)
    pywinstyles.set_opacity(login_label,color="#FFAB40")
    login_img = ctk.CTkImage(Image.open(relative_to_assets("button_2.png")),size=(65,27))
    login_button = ctk.CTkButton(RegisterFrame, text="", image=login_img, font=('Arial Bold', 11), bg_color="#FF7E52", fg_color=("#FF7E52","white"), width=65,height=27,
                                    command=lambda:open_login(RegisterFrame,login_callback))
    login_button.place(x=605, y=535)
    pywinstyles.set_opacity(login_button,color="#FF7E52")

    # Title and subtitle on the right
    title_label = ctk.CTkLabel(RegisterFrame, text="Register Now!", font=('Arial Bold', 32), bg_color="#FFAB40")
    title_label.place(x=760, y=280)
    pywinstyles.set_opacity(title_label,color="#FFAB40")
    subtitle_label = ctk.CTkLabel(RegisterFrame, text="Few more steps to make your trip better!", font=('Arial', 20), bg_color="#FFAB40")
    subtitle_label.place(x=710, y=320)
    pywinstyles.set_opacity(subtitle_label,color="#FFAB40")
