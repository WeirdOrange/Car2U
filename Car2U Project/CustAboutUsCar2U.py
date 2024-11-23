from pathlib import Path
from PIL import Image
from tkinter import Toplevel, messagebox
from tkcalendar import DateEntry
from MainCar2U_UserInfo import get_user_info,set_user_info
import tkinter as tk
import customtkinter as ctk 
import pywinstyles

# Set up the asset path
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Cust-AboutUs")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Function to handle login button click
def open_login(current_window, login_callback):
    current_window.destroy()  # Close the signup window
    userInfo = ""
    set_user_info(userInfo)
    login_callback()

# Function to handle home button click
def open_home(current_window, home_callback):
    current_window.destroy()  # Close the login window
    home_callback()

# Function to handle selection button click
def open_listing(current_window, list_callback):
    current_window.destroy()  # Close the signup window
    list_callback()

# Function to handle profile button click
def open_profile(current_window, profile_callback):
    current_window.destroy()  # Close the signup window
    profile_callback()

# Function to handle upgrade as renter button click
def open_upRent(current_window, uprent_callback):
    current_window.destroy()  # Close the login window
    uprent_callback()

# Function to handle profile button click
def open_about():
    messagebox.showinfo("You are on the About Us page")

# Function to handle profile button click
def open_review(current_window, review_callback):
    current_window.destroy()  # Close the signup window
    review_callback()

# Function to handle chats button click
def open_chat(current_window, chat_callback):
    current_window.destroy()  # Close the window
    chat_callback()

def accManage(current_window, login_callback,profile_callback,review_callback):
    global pfpState, droptabFrame

    if pfpState == 1:
        droptabFrame = ctk.CTkFrame(current_window,width=190,height=240, bg_color="#E6F6FF",fg_color="#E6F6FF")
        droptabFrame.place(x=1090, y=60)

        if userInfo == "":
            droptabFrame.configure(height=57)
            logoin = ctk.CTkButton(master=droptabFrame, text="Log In", text_color="#000000", fg_color=("#E6F6FF","#D9D9D9"), 
                                    bg_color="#E6F6FF", font=("SegoeUI Bold", 20), command=lambda:open_login(current_window, login_callback))
            logoin.place(x=30,y=13)

        else:
            myAcc = ctk.CTkButton(master=droptabFrame, text="My Account", text_color="#000000", fg_color=("#E6F6FF","#D9D9D9"), 
                                        bg_color="#E6F6FF", font=("SegoeUI Bold", 20), command=lambda:open_profile(current_window, profile_callback))
            myAcc.place(x=30,y=23)

            history = ctk.CTkButton(master=droptabFrame, text="My Bookings", text_color="#000000", fg_color=("#E6F6FF","#D9D9D9"), 
                                        bg_color="#E6F6FF", font=("SegoeUI Bold", 20), command=lambda:open_review(current_window, review_callback))
            history.place(x=30,y=80)

            setting = ctk.CTkButton(master=droptabFrame, text="Setting", text_color="#000000", fg_color=("#E6F6FF","#D9D9D9"), 
                                        bg_color="#E6F6FF", font=("SegoeUI Bold", 20))
            setting.place(x=30,y=137)

            logout = ctk.CTkButton(master=droptabFrame, text="Log Out", text_color="#000000", fg_color=("#E6F6FF","#D9D9D9"), 
                                        bg_color="#E6F6FF", font=("SegoeUI Bold", 20), command=lambda:open_login(current_window, login_callback))
            logout.place(x=30,y=195)
        pfpState = 0
    else:
        droptabFrame.destroy()
        pfpState = 1

