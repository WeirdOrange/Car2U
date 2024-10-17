import customtkinter as ctk
import pywinstyles
import sqlite3
from Car2U_UserInfo import get_user_info
from tkinter import Toplevel, messagebox
from pathlib import Path
from PIL import Image

# Function to handle login button click
def open_login(current_window, login_callback):
    current_window.destroy()  # Close the signup window
    login_callback()

# Function to handle selection button click
def open_home(current_window, home_callback):
    current_window.destroy()  # Close the signup window
    home_callback()

# Function to handle selection button click
def open_listing(current_window, list_callback):
    current_window.destroy()  # Close the signup window
    list_callback()

# Function to handle profile button click
def open_profile():
    messagebox.showinfo("You are on the profile page")

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Profile")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def Database(): #creating connection to database and creating table
    global conn, cursor
    conn = sqlite3.connect("car2u.db")
    # Enable access to columns by name
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

def fetch_user_data():
    global result
    Database()
    userInfo = get_user_info()
    print(userInfo)
    query = f"""SELECT *,(date()-dob) AS age FROM UserDetails where email = '{userInfo}'"""
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    accInfo()

def accInfo():
    for row in result:
        name = row[1]
        email = row[2]
        gender = row[4]
        dob = row[5]
        age = row[10]
        if gender == 0:
            gender = "Male"
        else:
            gender = "Female"
        contact = row[6]
        nationality = row[7]

        info_labels = [(email, 10), (age, 50), (contact, 90), (gender, 130), (nationality, 170)]
        for text, y_pos in info_labels:
            label = ctk.CTkLabel(info_frame, text=text, font=("Skranji", 20), text_color="#000000")
            label.place(x=175, y=y_pos)

        user_name_label = ctk.CTkLabel(profileFrame, text=name, font=("Cooper Black", 40), text_color="#000000")
        user_name_label.place(x=346, y=90)
        
        dob_label = ctk.CTkLabel(info_frame, text="Birth Date: ", font=("Skranji", 20), text_color="#000000")
        dob_label.place(x=400, y=50)
        userDOB = ctk.CTkLabel(info_frame, text=dob, font=("Skranji", 20), text_color="#000000")
        userDOB.place(x=500, y=50)

def editInfo():
    for widget in info_frame.winfo_children():
        if isinstance(widget, ctk.CTkFrame):
            widget.destroy()

    info_labels = [("Email:", 10), ("Date Of Birth:", 50), ("Phone Number:", 90), ("Gender:", 130), ("Nationality:", 170)]
    for text, y_pos in info_labels:
        label = ctk.CTkLabel(info_frame, text=text, font=("Skranji", 20), text_color="#000000")
        label.place(x=15, y=y_pos)
    # Entries 
    emailEntry = ctk.CTkEntry(info_frame, width=438, height=28, font=("Skranji", 20), text_color="#000000")
    emailEntry.place(x=175, y=10)

    dobEntry = ctk.CTkEntry(info_frame, width=438, height=28, font=("Skranji", 20), text_color="#000000")
    dobEntry.place(x=175, y=50)

    contactEntry = ctk.CTkEntry(info_frame, width=438, height=28, font=("Skranji", 20), text_color="#000000")
    contactEntry.place(x=175, y=90)
        
    genderEntry = ctk.CTkEntry(info_frame, width=438, height=28, font=("Skranji", 20), text_color="#000000")
    genderEntry.place(x=175, y=130)

    nationalityEntry = ctk.CTkEntry(info_frame, width=438, height=28, font=("Skranji", 20), text_color="#000000")
    nationalityEntry.place(x=175, y=170)
    
    edit_info = ctk.CTkButton(info_frame, text="Done", width=80, corner_radius=50, fg_color="#F95F43", bg_color="#FFFFFF",
                              font=("Tw Cen MT Condensed Extra Bold", 16), command=lambda: print("Edit Personal Info clicked"))
    edit_info.place(x=625, y=218)

