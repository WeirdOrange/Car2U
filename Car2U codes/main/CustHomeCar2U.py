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
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Cust-Home")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Function to handle login button click
def open_login(current_window, login_callback):
    current_window.destroy()  # Close the signup window
    userInfo = ""
    set_user_info(userInfo)
    login_callback()

# Function to handle profile button click
def open_home():
    messagebox.showinfo("You are on the Home page")

# Function to handle selection button click
def open_listing(current_window, list_callback):
    current_window.destroy()  # Close the signup window
    list_callback()

# Function to handle profile button click
def open_profile(current_window, profile_callback):
    current_window.destroy()  # Close the signup window
    profile_callback()

def open_upRent(current_window, uprent_callback):
    current_window.destroy()  # Close the login window
    uprent_callback()

# Function to handle about us button click
def open_aboutUs(current_window, about_callback):
    current_window.destroy()  # Close the signup window
    about_callback()
    
# Function to handle profile button click
def open_review(current_window, review_callback):
    current_window.destroy()  # Close the signup window
    review_callback()

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

def findcar(homeFrame,list_callback,location,pax):
    print(location,"  ",pax)
    if location != None:
        saveCarLocate(location)
    if pax != None:
        saveCarPax(pax)
    open_listing(homeFrame,list_callback)

def saveCarLocate(location):
    global chosen_Location
    for x in locations:
        if location == x:
            chosen_Location = str(location)
def getCarLocate():
    return chosen_Location

def saveCarPax(pax):
    global chosen_Pax
    chosen_Pax = str(pax)
def getCarPax():
    return chosen_Pax

