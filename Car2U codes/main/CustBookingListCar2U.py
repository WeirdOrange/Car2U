import customtkinter as ctk
import tkinter as tk
import pywinstyles
import sqlite3
from MainCar2U_UserInfo import get_user_info,set_user_info, set_CarID
from CustHomeCar2U import getCarLocate,getCarPax
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from pathlib import Path
from PIL import Image, ImageTk
from tkinter import Toplevel, messagebox
from io import BytesIO

# Set up the asset path (same as original)
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Cust-Selections")

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
    current_window.destroy()  # Close the signup window
    home_callback()

# Function to handle profile button click
def open_listing(login_callback,home_callback,profile_callback):
    booking(login_callback,home_callback,profile_callback)
    messagebox.showinfo("You are on the Car Selection page")

# Function to handle selection button click
def open_profile(current_window, profile_callback):
    current_window.destroy()  # Close the signup window
    profile_callback()

# Function to handle about us button click
def open_aboutUs(current_window, about_callback):
    current_window.destroy()  # Close the signup window
    about_callback()

# Function to handle chats button click
def open_chat(current_window, chat_callback):
    current_window.destroy()  # Close the window
    chat_callback()

def savePickLocate(location):
    global chosenPick_Location
    if location is None or location not in locations:
        chosenPick_Location = ""
    else:
        chosenPick_Location = str(location)

def getPickLocate():
    return chosenPick_Location

def getPickDate():
    return chosenPick_Date

def saveDropLocate(location):
    global chosenDrop_Location
    if location is None or location not in locations:
        chosenDrop_Location = ""
    else:
        chosenDrop_Location = str(location)

def getDropLocate():
    return chosenDrop_Location

def getDropDate():
    return chosenDrop_Date

# Function to handle selection button click
def open_bookDetails(current_window, bookdetails_callback, carid):
    # Save chosen information
    global chosenPick_Date, chosenDrop_Date
    if pickup_entry.get() != None:
        savePickLocate(pickup_entry.get())
    if dropoff_entry.get() != None:
        saveDropLocate(dropoff_entry.get())
    chosenPick_Date = pickup_date.get_date()
    chosenDrop_Date = dropoff_date.get_date()

    if userInfo == "":
        messagebox.showinfo("Please Log In","Oops! You are required to Log In before you can continue.")
    else:
        print("Chose CarID: ",carid)
        set_CarID(carid)
        current_window.destroy()  # Close the signup window
        bookdetails_callback()

# Function to handle profile button click
def open_review(current_window, review_callback):
    current_window.destroy()  # Close the signup window
    review_callback()

def Database(): #creating connection to database and creating table
    global conn, cursor
    conn = sqlite3.connect("car2u.db")
    # Enable access to columns by name
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
        
def convert_data(data):
    global pfp_img
    img_byte = BytesIO(data)
    img = Image.open(img_byte)
    pfp_img = ctk.CTkImage(img,size=(250,125))
    return pfp_img

# Hover over Items
def focus_frame(frame):
    frame.configure(fg_color="#35AAA4")
def unfocus_frame(frame):
    frame.configure(fg_color="#FFFFFF")

def fetchdata(bookdetails_callback):
    global i, result, query
    Database()
    filtering = []
    query = f"""SELECT * FROM CarDetails"""
    print(f"{filterBrand}\n{filterSeats}\n{filterTransmission}\nNext please")
    
    if filterBrand:
        model = "OR ".join(f"model LIKE '{brand}'" for brand in filterBrand)
        filtering.append(model)
    if filterSeats:
        seat = "OR ".join(f"seatingCapacity LIKE '{seating}'" for seating in filterSeats)
        filtering.append(seat)
    if filterTransmission:
        transmission = "OR ".join(f"transmissionType LIKE '{gear}'" for gear in filterTransmission)
        filtering.append(transmission)
    if filtering:
        query += " WHERE " + " AND ".join(filtering)\

    query = query +" LIMIT 6"
    if i > 0:
        query = query+f" OFFSET {i}"

    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    carlist(bookdetails_callback)