def aboutUspage(login_callback,uprent_callback,home_callback,list_callback,profile_callback,review_callback,chat_callback):
    # Create the main application window
    global aboutFrame
    aboutFrame = Toplevel()
    aboutFrame.title("Login")
    aboutFrame.geometry("1280x720")
    aboutFrame.resizable(False, False)
    aboutFrame.config(bg="white")
    
    global pfpState
    pfpState = 1

    # Navigation Tab
    nav_img = ctk.CTkImage(Image.open(relative_to_assets("image_2.png")),size=(1280,60))
    nav_label = ctk.CTkLabel(aboutFrame, image=nav_img, text="", width=1280, height=60)
    nav_label.place(x=0, y=0)

    logo_img = ctk.CTkImage(Image.open(relative_to_assets("logo.png")),size=(75,40))
    logo_label = ctk.CTkLabel(aboutFrame, image=logo_img, text="", bg_color="#F47749", width=95, height=50)
    logo_label.place(x=5, y=5)
    pywinstyles.set_opacity(logo_label,color="#F47749")
    
    pfp_img = ctk.CTkImage(Image.open(relative_to_assets("image_1.png")),size=(40,40))
    pfp_label = ctk.CTkButton(aboutFrame, image=pfp_img, text="", bg_color="#F47749", fg_color="#F47749",
                              width=40, height=40, command=lambda:accManage(aboutFrame,login_callback,profile_callback,review_callback))
    pfp_label.place(x=1203, y=5)
    pywinstyles.set_opacity(pfp_label,color="#F47749")

    # Relocate buttons
    home_button = ctk.CTkButton(master=aboutFrame, text="Home", width=120, fg_color=("#F95C41","#FA5740"), bg_color="#FA5740", 
                                text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_home(aboutFrame,home_callback))
    home_button.place(x=667, y=14)
    pywinstyles.set_opacity(home_button,color="#FA5740")

    selections_button = ctk.CTkButton(master=aboutFrame, text="Selections", width=120, fg_color=("#FA5740","#FB543F"), bg_color="#FB543F", 
                                      text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda:open_listing(aboutFrame,list_callback))
    selections_button.place(x=783, y=14)
    pywinstyles.set_opacity(selections_button,color="#FB543F")

    contact_us_button = ctk.CTkButton(master=aboutFrame, text="Contact Us", width=120, fg_color=("#FB543F","#FC503E"), bg_color="#FC503E", 
                                      text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_chat(aboutFrame, chat_callback))
    contact_us_button.place(x=930, y=14)
    pywinstyles.set_opacity(contact_us_button,color="#FC503E")

    about_us_button = ctk.CTkButton(master=aboutFrame, text="About Us", width=120, fg_color=("#FC503E","#FC4D3D"), bg_color="#FC4D3D", 
                                    text_color="#FFF6F6", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_about())
    about_us_button.place(x=1075, y=14)
    pywinstyles.set_opacity(about_us_button,color="#FC4D3D")
    

    aboutUsbg = ctk.CTkImage(Image.open(relative_to_assets("image_3.png")),size=(935,582))
    aboutUsbgLabel = ctk.CTkLabel(aboutFrame, text="", image=aboutUsbg, width=935, height=582)
    aboutUsbgLabel.place(x=345,y=60)

    biglogo_img = ctk.CTkImage(Image.open(relative_to_assets("logo.png")),size=(346,182))
    biglogo_label = ctk.CTkLabel(aboutFrame, image=biglogo_img, text="", bg_color="#FFFFFF", fg_color="#FFFFFF", width=346, height=182)
    biglogo_label.place(x=60, y=141)
    pywinstyles.set_opacity(logo_label,color="#FFFFFF")
    
    h1 = "Embracing The Art Of Simplicity In A Busy City"
    h2 = "Car2U is a platform that provides convenience throughout the process of booking and renting vehicles, \nincluding enquiries for the renters by the users."
    h3 = "Car2U showcases details regarding the cars available for rent\nand provides an easy access for our users to review their\nbookings simply using a few clicks."
    h1Label = ctk.CTkLabel(aboutFrame, text=h1, width=827, height=49, font=("Arial Black", 32), text_color="#000000", bg_color="#FFFFFF", fg_color="#FFFFFF")
    h1Label.place(x=435,y=120)
    pywinstyles.set_opacity(h1Label,color="#FFFFFF")

    h2Label = ctk.CTkLabel(aboutFrame, text=h2, width=827, height=49, font=("Tw Cen MT Condensed Extra Bold", 20), anchor="w", text_color="#000000", bg_color="#FFFFFF", fg_color="#FFFFFF")
    h2Label.place(x=450,y=190)
    pywinstyles.set_opacity(h2Label,color="#FFFFFF")
    
    titlebgLabel = ctk.CTkFrame(aboutFrame, width=500, height=120, bg_color="#FFFFFF", fg_color="#FFFFFF", corner_radius=100)
    titlebgLabel.place(x=40,y=360)

    h3Label = ctk.CTkLabel(aboutFrame, text=h3, width=606, height=80, font=("Tw Cen MT Condensed Extra Bold", 20), anchor="w", text_color="#000000", bg_color="#FFFFFF", fg_color="#FFFFFF")
    h3Label.place(x=60,y=360)
    pywinstyles.set_opacity(h3Label,color="#FFFFFF")


    # Footer Section
    footer_frame = ctk.CTkLabel(aboutFrame,text="", fg_color="#2A333D", width=1280, height=180)
    footer_frame.place(x=0,y=550)

    # Account section
    account_label = ctk.CTkLabel(master=aboutFrame, text="Account", fg_color="#2A333D", text_color="#4B5B6D", 
                                 font=("Tw Cen MT Condensed Extra Bold", 32))
    account_label.place(x=140,y=587)
    pywinstyles.set_opacity(account_label,color="#2A333D")

    myprofile_label = ctk.CTkButton(master=aboutFrame, text="My Profile", bg_color="#2A333D", fg_color="#2A333D", text_color="#9EA3A9", 
                                   font=("Tw Cen MT Condensed Extra Bold", 20),
                                   command= lambda:open_profile(aboutFrame,profile_callback))
    myprofile_label.place(x=290,y=577)
    pywinstyles.set_opacity(myprofile_label,color="#2A333D")
    aboutus_label = ctk.CTkButton(master=aboutFrame, text="About Car2U", bg_color="#2A333D", fg_color="#2A333D", text_color="#9EA3A9", 
                                 font=("Tw Cen MT Condensed Extra Bold", 20),
                                 command=lambda:open_about())
    aboutus_label.place(x=290,y=620)
    pywinstyles.set_opacity(aboutus_label,color="#2A333D")
    upRenter_label = ctk.CTkButton(master=aboutFrame, text="Upgrade to Rental Agent", bg_color="#2A333D", fg_color="#2A333D", text_color="#9EA3A9", 
                                  font=("Tw Cen MT Condensed Extra Bold", 20),
                                 command=lambda:open_upRent(aboutFrame, uprent_callback))
    upRenter_label.place(x=430,y=577)
    pywinstyles.set_opacity(upRenter_label,color="#2A333D")
    upMember_label = ctk.CTkButton(master=aboutFrame, text="Upgrade to Member", bg_color="#2A333D", fg_color="#2A333D", text_color="#9EA3A9", 
                                  font=("Tw Cen MT Condensed Extra Bold", 20),
                                 command=lambda:print("connecting to upgrade Member"))
    upMember_label.place(x=430,y=620)
    pywinstyles.set_opacity(upMember_label,color="#2A333D")

    # Support section
    support_label = ctk.CTkLabel(master=aboutFrame, text="Support", fg_color="#2A333D", text_color="#4B5B6D", 
                                 font=("Tw Cen MT Condensed Extra Bold", 32))
    support_label.place(x=725, y=587)
    pywinstyles.set_opacity(support_label,color="#2A333D")

    guide_label = ctk.CTkButton(master=aboutFrame, text="Car2U Guide", bg_color="#2A333D", fg_color="#2A333D", text_color="#9EA3A9", 
                               font=("Tw Cen MT Condensed Extra Bold", 24),
                                 command=lambda:bookingManual)
    guide_label.place(x=880,y=577)
    pywinstyles.set_opacity(guide_label,color="#2A333D")
    findus_label = ctk.CTkButton(master=aboutFrame, text="Find Us", bg_color="#2A333D", fg_color="#2A333D", text_color="#9EA3A9", 
                                font=("Tw Cen MT Condensed Extra Bold", 24),
                                 command=lambda:print("connecting to about us"))
    findus_label.place(x=880,y=620)
    pywinstyles.set_opacity(findus_label,color="#2A333D")

    rights_label = ctk.CTkLabel(master=aboutFrame, text="@All Rights Reserved", bg_color="#2A333D", fg_color="#2A333D", 
                                text_color="#FFFFFF", font=("Tw Cen MT Condensed Extra Bold", 16))
    rights_label.place(x=562, y=680)
    pywinstyles.set_opacity(rights_label,color="#2A333D")

    global userInfo
    userInfo = get_user_info()
    print(f"About Us : {userInfo}")