def accManage(current_window, login_callback):
    droptabFrame = ctk.CTkFrame(profileFrame,width=190,height=240, bg_color="#E6F6FF",fg_color="#E6F6FF")
    droptabFrame.place(x=1090, y=60)

    myAcc = ctk.CTkButton(master=droptabFrame, text="My Account", text_color="#000000", fg_color=("#E6F6FF","#D9D9D9"), 
                                  bg_color="#E6F6FF", font=("SegoeUI Bold", 20), command=lambda:open_profile())
    myAcc.place(x=30,y=23)

    history = ctk.CTkButton(master=droptabFrame, text="History", text_color="#000000", fg_color=("#E6F6FF","#D9D9D9"), 
                                  bg_color="#E6F6FF", font=("SegoeUI Bold", 20))
    history.place(x=30,y=80)

    setting = ctk.CTkButton(master=droptabFrame, text="Setting", text_color="#000000", fg_color=("#E6F6FF","#D9D9D9"), 
                                  bg_color="#E6F6FF", font=("SegoeUI Bold", 20))
    setting.place(x=30,y=137)

    logout = ctk.CTkButton(master=droptabFrame, text="Log Out", text_color="#000000", fg_color=("#E6F6FF","#D9D9D9"), 
                                  bg_color="#E6F6FF", font=("SegoeUI Bold", 20), command=lambda:open_login(current_window, login_callback))
    logout.place(x=30,y=224)