def carlist(bookdetails_callback):
    x=0

    for widget in selection_frame.winfo_children():
        if isinstance(widget, ctk.CTkFrame):
            widget.destroy()
    
    # If fewer than 6 results are returned, prevent redundant data to be displayed
    max_frames = len(result)        

    for row in result:
        if x >= max_frames:  # Stop if there are no more results
            break
        else:
            pass

        #Fetching data from database
        carid = row[0]
        name_car = row[2]
        seaters_car = row[5]
        transmission_car = row[6]
        price_car = row[7]
        carImage = convert_data(row[8])

        item_frame = ctk.CTkFrame(selection_frame,width=320, height=225, corner_radius=30, fg_color="#FFFFFF",bg_color="#FEFEFE")
        item_frame.bind("<Enter>", lambda event, f=item_frame: focus_frame(f))  # Hovering on frame
        item_frame.bind("<Button-1>", lambda event, carid=carid: open_bookDetails(bookingFrame, bookdetails_callback, carid))
        item_frame.bind("<Leave>", lambda event, f=item_frame: unfocus_frame(f))
        pywinstyles.set_opacity(item_frame, color="#FEFEFE")

        for widget in item_frame.winfo_children():
            widget.destroy()
        if x == 0 and result != None:
            item_frame.place(x=25,y=25)
        elif x == 1 and result != None:
            item_frame.place(x=375,y=25)
        elif x == 2 and result != None:
            item_frame.place(x=725,y=25)
        elif x == 3 and result != None:
            item_frame.place(x=25,y=285)
        elif x == 4 and result != None:
            item_frame.place(x=375,y=285)
        elif x == 5 and result != None:
            item_frame.place(x=725,y=285)
        else:
            print("No more data")
            
        car1_label = ctk.CTkLabel(item_frame, image=carImage, bg_color="#FFFFFF", text="")
        car1_label.place(x=35, y=5)
        pywinstyles.set_opacity(car1_label, color="#FFFFFF")
        
        car1_name = ctk.CTkLabel(item_frame, text=name_car, fg_color="#FFFFFF", bg_color="#FFFFFF", font=("Tw Cen MT Condensed Extra Bold", 20))
        car1_name.place(x=8,y=130)
        pywinstyles.set_opacity(car1_name, color="#FFFFFF")

        seats_img =  ctk.CTkImage(Image.open(relative_to_assets("image_11.png")),size=(30,30))
        seatIcon1 = ctk.CTkLabel(item_frame, image=seats_img, bg_color="#FFFFFF", text="")
        seatIcon1.place(x=9, y=170)
        pywinstyles.set_opacity(seatIcon1, color="#FFFFFF")
        car1_seats = ctk.CTkLabel(item_frame, text=seaters_car, fg_color="#FFFFFF", bg_color="#FFFFFF", font=("Tw Cen MT Condensed Extra Bold", 16))
        car1_seats.place(x=40,y=175)
        pywinstyles.set_opacity(car1_seats, color="#FFFFFF")

        transmission_img =  ctk.CTkImage(Image.open(relative_to_assets("image_12.png")),size=(30,30))
        transIcon1 = ctk.CTkLabel(item_frame, image=transmission_img, bg_color="#FFFFFF", text="")
        transIcon1.place(x=110, y=170)
        pywinstyles.set_opacity(transIcon1, color="#FFFFFF")
        car1_trans = ctk.CTkLabel(item_frame, text=transmission_car, fg_color="#FFFFFF", bg_color="#FFFFFF", font=("Tw Cen MT Condensed Extra Bold", 16))
        car1_trans.place(x=145,y=175)
        pywinstyles.set_opacity(car1_trans, color="#FFFFFF")

        price_img =  ctk.CTkImage(Image.open(relative_to_assets("image_13.png")),size=(30,30))
        priceIcon1 = ctk.CTkLabel(item_frame, image=price_img, bg_color="#FFFFFF", text="")
        priceIcon1.place(x=220, y=170)
        pywinstyles.set_opacity(priceIcon1, color="#FFFFFF")
        car1_price = ctk.CTkLabel(item_frame, text=(f"{price_car}/day"), fg_color="#FFFFFF", bg_color="#FFFFFF", font=("Tw Cen MT Condensed Extra Bold", 16))
        car1_price.place(x=250,y=175)
        pywinstyles.set_opacity(car1_price, color="#FFFFFF")
            
        x=x+1

