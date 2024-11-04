import customtkinter as ctk
import tkinter as tk
import pywinstyles
import sqlite3
import smtplib
import ssl
import easygui
import random, string
from Car2U_UserInfo import get_user_info
from datetime import date
from dateutil.parser import parse
from PIL import Image
from email.message import EmailMessage
from pathlib import Path
from tkinter import messagebox, Toplevel

# Set up the asset path (same as original)
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Upgrade-Renter")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Connecting to database
def Database():
    global conn, cursor
    conn = sqlite3.connect("car2u.db")
    cursor = conn.cursor()

# Function to handle sign-up button click
def sign_up_get(login_callback,name,email,location,contact,password,cpassword):
    global otp
    Database()

    # Validation
    if not name or not email or not location or not contact or not password or not cpassword:
        messagebox.showerror("Input Error", "All fields are required!")
    elif password != cpassword:
        messagebox.showerror("Input Error", "Password and Confirm Password do not match.")
    else:
        try:
            cursor.execute("SELECT * FROM RentalAgency WHERE agencyEmail = ?",(str(email),))
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
                        cursor.execute("INSERT INTO RentalAgency(agencyEmail,agencyName,agencyLocation,agencyContactNo,agencyPassword) VALUES (?,?,?,?,?)",
                                        (str(email),str(name),str(location),str(contact),str(password)))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo("Registration Successful", "You have successfully signed up!")
                        
                        # Notify user through email as well
                        subject = 'Registration Completed!'
                        body = f"""Someone has registered this email account in the Car2U application.
                            \nAgency Name: {name}\nAgency Email: {email}\nAgency Location: {location}\nContact No: {contact}
                            \nIf this is not you, please contact Car2U as soon as possible. 
                            \nPlease ignore this message if this was you.\n\nCar2U contact: 016-407 5284"""
                        emailNotif(email,subject,body)

                        Database()
                        cursor.execute("""DELETE FROM UserDetails WHERE email = ?""",(email))
                        conn.commit()
                        open_login(RenterFrame,login_callback)
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
                        break
                        
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