def homepage(login_callback,uprent_callback,list_callback,profile_callback,about_callback,review_callback):
    # Create the main application window
    global homeFrame
    homeFrame = Toplevel()
    homeFrame.title("Login")
    homeFrame.geometry("1280x720")
    homeFrame.resizable(False, False)
    homeFrame.config(bg="white")

    global chosen_Location, chosen_Pax, pfpState
    chosen_Location = ""
    chosen_Pax = ""
    pfpState = 1

    searchbg_img = ctk.CTkImage(Image.open(relative_to_assets("image_1.png")),size=(1280,253))
    searchbg_label = ctk.CTkLabel(homeFrame, image=searchbg_img, text="", width=1280, height=253)
    searchbg_label.place(x=0, y=0)

    # Navigation Tab
    nav_img = ctk.CTkImage(Image.open(relative_to_assets("image_2.png")),size=(1280,60))
    nav_label = ctk.CTkLabel(homeFrame, image=nav_img, text="", width=1280, height=60)
    nav_label.place(x=0, y=0)

    logo_img = ctk.CTkImage(Image.open(relative_to_assets("image_3.png")),size=(75,40))
    logo_label = ctk.CTkLabel(homeFrame, image=logo_img, text="", bg_color="#F47749", width=95, height=50)
    logo_label.place(x=5, y=5)
    pywinstyles.set_opacity(logo_label,color="#F47749")
    
    pfp_img = ctk.CTkImage(Image.open(relative_to_assets("image_4.png")),size=(40,40))
    pfp_label = ctk.CTkButton(homeFrame, image=pfp_img, text="", bg_color="#F47749", fg_color="#F47749",
                              width=40, height=40, command=lambda:accManage(homeFrame,login_callback,profile_callback,review_callback))
    pfp_label.place(x=1180, y=5)
    pywinstyles.set_opacity(pfp_label,color="#F47749")

    # Relocate buttons
    home_button = ctk.CTkButton(master=homeFrame, text="Home", width=120, fg_color=("#F95C41","#FA5740"), bg_color="#FA5740", 
                                text_color="#FFF6F6", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_home())
    home_button.place(x=627, y=14)
    pywinstyles.set_opacity(home_button,color="#FA5740")

    selections_button = ctk.CTkButton(master=homeFrame, text="Selections", width=120, fg_color=("#FA5740","#FB543F"), bg_color="#FB543F", 
                                      text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda:open_listing(homeFrame,list_callback))
    selections_button.place(x=763, y=14)
    pywinstyles.set_opacity(selections_button,color="#FB543F")

    contact_us_button = ctk.CTkButton(master=homeFrame, text="Contact Us", width=120, fg_color=("#FB543F","#FC503E"), bg_color="#FC503E", 
                                      text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: print("Contact Us clicked"))
    contact_us_button.place(x=910, y=14)
    pywinstyles.set_opacity(contact_us_button,color="#FC503E")

    about_us_button = ctk.CTkButton(master=homeFrame, text="About Us", width=120, fg_color=("#FC503E","#FC4D3D"), bg_color="#FC4D3D", 
                                    text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_aboutUs(homeFrame, about_callback))
    about_us_button.place(x=1055, y=14)
    pywinstyles.set_opacity(about_us_button,color="#FC4D3D")

    
    # Search Function
    search_frame = ctk.CTkLabel(homeFrame,text="", fg_color=("#FFFFFF","#D9D9D9"), bg_color="#D9D9D9", width=889, height=101, corner_radius=50)
    search_frame.place(x=178,y=126)
    pywinstyles.set_opacity(search_frame,color="#D9D9D9")

    location_label = ctk.CTkLabel(master=homeFrame, text="Place of Rental:", text_color="#000000", fg_color=("#FFFFFF","#D9D9D9"), 
                                  bg_color="#D9D9D9", font=("SegoeUI Bold", 16))
    location_label.place(x=189,y=165)
    pywinstyles.set_opacity(location_label,color="#D9D9D9")
    passenger_label = ctk.CTkLabel(master=homeFrame, text="Number of Passenger(s):", text_color="#000000", fg_color=("#FFFFFF","#D9D9D9"), 
                              bg_color="#D9D9D9", font=("SegoeUI Bold", 16))
    passenger_label.place(x=580,y=165)
    pywinstyles.set_opacity(passenger_label,color="#D9D9D9")

    global locations
    locations = ["Choose A Location","Penang International Airport","Penang Komtar","Penang Sentral",
                 "Kuala Lumpur International Airport","Kuala Lumpur Sentral","Kuala Lumpur City Centre",
                 "Sultan Azlan Shah Airport","Bus Terminal Amanjaya Ipoh","Ipoh Railway Station",
                 "INTI INTERNATION COLLEGE PENANG"]

    entry_1 = ctk.CTkComboBox(master=homeFrame, width=240, state="readonly", values=locations, fg_color="#D9D9D9", font=("Skranji", 14))
    entry_1.place(x=311, y=165)
    
    capacities = ["","2-seater", "4-seater", "6-seater"]

    entry_2 = ctk.CTkComboBox(master=homeFrame, width=100, state="readonly", values=capacities, fg_color="#D9D9D9", font=("Skranji", 14))
    entry_2.place(x=780, y=165)

    submit_button = ctk.CTkButton(master=homeFrame, text="Find", width=85, height=35, fg_color="#067BC1", command=lambda: findcar(homeFrame,list_callback,entry_1.get(),entry_2.get()))
    submit_button.place(x=958, y=159)

    # Promotions
    promotions_label = ctk.CTkLabel(master=homeFrame, text="Promotions", text_color="#000000", font=("SegoeUI Bold", 24))
    promotions_label.place(x=21, y=261)

    promobg_label = ctk.CTkLabel(master=homeFrame, text="No current promotions",fg_color="#D9D9D9", font=("Cooper Black", 36), width=1280, height=160)
    promobg_label.place(x=26,y=300)
    
    # Extra Content
    global manual
    manual = 1
    manual_lbl = ctk.CTkLabel(homeFrame, text="How to book a car?", fg_color=("#FFFFFF", "25272A"), font=('SegoeUI Bold', 24))
    manual_lbl.bind('<Enter>', lambda event, label=manual_lbl: label.configure(font=('SegoeUI Bold', 24, 'underline')))
    manual_lbl.bind("<Button-1>", bookingManual)
    manual_lbl.bind('<Leave>', lambda event, label=manual_lbl: label.configure(font=('SegoeUI Bold', 24)))
    manual_lbl.place(x=251,y=490)

    tnc_lbl = ctk.CTkLabel(homeFrame, text="Terms & Conditions", fg_color=("#FFFFFF", "25272A"), font=('SegoeUI Bold', 24))
    tnc_lbl.bind('<Enter>', lambda event, label=tnc_lbl: label.configure(font=('SegoeUI Bold', 24, 'underline')))
    tnc_lbl.bind("<Button-1>", openTNC)
    tnc_lbl.bind('<Leave>', lambda event, label=tnc_lbl: label.configure(font=('SegoeUI Bold', 24)))
    tnc_lbl.place(x=754,y=490)


    # Footer Section
    footer_frame = ctk.CTkLabel(homeFrame,text="", fg_color="#2A333D", width=1280, height=180)
    footer_frame.place(x=0,y=550)

    # Account section
    account_label = ctk.CTkLabel(master=homeFrame, text="Account", fg_color="#2A333D", text_color="#4B5B6D", 
                                 font=("Tw Cen MT Condensed Extra Bold", 32))
    account_label.place(x=140,y=587)
    pywinstyles.set_opacity(account_label,color="#2A333D")

    myprofile_label = ctk.CTkButton(master=homeFrame, text="My Profile", bg_color="#2A333D", fg_color="#2A333D", text_color="#9EA3A9", 
                                   font=("Tw Cen MT Condensed Extra Bold", 20),
                                   command= lambda:open_profile(homeFrame,profile_callback))
    myprofile_label.place(x=290,y=577)
    pywinstyles.set_opacity(myprofile_label,color="#2A333D")
    aboutus_label = ctk.CTkButton(master=homeFrame, text="About Car2U", bg_color="#2A333D", fg_color="#2A333D", text_color="#9EA3A9", 
                                 font=("Tw Cen MT Condensed Extra Bold", 20),
                                 command=lambda:open_aboutUs(homeFrame, about_callback))
    aboutus_label.place(x=290,y=620)
    pywinstyles.set_opacity(aboutus_label,color="#2A333D")
    upRenter_label = ctk.CTkButton(master=homeFrame, text="Upgrade to Renter", bg_color="#2A333D", fg_color="#2A333D", text_color="#9EA3A9", 
                                  font=("Tw Cen MT Condensed Extra Bold", 20),
                                 command=lambda:open_upRent(homeFrame, uprent_callback))
    upRenter_label.place(x=430,y=577)
    pywinstyles.set_opacity(upRenter_label,color="#2A333D")
    upMember_label = ctk.CTkButton(master=homeFrame, text="Upgrade to Member", bg_color="#2A333D", fg_color="#2A333D", text_color="#9EA3A9", 
                                  font=("Tw Cen MT Condensed Extra Bold", 20),
                                 command=lambda:print("connecting to upgrade Member"))
    upMember_label.place(x=430,y=620)
    pywinstyles.set_opacity(upMember_label,color="#2A333D")

    # Support section
    support_label = ctk.CTkLabel(master=homeFrame, text="Support", fg_color="#2A333D", text_color="#4B5B6D", 
                                 font=("Tw Cen MT Condensed Extra Bold", 32))
    support_label.place(x=725, y=587)
    pywinstyles.set_opacity(support_label,color="#2A333D")

    guide_label = ctk.CTkButton(master=homeFrame, text="Car2U Guide", bg_color="#2A333D", fg_color="#2A333D", text_color="#9EA3A9", 
                               font=("Tw Cen MT Condensed Extra Bold", 24),
                                 command=lambda:bookingManual)
    guide_label.place(x=880,y=577)
    pywinstyles.set_opacity(guide_label,color="#2A333D")
    findus_label = ctk.CTkButton(master=homeFrame, text="Find Us", bg_color="#2A333D", fg_color="#2A333D", text_color="#9EA3A9", 
                                font=("Tw Cen MT Condensed Extra Bold", 24),
                                 command=lambda:print("connecting to about us"))
    findus_label.place(x=880,y=620)
    pywinstyles.set_opacity(findus_label,color="#2A333D")

    rights_label = ctk.CTkLabel(master=homeFrame, text="@All Rights Reserved", bg_color="#2A333D", fg_color="#2A333D", 
                                text_color="#FFFFFF", font=("Tw Cen MT Condensed Extra Bold", 16))
    rights_label.place(x=562, y=680)
    pywinstyles.set_opacity(rights_label,color="#2A333D")

    global userInfo
    userInfo = get_user_info()
    print(f"Home : {userInfo}")

def bookingManual(event):
    global manual
    if manual == 1:
        global manualFrame
        manualFrame = ctk.CTkFrame(homeFrame, width=200, height=240,fg_color="#FFFFFF", border_color="#000000", border_width=2)
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
        for widget in homeFrame.winfo_children():
            if isinstance(manualFrame, (ctk.CTkFrame)):
                manualFrame.destroy()
        manual = 1

def openTNC(event):
    theFile = open(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\build\Terms&Condition.txt","r")
    greatString = theFile.read()
    theFile.close()
    messagebox.showinfo("Terms & Condition",greatString)