def next(bookdetails_callback):
    global i, backBttn, query
    i = i + 6
    backBttn = ctk.CTkButton(bookingFrame, text="Back", border_color="lime green", border_width=2, fg_color="#0E5A48", width=100, bg_color="#FFFFFF", 
                             font=("Tw Cen MT Condensed Extra Bold", 16), command=lambda:back(bookdetails_callback))
    backBttn.place(x=1000,y=680)
    pywinstyles.set_opacity(nextBttn, color="#FFFFFF")
    fetchdata(bookdetails_callback)
def back(bookdetails_callback):
    global i, query
    i = i - 6
    if i <= 1:
        backBttn.destroy()
    fetchdata(bookdetails_callback)

def filter_brand(var, brand_name,bookdetails_callback):
    global filterBrand
    print(brand_name)
    if var.get() == 1:
        filterBrand.append(f"{str(brand_name)}%")
    else:
        filterBrand.remove(f"{str(brand_name)}%")
    fetchdata(bookdetails_callback)
    return filterBrand

def filter_capacity(var, capacity,bookdetails_callback):
    global filterSeats
    if var.get() == True:
        filterSeats.append(f"{str(capacity)}")
    else:
        filterSeats.remove(f"{str(capacity)}")
    fetchdata(bookdetails_callback)
    return filterSeats

def filter_transmission(var, transmission,bookdetails_callback):
    global filterTransmission
    if var.get() == True:
        filterTransmission.append(f"{str(transmission)}")
    else:
        filterTransmission.remove(f"{str(transmission)}")
    fetchdata(bookdetails_callback)
    return filterTransmission

def filters(bookdetails_callback):
    # Brand options
    brand_label = ctk.CTkLabel(filter_frame, text="Brand", font=("Arial", 20))
    brand_label.place(x=10, y=10)

    brand_vars = []
    brands = ["Toyota", "Mazda", "Perodua", "Mercedes"]
    for i, brand in enumerate(brands):
        var = ctk.IntVar()
        chk = ctk.CTkCheckBox(filter_frame, text=brand, variable=var, font=("Arial", 16),command=lambda v=var, b=brand: filter_brand(v, b,bookdetails_callback))
        chk.place(x=10, y=50 + i * 30)
        brand_vars.append(var)

    # Seating Capacity options
    capacity_label = ctk.CTkLabel(filter_frame, text="Seating Capacity", font=("Arial", 20))
    capacity_label.place(x=10, y=180)

    global capacities
    capacity_vars = []
    capacities = ["2-seater", "4-seater", "6-seater"]
    for i, capacity in enumerate(capacities):
        if pax == capacity:
            var = ctk.IntVar(value=1)
            chk = ctk.CTkCheckBox(filter_frame, text=capacity, variable=var, font=("Arial", 16), command=lambda v=var, b=capacity: filter_capacity(v, b,bookdetails_callback))
            chk.place(x=10, y=210 + i * 30)
            filterSeats.append(f"{str(pax)}")
        else:
            var = ctk.IntVar()
            chk = ctk.CTkCheckBox(filter_frame, text=capacity, variable=var, font=("Arial", 16), command=lambda v=var, b=capacity: filter_capacity(v, b,bookdetails_callback))
            chk.place(x=10, y=210 + i * 30)
            capacity_vars.append(var)

    # Transmission Type options
    transmission_label = ctk.CTkLabel(filter_frame, text="Transmission Type", font=("Arial", 20))
    transmission_label.place(x=10, y=310)

    transmission_vars = []
    transmissions = ["Manual", "Automatic"]
    for i, transmission in enumerate(transmissions):
        var = ctk.IntVar()
        chk = ctk.CTkCheckBox(filter_frame, text=transmission, variable=var, font=("Arial", 16), command=lambda v=var, b=transmission: filter_transmission(v, b,bookdetails_callback))
        chk.place(x=10, y=340 + i * 30)
        transmission_vars.append(var)

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