def info_checker():
    if userInfo != "":
        try:
            Database()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""SELECT name, email, contactNo FROM UserDetails WHERE userID = ?""",(userInfo,))
            conn.commit()
            result = cursor.fetchall()
            
            for row in result:
                name = row[0]
                email = row[1]
                contact = row[2]
            
            name_entry.insert(0,name)
            email_entry.insert(0,email)
            contact_entry.insert(0,contact)
        except sqlite3.Error as e:
            messagebox.showerror("Error", "Error occurred during registration: {}".format(e))
        finally:
            conn.close()

def upRenter(login_callback, home_callback):
    global RenterFrame
    RenterFrame = Toplevel()
    RenterFrame.title("Sign Up")
    RenterFrame.geometry("1280x720")
    RenterFrame.resizable(False, False)

    # For signup verification
    global otp
    otp = ""
    for x in range(5):
        otp = otp + str(random.choice(string.ascii_letters))
    print(otp)

    # Load and set background image
    bg_image = ctk.CTkImage(Image.open(relative_to_assets("image_1.png")),size=(1073,720))
    bg_label = ctk.CTkLabel(RenterFrame, image=bg_image,text="")
    bg_label.place(x=207, y=0)
    
    rectangle1_img = ctk.CTkImage(Image.open(relative_to_assets("Rectangle_1.png")),size=(527,720))
    rectangle1 = ctk.CTkLabel(RenterFrame, image=rectangle1_img,text="")
    rectangle1.place(x=0, y=0)

    rectangle2_img = ctk.CTkImage(Image.open(relative_to_assets("Rectangle_2.png")),size=(930,520))
    rectangle2 = ctk.CTkLabel(RenterFrame, image=rectangle2_img,text="")
    rectangle2.place(x=210, y=100)

    car_img = ctk.CTkImage(Image.open(relative_to_assets("car.png")),size=(500,500))
    car_bg = ctk.CTkLabel(RenterFrame, image=car_img,text="", bg_color="#FC4F3E", fg_color="#FC4F3E")
    car_bg.place(x=780, y=320)
    pywinstyles.set_opacity(car_bg,color="#FC4F3E")

    home_image = ctk.CTkImage(Image.open(relative_to_assets("image_5.png")),size=(30,30))
    home_button = ctk.CTkButton(master=RenterFrame, text="  Home", image=home_image, width=120, fg_color=("#067BC1","#5EC5FF"), bg_color="#FA5740", 
                                text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20),
                                command=lambda:open_home(RenterFrame,home_callback))
    home_button.place(x=30, y=20)
    pywinstyles.set_opacity(home_button,color="#5EC5FF")
    
    logo_img = ctk.CTkImage(Image.open(relative_to_assets("logo.png")),size=(90,45))
    logo_label = ctk.CTkLabel(master=RenterFrame, text="", image=logo_img, fg_color="#76CEFF", bg_color="#76CEFF")
    logo_label.place(x=160, y=15)
    pywinstyles.set_opacity(logo_label,color="#76CEFF")

    # Creating labels and entry fields
    name_label = ctk.CTkLabel(RenterFrame, text="Agency Name:", width=177, height=27, anchor="e", bg_color="#880FC1", text_color="#FFFFFF", font=('Tw Cen MT Condensed Extra Bold', 20))
    name_label.place(x=190, y=140)
    pywinstyles.set_opacity(name_label,color="#880FC1")
    global name_entry
    name_entry = tk.Entry(RenterFrame, font=('Lucida Console', 10))
    name_entry.place(x=380, y=140, width=270, height=30)

    email_label = ctk.CTkLabel(RenterFrame, text="Email Address:", width=177, height=27, anchor="e", bg_color="#7121C1", text_color="#FFFFFF", font=('Tw Cen MT Condensed Extra Bold', 20))
    email_label.place(x=190, y=205)
    pywinstyles.set_opacity(email_label,color="#7121C1")
    global email_entry
    email_entry = tk.Entry(RenterFrame, font=('Lucida Console', 10))
    email_entry.place(x=380, y=205, width=270, height=30)

    location_label = ctk.CTkLabel(RenterFrame, text="Location:", width=177, height=27, anchor="e", bg_color="#5E32C1", text_color="#FFFFFF", font=('Tw Cen MT Condensed Extra Bold', 20))
    location_label.place(x=190, y=270)
    pywinstyles.set_opacity(location_label,color="#5E32C1")
    location_entry = tk.Entry(RenterFrame, font=('Lucida Console', 10))
    location_entry.place(x=380, y=270, width=270, height=30)

    contact_label = ctk.CTkLabel(RenterFrame, text="Contact No:", width=177, height=27, anchor="e", bg_color="#503DC1", text_color="#FFFFFF", font=('Tw Cen MT Condensed Extra Bold', 20))
    contact_label.place(x=190, y=335)
    pywinstyles.set_opacity(contact_label,color="#503DC1")
    global contact_entry
    contact_entry = tk.Entry(RenterFrame, font=('Lucida Console', 10))
    contact_entry.place(x=380, y=335, width=270, height=30)

    passW_label = ctk.CTkLabel(RenterFrame, text="Password:", width=177, height=27, anchor="e", bg_color="#3C4EC1", text_color="#FFFFFF", font=('Tw Cen MT Condensed Extra Bold', 20))
    passW_label.place(x=190, y=400)
    pywinstyles.set_opacity(passW_label,color="#3C4EC1")
    passW_entry = tk.Entry(RenterFrame, font=('Lucida Console', 10), show="*")
    passW_entry.place(x=380, y=400, width=270, height=30)

    cpassW_label = ctk.CTkLabel(RenterFrame, text="Confirm Password:", width=177, height=27, anchor="e", bg_color="#2F59C1", text_color="#FFFFFF", font=('Tw Cen MT Condensed Extra Bold', 20))
    cpassW_label.place(x=190,y=465)
    pywinstyles.set_opacity(cpassW_label,color="#2F59C1")
    cpassW_entry = tk.Entry(RenterFrame, font=('Lucida Console', 10), show="*")
    cpassW_entry.place(x=380, y=465, width=270, height=30)

    # Sign-up button
    sign_up_button = ctk.CTkButton(RenterFrame, text="Sign Up", font=('Tw Cen MT Condensed Extra Bold', 20), width=400, height=40, 
                                   text_color="#000000",bg_color="#067BC1", fg_color="#7CF6BF", corner_radius=50, 
                                   command=lambda:sign_up_get(login_callback,name_entry.get(),email_entry.get(),location_entry.get(),contact_entry.get(),passW_entry.get(),cpassW_entry.get()))
    sign_up_button.place(x=250, y=515)
    pywinstyles.set_opacity(sign_up_button,color="#067BC1")

    # When user is logged in
    global userInfo
    userInfo = get_user_info()

    # Log in button
    if userInfo == "":
        login_label = ctk.CTkLabel(RenterFrame, text="Already Registered?", bg_color="#1C69C1", font=('Tw Cen MT Condensed Extra Bold', 14), text_color="#FFFFFF")
        login_label.place(x=465,y=565)
        pywinstyles.set_opacity(login_label,color="#1C69C1")
        login_img = ctk.CTkImage(Image.open(relative_to_assets("Rectangle_3.png")),size=(65,27))
        login_button = ctk.CTkButton(RenterFrame, text="", image=login_img, bg_color="#1C69C1", fg_color="#1C69C1", width=65, height=27,
                                    command=lambda:open_login(RenterFrame,login_callback))
        login_button.place(x=580, y=560)
        pywinstyles.set_opacity(login_button,color="#1C69C1")

    # Title and subtitle on the right
    title_label = ctk.CTkLabel(RenterFrame, text="Become A Renter!", font=('Bauhaus 93', 48), bg_color="#5E32C1")
    title_label.place(x=710, y=240)
    pywinstyles.set_opacity(title_label,color="#5E32C1")
    subtitle_label = ctk.CTkLabel(RenterFrame, text="Join Us On Your Journey\nOf Becoming A Renter!", text_color="#FFFFFF", font=('Tw Cen MT Condensed Extra Bold', 24), bg_color="#503DC1")
    subtitle_label.place(x=770, y=310)
    pywinstyles.set_opacity(subtitle_label,color="#503DC1")

    info_checker()