def profile(login_callback,home_callback,list_callback):
    # Create the main application window
    global profileFrame
    profileFrame = Toplevel()
    profileFrame.title("Profile Page")
    profileFrame.geometry("1280x720")
    profileFrame.resizable(False, False)

    # Background
    bg_img = ctk.CTkImage(Image.open(relative_to_assets("image_1.png")),size=(1280,720))
    bg_label = ctk.CTkLabel(profileFrame, image=bg_img, text="", width=1280, height=60)
    bg_label.place(x=0, y=0)

    # Navigation Bar
    header = ctk.CTkFrame(profileFrame, width=1280, height=60, fg_color="#FFFFFF")
    header.place(x=0, y=0)

    navbg_img = ctk.CTkImage(Image.open(relative_to_assets("nav.png")),size=(1280,60))
    navbg_label = ctk.CTkLabel(header, image=navbg_img, text="", width=1280, height=60)
    navbg_label.place(x=0, y=0)

    # Relocating buttons
    home_button = ctk.CTkButton(master=profileFrame, text="Home", width=120, fg_color=("#F95C41","#FA5740"), bg_color="#FA5740", 
                                text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), 
                                command=lambda: open_home(profileFrame,home_callback))
    home_button.place(x=647, y=14)
    pywinstyles.set_opacity(home_button,color="#FA5740")

    selections_button = ctk.CTkButton(master=profileFrame, text="Selections", width=120, fg_color=("#FA5740","#FB543F"), bg_color="#FB543F", 
                                      text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), 
                                      command=lambda: open_listing(profileFrame,list_callback))
    selections_button.place(x=783, y=14)
    pywinstyles.set_opacity(selections_button,color="#FB543F")

    contact_us_button = ctk.CTkButton(master=profileFrame, text="Contact Us", width=120, fg_color=("#FB543F","#FC503E"), bg_color="#FC503E", 
                                      text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), 
                                      command=lambda: print("Contact Us clicked"))
    contact_us_button.place(x=930, y=14)
    pywinstyles.set_opacity(contact_us_button,color="#FC503E")

    about_us_button = ctk.CTkButton(master=profileFrame, text="About Us", width=120, fg_color=("#FC503E","#FC4D3D"), bg_color="#FC4D3D", 
                                    text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), 
                                    command=lambda: print("About Us clicked"))
    about_us_button.place(x=1075, y=14)
    pywinstyles.set_opacity(about_us_button,color="#FC4D3D")

    logo_img = ctk.CTkImage(Image.open(relative_to_assets("logo.png")),size=(75,40))
    logo_label = ctk.CTkLabel(profileFrame, image=logo_img, text="", bg_color="#F47749", width=95, height=50)
    logo_label.place(x=5, y=5)
    pywinstyles.set_opacity(logo_label,color="#F47749")
    
    pfp_img = ctk.CTkImage(Image.open(relative_to_assets("image_6.png")),size=(40,40))
    pfp_label = ctk.CTkButton(profileFrame, image=pfp_img, text="", bg_color="#F47749", fg_color="#F47749",
                              width=40, height=40, command=lambda:accManage(profileFrame,login_callback))
    pfp_label.place(x=1180, y=5)
    pywinstyles.set_opacity(pfp_label,color="#F47749")

    # User Info section
    # Placeholder for user image
    user_image = ctk.CTkLabel(profileFrame, text="Image Placeholder", width=270, height=230, fg_color="#D9D9D9")
    user_image.place(x=40, y=153)

    # Personal information section
    global info_frame
    info_frame = ctk.CTkFrame(profileFrame, width=757, height=260, fg_color="#FFFFFF", border_width=2, border_color="grey")
    info_frame.place(x=345, y=152)

    info_labels = [("Email:", 10), ("Age:", 50), ("Phone Number:", 90), ("Gender:", 130), ("Nationality:", 170)]
    for text, y_pos in info_labels:
        label = ctk.CTkLabel(info_frame, text=text, font=("Skranji", 20), text_color="#000000")
        label.place(x=15, y=y_pos)

    fetch_user_data()
    
    edit_info = ctk.CTkButton(info_frame, text="Edit", width=80, corner_radius=50, fg_color="#F95F43", bg_color="#FFFFFF",
                              font=("Tw Cen MT Condensed Extra Bold", 16), command=lambda: editInfo())
    edit_info.place(x=625, y=218)

    # "Top Places to Visit" Section
    places_label = ctk.CTkLabel(profileFrame, text="Top Places to Visit", font=("Skranji", 36), text_color="#000000")
    places_label.place(x=70, y=427)
    pywinstyles.set_opacity(places_label,color="#FFFFFF")

    # Top places background
    place_bg = ctk.CTkFrame(profileFrame, width=1170, height=210, border_width=2,fg_color="white")
    place_bg.place(x=55,y=470)

    # Placeholders for destination images
    place_1_img = ctk.CTkImage(Image.open(relative_to_assets("image_2.png")),size=(260,190))
    place_1_photo = ctk.CTkLabel(profileFrame,image=place_1_img,text="")
    place_1_photo.place(x=65, y=480)
    place_1 = ctk.CTkLabel(profileFrame, text="Penang", fg_color="#FFFFFF")
    place_1.place(x=355, y=510)

    place_2_img = ctk.CTkImage(Image.open(relative_to_assets("image_4.png")),size=(260,190))
    place_2_photo = ctk.CTkLabel(profileFrame,image=place_2_img,text="")
    place_2_photo.place(x=530, y=480)
    place_2 = ctk.CTkLabel(profileFrame, text="Kuala\n\tLumpur", fg_color="#FFFFFF")
    place_2.place(x=810, y=520)

    place_3_img = ctk.CTkImage(Image.open(relative_to_assets("image_5.png")),size=(228,190))
    place_3_photo = ctk.CTkLabel(profileFrame,image=place_3_img,text="")
    place_3_photo.place(x=990, y=480)

    # "Know more" links
    know_more_1 = ctk.CTkLabel(profileFrame, text="Know more...", font=("Sriracha Regular", 15), text_color="#00A3FF")
    know_more_1.bind('<Enter>', lambda event, label=know_more_1: label.configure(font=('SegoeUI Bold', 15, 'underline')))
    know_more_1.bind('<Leave>', lambda event, label=know_more_1: label.configure(font=('SegoeUI Bold', 15)))
    know_more_1.place(x=431, y=643)

    know_more_2 = ctk.CTkLabel(profileFrame, text="Know more...", font=("Sriracha Regular", 15), text_color="#00A3FF")
    know_more_2.bind('<Enter>', lambda event, label=know_more_2: label.configure(font=('SegoeUI Bold', 15, 'underline')))
    know_more_2.bind('<Leave>', lambda event, label=know_more_2: label.configure(font=('SegoeUI Bold', 15)))
    know_more_2.place(x=894, y=643)

    # Footer buttons (optional)
    nextbttn_img = ctk.CTkImage(Image.open(relative_to_assets("button_1.png")),size=(30,30))
    nextPromo_button = ctk.CTkButton(profileFrame, text="", image=nextbttn_img, width=10, height=10, corner_radius=100, fg_color="#4B5B6C", bg_color="#4B5B6C", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: print("About Us clicked"))
    nextPromo_button.place(x=1173, y=563)
    pywinstyles.set_opacity(nextPromo_button,color="#4B5B6C")
