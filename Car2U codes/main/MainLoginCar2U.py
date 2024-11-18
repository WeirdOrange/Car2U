import sqlite3
import tkinter as tk
import customtkinter as ctk
import pywinstyles
import hashlib
import easygui
import random, string
import smtplib
import ssl
from MainCar2U_UserInfo import set_user_info
from pathlib import Path
from tkinter import messagebox,Toplevel
from PIL import ImageTk, Image
from email.message import EmailMessage

# Set up the asset path 
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Main-Login")

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

def open_return(current_window, returnLogin):
    current_window.destroy()  # Close the login window
    returnLogin()

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

def forgorPssw(loginFrame,returnLogin):
    global otp
    name = ""
    for x in range(5):
        otp = otp + str(random.choice(string.ascii_letters))
    # Validate email    
    while True:
        askEmail = easygui.enterbox("Enter Email: ","Finding Email...")
        if askEmail is not None and askEmail != "":
            print(askEmail)
            # Find Email within database
            Database()
            cursor.execute("SELECT name FROM UserDetails WHERE `email` = ?",(str(askEmail),))
            result = cursor.fetchall()
            conn.close()

            if result is None:
                # Check if it the user is a Rental Agency
                Database()
                cursor.execute("SELECT agencyName FROM RentalAgency WHERE `agencyEmail` = ?",(str(askEmail),))
                result = cursor.fetchall()
                conn.close()

                if result is None:
                    messagebox.showerror("Error","Email has not been registered!") # Email not found
                    break
                else:
                    pass
            for row in result:
                name = row[0]
                print(name)

            else:
                for row in result:
                    name = row[0]
                    print(name)
                # Sending OTP to user
                subject = 'Forgot Password Request'
                body = f"""Hey, {name}\nWe heard that you lost your Car2U password. If this was not you, please ignore this email.
                            \nIf this was you,\n\nYour OTP is {otp}\n\nNeed Help? Contact us via Car2U support team."""
                emailNotif(askEmail,subject,body)
                conn.close()
                userotp = easygui.enterbox("Enter OTP (Press cancel to request for another OTP): ","Check Your Email for OTP")
                
                if userotp == otp: # If OTP is enter correctly

                    msg = "Enter your new password (A minimum of 8 letters are required)"
                    title = "Changing password..."
                    fieldNames = ["New Password","Confirm New Password"]

                    while True:
                        passw = easygui.multenterbox(msg, title, fieldNames)   
                        if not passw:
                            break
                        if len(str(passw[0])) < 8:
                            easygui.msgbox("Passwords are required to have at least 8 letters. Please try again.")

                        elif passw[0].strip() == "" or passw[0] != passw[1]:
                            easygui.msgbox("Passwords do not match or are empty. Please try again.")
                        else:
                            break
                    
                    if passw:
                        print("Reply was:", passw)

                        newpassw = hashlib.sha256(str(passw[0]).encode()).hexdigest()
                        
                        Database()
                        cursor.execute("SELECT name FROM UserDetails WHERE email = ?",(str(askEmail),))
                        result = cursor.fetchall()
                        conn.close()

                        if result is None:
                            try:
                                Database()
                                cursor.execute("UPDATE RentalAgency SET agenyPassword = ? WHERE agencyEmail = ?", (str(newpassw),str(askEmail)))
                                conn.commit()
                                print("Admin Change done:", passw)

                                messagebox.showinfo("Password Change Successful", "You have changed your password, you can log into Car2U once more!")
                                open_return(loginFrame, returnLogin)
                                return False
                            
                            except sqlite3.Error as e:
                                messagebox.showerror("Error", "Error occurred during registration: {}".format(e))
                                continue
                            finally:
                                conn.close()
                                return False
                        else:
                            for row in result:
                                print(row)
                            try:
                                Database()
                                cursor.execute("UPDATE UserDetails SET password = ? WHERE email = ?", (str(newpassw),str(askEmail)))
                                conn.commit()
                                print("User Change done:", passw)

                                messagebox.showinfo("Password Change Successful", "You have changed your password, you can log into Car2U once more!")
                                open_return(loginFrame, returnLogin)
                                return False
                            except sqlite3.Error as e:
                                messagebox.showerror("Error", "Error occurred during registration: {}".format(e))
                                continue
                            finally:
                                conn.close()
                                return False

                elif userotp is None:  # If the user clicks "Cancel" (user_input will be None)
                    # Display the buttonbox with options
                    choice = easygui.buttonbox("You clicked Cancel. What would you like to do next?", "Options", 
                                            choices=["Back", "Resend OTP", "Cancel"])
                    
                    if choice == "Back":
                        # Return back to the enterbox (loop continues)
                        continue  # This goes back to the beginning of the loop
                    
                    elif choice == "Resend OTP":
                        for x in range(5):
                            otp = otp + str(random.choice(string.ascii_letters))
                        
                        easygui.msgbox("Resending OTP.", "Do check your email for an OTP. (Delay might happen)")

                        # Sending OTP to user
                        subject = 'Car2U: OTP to verify your identity'
                        body = f"""Hi {name},\nYour OTP is : {otp}\nNever Share this code to others. If this is not your actions, please contact our customer service.
                        \n\nCar2U contact: 016-407 5284 or email via this account"""
                        emailNotif(askEmail,subject,body)
                        continue
                    
                    elif choice == "Cancel":
                        easygui.msgbox(f"Registration Terminated", "Press the 'Sign Up' button again to register")
                    break  # Exit the loop if the user doesn't want to continue
                else:
                    easygui.msgbox(f"Wrong OTP Value", "The entered OTP is incorrect. Check if you had entered a space?")
                    continue
        elif askEmail is None and askEmail == "":
            messagebox.showerror("Error","Email was not entered!") # Email not found
            continue
        else:
            print("Enterbox closed")
            break
        