def booking(login_callback,home_callback,profile_callback,about_callback,bookdetails_callback,review_callback,chat_callback):
    # Create the main application window
    global bookingFrame
    bookingFrame = Toplevel()
    bookingFrame.title("Login")
    bookingFrame.geometry("1280x720")
    bookingFrame.resizable(False, False)

    # Initialize global variables
    global i, filterBrand, filterSeats, filterTransmission, filtering, userInfo
    filterBrand = []
    filterSeats = []
    filterTransmission = []
    filtering = []
    i = 0
    userInfo = get_user_info()
    print(f"About Us : {userInfo}")
    # Initialize global variables with default values
    global chosenPick_Location,chosenDrop_Location,chosenPick_Date,chosenDrop_Date
    chosenPick_Location = ""
    chosenDrop_Location = ""
    chosenPick_Date = None
    chosenDrop_Date = None

    # Navigation Tab
    nav_img = ctk.CTkImage(Image.open(relative_to_assets("image_2.png")),size=(1280,60))
    nav_label = ctk.CTkLabel(bookingFrame, image=nav_img, text="", width=1280, height=60)
    nav_label.place(x=0, y=0)

    logo_img = ctk.CTkImage(Image.open(relative_to_assets("image_3.png")),size=(75,40))
    logo_label = ctk.CTkLabel(bookingFrame, image=logo_img, text="", bg_color="#F47749", width=95, height=50)
    logo_label.place(x=5, y=5)
    pywinstyles.set_opacity(logo_label,color="#F47749")

    global pfpState
    pfpState = 1
    pfp_img = ctk.CTkImage(Image.open(relative_to_assets("image_4.png")),size=(40,40))
    pfp_label = ctk.CTkButton(bookingFrame, image=pfp_img, text="", bg_color="#F47749", fg_color="#F47749", width=40, height=40, 
                                command=lambda:accManage(bookingFrame,login_callback,profile_callback,review_callback))
    pfp_label.place(x=1180, y=5)
    pywinstyles.set_opacity(pfp_label,color="#F47749")

    # Relocate buttons
    home_button = ctk.CTkButton(master=bookingFrame, text="Home", width=120, fg_color=("#F95C41","#FA5740"), bg_color="#FA5740", 
                                text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), 
                                command=lambda:open_home(bookingFrame,home_callback))
    home_button.place(x=627, y=14)
    pywinstyles.set_opacity(home_button,color="#FA5740")

    selections_button = ctk.CTkButton(master=bookingFrame, text="Selections", width=120, fg_color=("#FA5740","#FB543F"), bg_color="#FB543F", 
                                      text_color="#FFF6F6", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: print("Selections clicked"))
    selections_button.place(x=763, y=14)
    pywinstyles.set_opacity(selections_button,color="#FB543F")

    contact_us_button = ctk.CTkButton(master=bookingFrame, text="Contact Us", width=120, fg_color=("#FB543F","#FC503E"), bg_color="#FC503E", 
                                      text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), 
                                      command=lambda: open_chat(bookingFrame, chat_callback))
    contact_us_button.place(x=910, y=14)
    pywinstyles.set_opacity(contact_us_button,color="#FC503E")

    about_us_button = ctk.CTkButton(master=bookingFrame, text="About Us", width=120, fg_color=("#FC503E","#FC4D3D"), bg_color="#FC4D3D", 
                                    text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), 
                                    command=lambda: open_aboutUs(bookingFrame, about_callback))
    about_us_button.place(x=1055, y=14)
    pywinstyles.set_opacity(about_us_button,color="#FC4D3D")

    # Locations frame
    global location, pax
    location = ""
    pax = ""

    location_frame = ctk.CTkFrame(bookingFrame, corner_radius=0, width=1090, height=90, fg_color="light grey")
    location_frame.place(x=190, y=60)

    # Pickup entry
    locateIcon_img = ctk.CTkImage(Image.open(relative_to_assets("image_6.png")),size=(40,40))
    locateIcon_label = ctk.CTkLabel(location_frame, image=locateIcon_img, text="")
    locateIcon_label.place(x=30, y=40)

    dateIcon_img = ctk.CTkImage(Image.open(relative_to_assets("image_7.png")),size=(40,40))
    dateIcon_label = ctk.CTkLabel(location_frame, image=dateIcon_img, text="")
    dateIcon_label.place(x=280, y=40)

    pickup_text = ctk.CTkLabel(location_frame, text="Pick-up Details", fg_color="#D7D7D7", font=("Tw Cen MT Condensed Extra Bold", 20))
    pickup_text.place(x=30,y=10)
    pywinstyles.set_opacity(pickup_text,color="#D7D7D7")

    global locations
    locations = ["Choose A Location","Penang International Airport","Penang Komtar","Penang Sentral",
                 "Kuala Lumpur International Airport","Kuala Lumpur Sentral","Kuala Lumpur City Centre",
                 "Sultan Azlan Shah Airport","Bus Terminal Amanjaya Ipoh","Ipoh Railway Station",
                 "INTI INTERNATION COLLEGE PENANG"]
    
    global pickup_entry,pickup_date
    today = datetime.today()
    pickup_entry = ctk.CTkComboBox(master=location_frame, width=175, state="readonly", values=locations, fg_color="#bbbbbb", font=("Skranji", 12))
    pickup_entry.place(x=85, y=50)
    pickup_date = DateEntry(location_frame, width=12, background='orange', foreground='white', borderwidth=2, font=("Arial", 10), mindate=today)
    pickup_date.place(x=345, y=50)

    # Drop-off entry
    locateIcon2_img = ctk.CTkImage(Image.open(relative_to_assets("image_6.png")),size=(40,40))
    locateIcon2_label = ctk.CTkLabel(location_frame, image=locateIcon2_img, text="")
    locateIcon2_label.place(x=565, y=40)

    dateIcon2_img = ctk.CTkImage(Image.open(relative_to_assets("image_7.png")),size=(40,40))
    dateIcon2_label = ctk.CTkLabel(location_frame, image=dateIcon2_img, text="")
    dateIcon2_label.place(x=815, y=40)

    dropoff_text = ctk.CTkLabel(location_frame, text="Drop-off Details", fg_color="#D7D7D7", font=("Tw Cen MT Condensed Extra Bold", 20))
    dropoff_text.place(x=565,y=5)
    pywinstyles.set_opacity(dropoff_text,color="#D7D7D7")

    global dropoff_entry,dropoff_date
    tmr = today + timedelta(days=1)
    dropoff_entry = ctk.CTkComboBox(master=location_frame, width=175, state="readonly", values=locations, fg_color="#bbbbbb", font=("Skranji", 12))
    dropoff_entry.place(x=620, y=50)
    dropoff_date = DateEntry(location_frame, width=12, background='orange', foreground='white', borderwidth=2, font=("Arial", 10), mindate=tmr)
    dropoff_date.place(x=880, y=50)

    # If user had already chosen location from home page
    location = getCarLocate()
    pax = getCarPax()
    print(f"Location: {location}, Pax: {pax}")
    if location != None:
        if location != "Choose A Location":
            pickup_entry.set(location)
            dropoff_entry.set(location)

    # Create a frame for the filter options
    global filter_frame
    filter_frame = ctk.CTkFrame(bookingFrame, corner_radius=0, width=190, height=670, fg_color="white")
    filter_frame.place(x=0, y=60)

    filters(bookdetails_callback)

    # Item 
    global selection_frame, nextBttn, item_frame
    selection_frame = ctk.CTkFrame(bookingFrame, width=1090, height=570,fg_color="white")
    selection_frame.place(x=190,y=150)
    selection_frameimg = ctk.CTkImage(Image.open(relative_to_assets("image_1.png")),size=(1090,570))
    selection_framebg = ctk.CTkLabel(selection_frame, text="", image=selection_frameimg)
    selection_framebg.place(x=0,y=0)
    
    fetchdata(bookdetails_callback)

    nextBttn = ctk.CTkButton(bookingFrame, text="Next", border_color="lime green", border_width=2, fg_color="#0E5A48", width=100, bg_color="#FFFFFF", 
                             font=("Tw Cen MT Condensed Extra Bold", 16), command=lambda:next(bookdetails_callback))
    nextBttn.place(x=1150,y=680)
    pywinstyles.set_opacity(nextBttn, color="#FFFFFF")