def bookingManual(event):
    global manual
    if manual == 1:
        global manualFrame
        manualFrame = ctk.CTkFrame(aboutFrame, width=200, height=240,fg_color="#FFFFFF", border_color="#000000", border_width=2)
        manualFrame.place(x=256,y=240)

        steps = ["Step 1","Step 2","Step 3","Step 4","Step 5"]
        for i,step in enumerate(steps):
            stepLabel = ctk.CTkLabel(manualFrame, text=step, fg_color="#FFFFFF", text_color="#000000", font=("Segeo UI",14))
            stepLabel.place(x=10,y=10+i*40)
            pywinstyles.set_opacity(stepLabel,color="#FFFFFF")
        
        definition = ["Choose a car","Fill in relative details","Send a booking request","Pay for booking after request\nis approved","Have a fun rental experience"]
        for i,define in enumerate(definition):
            defLabel = ctk.CTkLabel(manualFrame, text=define, fg_color="#FFFFFF", text_color="#000000", font=("Segeo UI",12))
            defLabel.place(x=25,y=32+i*40)
            pywinstyles.set_opacity(defLabel,color="#FFFFFF")
        manual = 0
    else:
        for widget in manualFrame.winfo_children():
            if isinstance(widget, (ctk.CTkFrame,ctk.CTkLabel)):
                widget.destroy()
        for widget in aboutFrame.winfo_children():
            if isinstance(manualFrame, (ctk.CTkFrame)):
                manualFrame.destroy()
        manual = 1