def logingui(signup_callback,home_callback,adminHome_callback,returnLogin):
    # Create the main application window
    global loginFrame,email_entry,password_entry
    loginFrame = Toplevel()
    loginFrame.title("Login")
    loginFrame.geometry("1280x720")
    loginFrame.resizable(False, False)

    # For forgot password verification
    global otp
    otp = ""

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
    signup_img = ctk.CTkImage(Image.open(relative_to_assets("button_2.png")),size=(65,27))
    signup_label = ctk.CTkLabel(loginFrame, text="New User?", bg_color="#FFA843", font=("Arial", 10, "bold"))
    signup_label.place(x=900,y=422)
    pywinstyles.set_opacity(signup_label,color="#FFA843")
    signup_button = ctk.CTkButton(loginFrame, text="", image=signup_img, font=("Arial", 10, "bold"), width=80,
                                  bg_color="#FFA843", fg_color=("#FFA843","white"),command=lambda:open_signup(loginFrame,signup_callback))
    signup_button.place(x=968, y=420)
    pywinstyles.set_opacity(signup_button,color="#FFA843")

    # Forgot Password
    forgot = ctk.CTkLabel(loginFrame,text="Forgot Password", width=105, height=15, font=("Arial", 11), text_color="#2F59C1", bg_color="#FFA843", fg_color="#FFA843")
    forgot.bind('<Enter>', lambda event, label=forgot: label.configure(font=('Arial Bold', 11, 'underline')))
    forgot.bind("<Button-1>", lambda event: forgorPssw(loginFrame,returnLogin))
    forgot.bind('<Leave>', lambda event, label=forgot: label.configure(font=('Arial Bold', 11)))
    forgot.place(x=710, y=422)
    pywinstyles.set_opacity(forgot,color="#FFA843")

    # Additional Title Texts
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
    
    password = hashlib.sha256(str(password).encode()).hexdigest()
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
