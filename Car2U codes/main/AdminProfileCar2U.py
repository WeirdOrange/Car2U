import tkinter as tk
import customtkinter as ctk
import pywinstyles
import sqlite3
import tkinter
import os
from MainCar2U_UserInfo import get_user_info,set_user_info
from tkinter import Toplevel, messagebox, filedialog, Scrollbar
from tkcalendar import Calendar, DateEntry
from calendar import monthrange
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageTk
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas

# For plotting graphs
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Admin-Profile")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def Database(): #creating connection to database and creating table
    global conn, cursor
    conn = sqlite3.connect("car2u.db")
    # Enable access to columns by name
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

# Function to handle login button click
def open_login(current_window, login_callback):
    current_window.destroy()  # Close the window
    userInfo = ""
    set_user_info(userInfo)
    login_callback()

# Function to handle profile button click
def open_home(current_window, home_callback):
    current_window.destroy()  # Close the window
    home_callback()

# Function to handle selection button click
def open_history(current_window, list_callback):
    current_window.destroy()  # Close the window
    list_callback()

# Function to handle profile button click
def open_profile():
    messagebox.showinfo("You are on the Profile page")

# Function to handle car details button click
def open_Cdetail(current_window, detail_callback):
    current_window.destroy()  # Close the window
    detail_callback()

# Function to handle bookings button click
def open_bookings(current_window, booking_callback):
    current_window.destroy()  # Close the window
    booking_callback()

# Function to handle chats button click
def open_chat(current_window, chat_callback):
    current_window.destroy()  # Close the window
    chat_callback()

def accManage(current_window, login_callback):
    global pfpState, droptabFrame

    if pfpState == 1:
        droptabFrame = ctk.CTkFrame(current_window,width=160,height=170, bg_color="#E6F6FF",fg_color="#E6F6FF")
        droptabFrame.place(x=16, y=413)

        if userInfo == "":
            droptabFrame.configure(height=57)
            logoin = ctk.CTkButton(master=droptabFrame, text="Log In", text_color="#000000", fg_color=("#E6F6FF","#D9D9D9"), 
                                    bg_color="#E6F6FF", font=("SegoeUI Bold", 20), command=lambda:open_login(current_window, login_callback))
            logoin.place(x=30,y=13)

        else:
            myAcc = ctk.CTkButton(master=droptabFrame, text="My Account", text_color="#000000", fg_color=("#E6F6FF","#D9D9D9"), anchor='center', width=110,
                                        bg_color="#E6F6FF", font=("SegoeUI Bold", 20), command=lambda:open_profile())
            myAcc.place(x=25,y=15)

            setting = ctk.CTkButton(master=droptabFrame, text="Setting", text_color="#000000", fg_color=("#E6F6FF","#D9D9D9"), anchor='center', width=110,
                                        bg_color="#E6F6FF", font=("SegoeUI Bold", 20))
            setting.place(x=25,y=70)

            logout = ctk.CTkButton(master=droptabFrame, text="Log Out", text_color="#000000", fg_color=("#E6F6FF","#D9D9D9"), anchor='center', width=110,
                                        bg_color="#E6F6FF", font=("SegoeUI Bold", 20), command=lambda:open_login(current_window, login_callback))
            logout.place(x=25,y=125)
        pfpState = 0
    else:
        droptabFrame.destroy()
        pfpState = 1

def fetch_user_data():
    global result
    Database()
    userInfo = get_user_info()
    print(f"UserID : {userInfo}")
    query = f"""SELECT agencyName,agencyEmail,agencyLocation,agencyContactNo,agencyLogo FROM RentalAgency WHERE agencyID = '{userInfo}'"""
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    accInfo()


def add_header_footer(c, doc_title):
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 24)
    c.drawString(40, height - 45, doc_title)  # Title at the top
    
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 60, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.line(40, height - 70, width - 40, height - 70)  # Horizontal line under the header

    # Add an image on the right
    image_width = 95
    image_height = 50
    image_path = relative_to_assets("image_3.png")
    x_image = width - image_width - 40  # Position 40 units from the right edge
    y_position = height-image_height-10  # Y position (e.g., 100 units from top)

    c.drawImage(image_path, x_image, y_position, width=image_width, height=image_height,mask="auto")
    
    # Agency details at the top
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, height - 90, f"Agency Name : {name}")  
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, height - 105, f"Email : {email}")  
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, height - 120, f"Address : {address}")  

    # Add footer
    c.setFont("Helvetica", 12)
    c.drawString(40, 40, "Car2U Official Car Rental Services")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(width - 220, 40, "Contact Us: car2uofficial.com")
    c.line(40, 60, width - 40, 60)  # Horizontal line above the footer

    # Page number
    c.setFont("Helvetica", 10)
    c.drawString(width - 70, 20, f"Page {c.getPageNumber()}")


# Generate PDF for selected booking
def save_selected_as_pdf(title,rating,bookings,total):

    pdf_filename = f"{title} Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=A4)
    width, height = A4
    add_header_footer(c, title)

    x_position = 60
    y_position = height - 150  # Start text below the header

    c.drawString(40, y_position, "Cars Rating")
    y_position = y_position - 10
    c.line(40, y_position, width-40, y_position) 

    c.setFont("Helvetica", 12)
    
    # Display each Rating field horizontally
    ratingfields = ["Car No.", "Car Average Rating", "Numbers of New Rating"]

    y_position = y_position - 15
    for field in ratingfields:
        c.drawString(x_position, y_position, field)
        x_position += 130  # Move down for the next line
    
    y_position = y_position - 15
    c.line(40, y_position, width-40, y_position) 
    
    y_position = y_position - 30
    if not rating:
        c.drawString(60, y_position, "No Cars Rated")
    
    for row in rating:
        x_position = 60
        for field in row:
            c.drawString(x_position, y_position, str(field))
            x_position += 130
        y_position -= 20  # Move down for the next line

        # Move to next page if out of space
        if y_position < 100:
            c.showPage()
            add_header_footer(c, title)
            y_position = height - 100
    
    y_position = y_position - 10
    c.line(40, y_position, width-40, y_position) 

    y_position = y_position - 50
    c.drawString(40, y_position, "Rental Revenues")

    y_position = y_position - 10
    c.line(40, y_position, width-40, y_position) 
    
    bookingsfield = ["Car No.","Numbers of dakys booked","Revenues"]

    x_position = 60
    y_position = y_position-20
    for i,field in enumerate(bookingsfield):
        c.drawString(x_position, y_position, field)
        
        if i == 1:
            x_position+=200
        else:
            x_position += 130  # Move down for the next line

    y_position = y_position-10
    c.line(40, y_position, width-40, y_position) 

    if not bookings:
        c.drawString(40, y_position-25, "No Cars Rated")

    y_position = y_position-25
    for row in bookings:
        x_position = 60
        for i,field in enumerate(row):
            c.drawString(x_position, y_position, str(field))

            if i == 1:
                x_position+=200
            else:
                x_position += 130  
        y_position -= 20 # Move down for the next line

        # Move to next page if out of space
        if y_position < 100:
            c.showPage()
            add_header_footer(c, title)
            y_position = height - 100
    
    y_position = y_position-25
    c.line(40, y_position, width-40, y_position) 
    
    y_position = y_position-25
    c.drawString(60, y_position, "Total")
    x_position = 390
    for i,row in enumerate(total):
        c.drawString(x_position, y_position, str(row[i]))
    
    y_position = y_position-15
    c.line(40, y_position, width-40, y_position) 
    
    c.showPage()
    c.save()

    return pdf_filename


def save_and_print_selected_booking(title,rating,bookings,total):
    pdf_filename = save_selected_as_pdf(title,rating,bookings,total)

    if pdf_filename:
        if os.name == 'posix':  # For Linux/macOS
            os.system(f'lpr {pdf_filename}')
        elif os.name == 'nt':  # For Windows
            os.startfile(pdf_filename, "print")

        messagebox.showinfo("PDF Saved",f"Selected booking details saved as {pdf_filename}.")


def accInfo():
    for widget in info_frame.winfo_children():
        if isinstance(widget, (ctk.CTkFrame,ctk.CTkLabel,ctk.CTkEntry,ctk.CTkComboBox,ctk.CTkButton)):
            widget.destroy()
    # Check if dobEntry and nameEntry exists before trying to destroy it
    if 'nameEntry' in globals():
        if isinstance(nameEntry,ctk.CTkEntry):
            nameEntry.destroy()

    global name,email,address,contact, infoData, user_name_label,pfp_img
    infoData = []
    for row in result:
        name = row[0]
        infoData.append(name)
        email = row[1]
        infoData.append(email)
        address = row[2]
        infoData.append(address)
        contact = row[3]
        infoData.append(contact)
        pfp = row[4]

        if pfp != None:
            pfp_img = convert_data(pfp)
        else:
            pfp_img = ctk.CTkImage(Image.open(relative_to_assets("image_6.png")),size=(200,200))
    
    # Placeholder for user image
    user_image = ctk.CTkButton(adminProfileFrame, image=pfp_img, text="", width=200, height=200, bg_color="#FFFFFF", fg_color="#FFFFFF", 
                               command=lambda: convertToBinaryData())
    user_image.place(x=230, y=50)
    pywinstyles.set_opacity(user_image,color="#FFFFFF")

    info_labels = [("Email:", 15), ("Location:", 50), ("Phone Number:", 90)]
    for text, y_pos in info_labels:
        label = ctk.CTkLabel(info_frame, text=text, font=("Skranji", 20), anchor='e', width=150, text_color="#000000")
        label.place(x=15, y=y_pos)

    info_labels = [(email, 10), (address, 50), (contact, 90)]
    for text, y_pos in info_labels:
        label = ctk.CTkLabel(info_frame, text=text, font=("Skranji", 20), text_color="#000000")
        label.place(x=175, y=y_pos)

    user_name_label = ctk.CTkLabel(adminProfileFrame, text=name, font=("Cooper Black", 40), text_color="#000000", bg_color="#73CDFF", fg_color="#73CDFF")
    user_name_label.place(x=480, y=30)
    pywinstyles.set_opacity(user_name_label,color="#73CDFF")
    
    edit_info = ctk.CTkButton(info_frame, text="Edit", width=80, corner_radius=50, fg_color="#F95F43", bg_color="#DEF3FF",
                              font=("Tw Cen MT Condensed Extra Bold", 16), text_color="#FFFFFF", command=lambda: editInfo())
    edit_info.place(x=640, y=125)
    pywinstyles.set_opacity(edit_info,color="#DEF3FF")
        
    print(infoData)

def editInfo():
    for widget in info_frame.winfo_children():
        if isinstance(widget, (ctk.CTkFrame,ctk.CTkLabel,ctk.CTkButton)):
            widget.destroy()
    if isinstance(user_name_label,ctk.CTkLabel):
        user_name_label.destroy()

    info_labels = [("Email:", 15), ("Location:", 50), ("Phone Number:", 90)]
    for text, y_pos in info_labels:
        label = ctk.CTkLabel(info_frame, text=text, font=("Skranji", 20), anchor='e', width=150, text_color="#000000")
        label.place(x=15, y=y_pos)
    # Entries 
    global nameEntry
    nameEntry = ctk.CTkEntry(adminProfileFrame, width=438, height=50, font=("Skranji", 40), text_color="#000000")
    nameEntry.insert(0,name)
    nameEntry.place(x=480, y=30)

    emailEntry = ctk.CTkEntry(info_frame, width=438, height=28, font=("Skranji", 20), text_color="#000000")
    emailEntry.insert(0,email)
    emailEntry.place(x=175, y=10)

    contactEntry = ctk.CTkEntry(info_frame, width=438, height=28, font=("Skranji", 20), text_color="#000000")
    if contact != None:
        contactEntry.insert(0,contact)
    contactEntry.place(x=175, y=90)

    addressEntry = ctk.CTkEntry(info_frame, width=438, height=28, font=("Skranji", 20), text_color="#000000")
    if addressEntry != None:
        addressEntry.insert(0,address)
    addressEntry.place(x=175, y=50)
    
    edit_info = ctk.CTkButton(info_frame, text="Done", width=80, corner_radius=50, fg_color="#F95F43", bg_color="#DEF3FF",
                              font=("Tw Cen MT Condensed Extra Bold", 16), text_color="#FFFFFF", 
                              command=lambda: info_Update_Checker(nameEntry.get(),emailEntry.get(),contactEntry.get(),addressEntry.get()))
    edit_info.place(x=640, y=125)
    pywinstyles.set_opacity(edit_info,color="#DEF3FF")

def info_Update_Checker(returnName,returnEmail,returnContact,returnAddress):
    Database()

    if not returnName or not returnEmail or not returnContact or not returnAddress:
        messagebox.showerror("Input Error", "All fields are required!")
    elif returnName == name and returnEmail == email and returnContact == contact and returnAddress == address:
        messagebox.showerror("Nothing Changed.")
        fetch_user_data()
    else:
        try:
            cursor.execute(f"UPDATE RentalAgency SET agencyName=?,agencyEmail=?,agencyLocation=?,agencyContactNo=? WHERE agencyID = {get_user_info()}",
                           (str(returnName),str(returnEmail),str(returnAddress),str(returnContact)))
            conn.commit()
            messagebox.showinfo("Update Successful", "You have successfully update your info!")
            fetch_user_data()
        except sqlite3.Error as e:
            messagebox.showerror("Error", "Error occurred during registration: {}".format(e))
        finally:
            conn.close()

def convertToBinaryData(): 
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        try:
            # Convert binary format to images
            with open(file_path, 'rb') as file: 
                blobData = file.read() 
                insertBLOB(blobData)
            return blobData 
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload image: {e}")
            

def convert_data(data):
    global pfp_image
    img_byte = BytesIO(data)
    img = Image.open(img_byte)
    img = img.resize((240,240), Image.Resampling.LANCZOS)
    pfp_img = ImageTk.PhotoImage(img)
    return pfp_img

def insertBLOB(data): 
    try: 
        Database()
        
        # Updating the previous blob data to new
        cursor.execute(f"""UPDATE RentalAgency SET agencyLogo= ? WHERE agencyID = {get_user_info()}""", (data,))
        conn.commit() 
        print("Image and file inserted successfully as a BLOB into a table") 
        cursor.close() 
  
    except sqlite3.Error as error: 
        print("Failed to insert blob data into sqlite table", error) 
        messagebox.showinfo("Failed to insert blob data into sqlite table", error) 
      
    finally: 
        if conn: 
            conn.close() 
            print("the sqlite connection is closed") 
            fetch_user_data()

def adminProfile(login_callback,home_callback,detail_callback,booking_callback,chat_callback):
    # Create the main application window
    global adminProfileFrame
    adminProfileFrame = Toplevel()
    adminProfileFrame.title("Profile Page")
    adminProfileFrame.geometry("1280x720")
    adminProfileFrame.resizable(False, False)
    adminProfileFrame.config(bg="white")

    global userInfo
    userInfo = get_user_info()
    print(f"Profile : {userInfo}")

    # Background
    bg_img = ctk.CTkImage(Image.open(relative_to_assets("bg.png")),size=(1280,720))
    bg_label = ctk.CTkLabel(adminProfileFrame, image=bg_img, text="", width=1280, height=60)
    bg_label.place(x=0, y=0)

    # Navigation Tab
    nav_img = ctk.CTkImage(Image.open(relative_to_assets("nav.png")),size=(200,720))
    nav_label = ctk.CTkLabel(adminProfileFrame, image=nav_img, text="")
    nav_label.place(x=0, y=0)

    logo_img = ctk.CTkImage(Image.open(relative_to_assets("Logo.png")),size=(150,60))
    logo_label = ctk.CTkLabel(adminProfileFrame, image=logo_img, text="", bg_color="#F47749", width=95, height=50)
    logo_label.place(x=22, y=10)
    pywinstyles.set_opacity(logo_label,color="#F47749")
    
    global pfpState
    pfpState = 1
    pfp_img = ctk.CTkImage(Image.open(relative_to_assets("image_6.png")),size=(100,100))
    pfp_label = ctk.CTkButton(adminProfileFrame, image=pfp_img, text="", bg_color="#FE453B", fg_color="#FE453B",
                              width=40, height=40, command=lambda:accManage(adminProfileFrame,login_callback))
    pfp_label.place(x=41, y=590)
    pywinstyles.set_opacity(pfp_label,color="#FE453B")

    # Relocate buttons
    home_button = ctk.CTkButton(master=adminProfileFrame, text="Home", width=120, fg_color=("#F95C41","#FA5740"), bg_color="#FA5740", 
                                text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_home(adminProfileFrame,home_callback))
    home_button.place(x=22, y=100)
    pywinstyles.set_opacity(home_button,color="#FA5740")

    booking_button = ctk.CTkButton(master=adminProfileFrame, text="Bookings", width=120, fg_color=("#FA5740","#FB543F"), bg_color="#FB543F", 
                                      text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda:open_bookings(adminProfileFrame,booking_callback))
    booking_button.place(x=22, y=165)
    pywinstyles.set_opacity(booking_button,color="#FB543F")

    inventory_button = ctk.CTkButton(master=adminProfileFrame, text="Inventory", width=120, fg_color=("#FB543F","#FC503E"), bg_color="#FC503E", 
                                      text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), 
                                      command=lambda: open_Cdetail(adminProfileFrame, detail_callback))
    inventory_button.place(x=22, y=230)
    pywinstyles.set_opacity(inventory_button,color="#FC503E")

    chat_button = ctk.CTkButton(master=adminProfileFrame, text="Chat", width=120, fg_color=("#FC503E","#FC4D3D"), bg_color="#FC4D3D", 
                                    text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_chat(adminProfileFrame, chat_callback))
    chat_button.place(x=22, y=295)
    pywinstyles.set_opacity(chat_button,color="#FC4D3D")

    # User Info section
    # Personal information section
    global info_frame
    info_frame = ctk.CTkFrame(adminProfileFrame, width=760, height=180, bg_color="#87D4FF", fg_color="#DEF3FF", border_width=2, border_color="#000000")
    info_frame.place(x=480, y=100)
    pywinstyles.set_opacity(info_frame,color="#FC4D3D")

    fetch_user_data()

    # Statistics filter + title
    statsTitle = ctk.CTkLabel(adminProfileFrame, text="Statistic Report", width=170, font=("Tw Cen MT Condensed Extra Bold", 24))
    statsTitle.place(x=250,y=295)

    global months,yearList, monthBox
    months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    monthBox = ctk.CTkComboBox(adminProfileFrame, state="readonly", values=months, font=("Tw Cen MT Condensed Extra Bold", 20))
    monthBox.place(x=425,y=295)
    current_month = datetime.now().month
    monthBox.set(months[current_month-1])

    # get current year
    year_now = datetime.now().year
    # start list 10 years ago
    years = list(range(year_now-10, year_now+1))
    yearList = []
    for year in years:
        yearList.append(str(year))
    yearBox = ctk.CTkComboBox(adminProfileFrame, state="readonly", values=yearList, font=("Tw Cen MT Condensed Extra Bold", 20), width=100)
    yearBox.place(x=580,y=295)
    yearBox.set(year_now)

    refreshBttn = ctk.CTkButton(adminProfileFrame, text="Refresh", width=75, corner_radius=50, fg_color="#067BC1",
                              font=("Tw Cen MT Condensed Extra Bold", 16), text_color="#FFFFFF", 
                              command=lambda:refresh(datetime.strptime(monthBox.get(), '%B').month,yearBox.get()))
    refreshBttn.place(x=700, y=295)


    # Statistics Info
    statsFrame = ctk.CTkFrame(adminProfileFrame, width=945, height=390, fg_color="#FFFFFF",bg_color="#FFFFFF", border_width=2, border_color="#000000")
    statsFrame.place(x=250,y=330)
    pywinstyles.set_opacity(statsTitle,color="#FFFFFF")

    global monthlyFrame,saleFrame,yearlyFrame
    monthlyFrame = ctk.CTkFrame(statsFrame, width=440, height=340, border_width=4, border_color="#2F59C1",fg_color="#FFFFFF",bg_color="#F7F7F7")
    monthlyFrame.place(x=15,y=15)
    pywinstyles.set_opacity(statsTitle,color="#F7F7F7")
    monthlyLabel = ctk.CTkLabel(monthlyFrame, text="Monthly Report", width=430, anchor="center", font=("Tw Cen MT Condensed Extra Bold", 20))
    monthlyLabel.place(x=5, y=10)
    monthlyEarns = ctk.CTkLabel(monthlyFrame, text="Revenue: ", width=100, anchor="e", font=("Tw Cen MT Condensed Extra Bold", 16), text_color="#000000")
    monthlyEarns.place(x=50,y=300)
    mPrintBttn = ctk.CTkButton(monthlyFrame, text="Print", width=75, height=30, corner_radius=20, fg_color="#F95F43", font=("Tw Cen MT Condensed Extra Bold", 16), text_color="#FFFFFF",
                               command=lambda: save_and_print_selected_booking(saveMonth,mthRating,mthRenting,mthprofits))
    mPrintBttn.place(x=280,y=300)

    saleFrame = ctk.CTkFrame(statsFrame, width=440, height=130, border_width=4, border_color="#2F59C1",fg_color="#FFFFFF",bg_color="#F7F7F7")
    saleFrame.place(x=490,y=15)
    pywinstyles.set_opacity(statsTitle,color="#F7F7F7")
    saleLabel = ctk.CTkLabel(saleFrame, text="Cars Rating", width=115, anchor="center", font=("Tw Cen MT Condensed Extra Bold", 20))
    saleLabel.place(x=315, y=10)

    yearlyFrame = ctk.CTkFrame(statsFrame, width=440, height=340, border_width=4, border_color="#2F59C1",fg_color="#FFFFFF",bg_color="#F7F7F7")
    yearlyFrame.place(x=490,y=15)
    pywinstyles.set_opacity(statsTitle,color="#F7F7F7")
    yearlyLabel = ctk.CTkLabel(yearlyFrame, text="Yearly Report", width=430, anchor="center", font=("Tw Cen MT Condensed Extra Bold", 20))
    yearlyLabel.place(x=5, y=10)
    yearlyEarns = ctk.CTkLabel(yearlyFrame, text="Total Revenue: ", width=100, anchor="e", font=("Tw Cen MT Condensed Extra Bold", 16), text_color="#000000")
    yearlyEarns.place(x=50,y=200)
    yPrintBttn = ctk.CTkButton(yearlyFrame, text="Print", width=75, height=30, corner_radius=20, fg_color="#F95F43", font=("Tw Cen MT Condensed Extra Bold", 16), text_color="#FFFFFF",
                               command=lambda: save_and_print_selected_booking(yrTitle,yrRating,yrRenting,yrProfit))
    yPrintBttn.place(x=280,y=300)
    
    global monthStatsFrame,monthNavFrame 
    monthStatsFrame = ctk.CTkFrame(monthlyFrame, width=390, height=230)
    monthStatsFrame.place(x=10,y=40)
    monthNavFrame = ctk.CTkFrame(monthlyFrame, width=10, height=200)
    monthNavFrame.place(x=4,y=20)
    
    global yearStatsFrame,yearNavFrame
    yearStatsFrame = ctk.CTkFrame(yearlyFrame, width=390, height=230)
    yearStatsFrame.place(x=10,y=40)
    yearNavFrame = ctk.CTkFrame(yearlyFrame, width=10, height=200)
    yearNavFrame.place(x=4,y=20)
    refresh(str(datetime.now().month),str(datetime.now().year))


def refresh(month,year):       
    for widget in monthStatsFrame.winfo_children():
        widget.destroy()  
    for widget in monthNavFrame.winfo_children():
        widget.destroy()  
    for widget in yearStatsFrame.winfo_children():
        widget.destroy()

    monthinfo(month,year)
    yearlyinfo(year)

def monthlyReport(notRent,rejectBooking,gotCancelled,success,earning): # Monthly Report
    global mfig
    activities = [f'Cars Not Rented:{notRent}', f'Cars Rejected:{rejectBooking}', f'Bookings Cancelled:{gotCancelled}', f'Cars Rented:{success}']
    slices = [notRent, rejectBooking, gotCancelled, success]
    colors = ['#247BA0', '#D80000', '#60D8C4', '#9BBB58']

    # Create a figure for the pie chart
    mfig = Figure(figsize=(3.9, 2.3), dpi=100, constrained_layout=True)
    ax = mfig.add_subplot(111)
    ax.pie(slices, colors=colors, startangle=90, shadow=True, explode=(0, 0, 0.1, 0), autopct='%1.1f%%', textprops={'color': 'white'})
    ax.legend(labels=activities, fontsize=7,loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=2)

    global monthcanvas
    monthcanvas = FigureCanvasTkAgg(mfig, master=monthStatsFrame)  # A tk.DrawingArea.
    monthcanvas.draw()
    monthcanvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

    global toolbar
    toolbar = VerticalToolbar(monthcanvas, monthNavFrame)
    toolbar.update()

    monthlyEarnings = ctk.CTkLabel(monthlyFrame, text=f"RM {str(earning)}", width=100, anchor="center", font=("Tw Cen MT Condensed Extra Bold", 16), text_color="#000000")
    monthlyEarnings.place(x=160,y=300)
    

def monthinfo(month,year): # Fetching info for monthly report
    global notRent,rejectBooking,gotCancelled,success,earning
    global mthRenting,saveMonth
    saveMonth = f"{monthBox.get()} {year} Report"
    year = int(year)
    month = int(month)
    
    firstDayofMonth = f"{year}-{month}-01"
    firstDayofMonth = datetime.strptime(firstDayofMonth,"%Y-%m-%d")
    firstDayofMonth = datetime.strftime(firstDayofMonth,"%Y-%m-%d")
            
    # Find last date of the month
    last_day = monthrange(year,month)
    end_month = f"{year}-{month}-{last_day[1]:02d}"
    end_month = datetime.strptime(end_month,"%Y-%m-%d")
    end_month = datetime.strftime(end_month,"%Y-%m-%d")

    # Fetching Cars Not Rent
    Database()
    cursor.execute("""SELECT count(carID) from CarDetails
                        WHERE not EXISTS(SELECT * from BookingDetails where BookingDetails.carID=CarDetails.carID and 
                        pickupDate >= ? and pickupDate <= ?) and agencyID=?""",(firstDayofMonth,end_month,userInfo))
    unRent = cursor.fetchall()
    conn.close()

    if not unRent:
        notRent = 0
    for row in unRent:
        notRent = row[0]

    # Fetching rejected bookings
    Database()
    cursor.execute("""SELECT count(bookingStatus) from BookingDetails b
                        INNER join CarDetails c on b.carID=c.carID
                        WHERE bookingStatus="Rejected" and pickupDate >= ? and pickupDate <= ? and c.agencyID = ?""",(firstDayofMonth,end_month,userInfo))
    rejected = cursor.fetchall()
    conn.close()

    if not rejected:
        rejectBooking = 0
    for row in rejected:
        rejectBooking = row[0]

    # Select cars that got cancelled
    Database()
    cursor.execute("""SELECT count(bookingStatus) from BookingDetails b
                        INNER join CarDetails c on b.carID=c.carID
                        WHERE bookingStatus="Cancelled" and pickupDate >= ? and pickupDate <=? and c.agencyID = ?""",(firstDayofMonth,end_month,userInfo))
    cancel = cursor.fetchall()
    conn.close()

    if not cancel:
        gotCancelled = 0
    for row in cancel:
        gotCancelled = row[0]

    # Select cars that are successfully rented
    Database()
    cursor.execute("""SELECT count(bookingStatus) from BookingDetails b INNER join CarDetails c on b.carID=c.carID
                        WHERE bookingStatus="Rented" and pickupDate >= ? and pickupDate <= ? and c.agencyID = ?""",(firstDayofMonth,end_month,userInfo))
    rented = cursor.fetchall()
    conn.close()

    if not rented:
        success = 0
    for row in rented:
        success = row[0]
        
    # Monthly earnings
    global mthprofits
    Database()
    cursor.execute("""SELECT printf("%.2f", (sum(totalAmount))) from BookingDetails b
                        INNER join CarDetails c on b.carID=c.carID
                        WHERE bookingStatus in ("Approved","On Rent", "Rented") and
                        pickupDate >= ? and pickupDate <= ? and c.agencyID = ?""",(firstDayofMonth,end_month,userInfo))
    mthprofits = cursor.fetchall()
    conn.close()

    if not mthprofits:
        earning = 0
    for row in mthprofits:
        earning = row[0]

    # Monthly Report print info
    Database()
    cursor.execute("""SELECT C.registrationNo,sum(julianday(date(dropoffDate)) - julianday(date(pickupDate))) as difference,printf("%.2f", (sum(totalAmount))) FROM BookingDetails B
                        INNER JOIN CarDetails C ON B.carID = C.carID
                        WHERE bookingStatus in ("Approved","On Rent", "Rented") AND pickupDate >= ? and pickupDate <= ? AND agencyID= ?
						GROUP by B.carID
                        ORDER by C.registrationNo""",(firstDayofMonth,end_month,userInfo))
    mthRenting = cursor.fetchall()
    conn.close()
        
    # Select cars that rated
    global mthRating
    firstday = f"{year}-01-01 00:00:00"
    lastday = f"{year}-12-31 23:59:59"
    
    Database()
    cursor.execute("""SELECT C.registrationNo,round(avg(ratings),1),count(ratings) as 'Number of Ratings' FROM Reviews R
                        INNER JOIN BookingDetails B on R.bookingID = B.bookingID
                        INNER JOIN CarDetails C ON C.carID = B.carID
                        GROUP by C.carID HAVING agencyID=? AND R.dateCreated >= ? AND R.dateCreated <= ?""",(userInfo,firstday,lastday))
    mthRating = cursor.fetchall()
    conn.close()

    monthlyReport(notRent,rejectBooking,gotCancelled,success,earning)

def yearlyinfo(year): # Yearly Report
    global ynotRent,yrejectBooking,ygotCancelled,ysuccess,yearnings
    global yrTitle,yrRenting

    firstday = f"{year}-01-01"
    lastday = f"{year}-12-31"

    # Fetching Cars Not Rent
    Database()
    
    cursor.execute("""SELECT * from CarDetails
                        WHERE not EXISTS(SELECT * from BookingDetails where BookingDetails.carID=CarDetails.carID and 
                        pickupDate >= ? and pickupDate <= ?) and agencyID=?""",(firstday,lastday,userInfo))
    unRent = cursor.fetchall()
    conn.close()

    print(unRent)
    if not unRent:
        ynotRent = 0
        print(ynotRent)
    else:
        for row in unRent:
            ynotRent = row[0]
            print(ynotRent)

    # Fetching rejected bookings
    Database()
    cursor.execute("""SELECT count(bookingStatus) from BookingDetails b
                        INNER join CarDetails c on b.carID=c.carID
                        WHERE bookingStatus="Rejected" and pickupDate >= ? and pickupDate <= ? and c.agencyID = ?""",(firstday,lastday,userInfo))
    rejected = cursor.fetchall()
    conn.close()

    if not rejected:
        yrejectBooking = 0
    for row in rejected:
        yrejectBooking = row[0]

    # Select cars that got cancelled
    Database()
    cursor.execute("""SELECT count(bookingStatus) from BookingDetails b
                        INNER join CarDetails c on b.carID=c.carID
                        WHERE bookingStatus="Cancelled" and pickupDate >= ? and pickupDate <= ? and c.agencyID = ?""",(firstday,lastday,userInfo))
    cancel = cursor.fetchall()
    conn.close()

    if not cancel:
        ygotCancelled = 0
    for row in cancel:
        ygotCancelled = row[0]

    # Select cars that are successfully rented
    Database()
    cursor.execute("""SELECT count(bookingStatus) from BookingDetails b
                        INNER join CarDetails c on b.carID=c.carID
                        WHERE bookingStatus="Rented" and pickupDate >= ? and pickupDate <= ? and c.agencyID = ?""",(firstday,lastday,userInfo))
    rented = cursor.fetchall()
    conn.close()

    if not rented:
        ysuccess = 0
    for row in rented:
        ysuccess = row[0]
        
    # Yearly Earnings
    global yrProfit
    Database()
    cursor.execute("""SELECT printf("%.2f", (sum(totalAmount))) from BookingDetails b
                        INNER join CarDetails c on b.carID=c.carID
                        WHERE bookingStatus in ("Approved","On Rent", "Rented") and pickupDate >= ? and pickupDate <= ? and c.agencyID = ?""",
                        (firstday,lastday,userInfo))
    yrProfit = cursor.fetchall()
    conn.close()

    if not yrProfit:
        yearnings = 0
    for row in yrProfit:
        yearnings = row[0]

    # Yearly Report print info
    Database()
    cursor.execute("""SELECT C.registrationNo,sum(julianday(date(dropoffDate)) - julianday(date(pickupDate))) as difference,printf("%.2f", (sum(totalAmount))) FROM BookingDetails B
                        INNER JOIN CarDetails C ON B.carID = C.carID
                        where bookingStatus in ("Approved","On Rent", "Rented") AND pickupDate >= ? and pickupDate <= ? AND agencyID= ?
						GROUP by B.carID
                        ORDER by C.registrationNo""",(firstday,lastday,userInfo))
    yrRenting = cursor.fetchall()
    conn.close()

    if not yrRenting:
        yearnings = ["No Renting happened this year"]
    
    # Select cars that rated
    global yrRating
    firstMonthday = f"{year}-01-01 00:00:00"
    
    end_month = f"{year}-12-31 23:59:59"
    
    yrTitle = f"{year} Yearly Report"
    
    Database()
    cursor.execute("""SELECT C.registrationNo,round(avg(ratings),1),count(ratings) as 'Number of Ratings' FROM Reviews R
                        INNER JOIN BookingDetails B on R.bookingID = B.bookingID
                        INNER JOIN CarDetails C ON C.carID = B.carID
                        GROUP by C.carID HAVING agencyID=? AND R.dateCreated >= ? AND R.dateCreated <= ?""",(userInfo,firstMonthday,end_month))
    yrRating = cursor.fetchall()
    conn.close()
    
    yearlyReport(ynotRent,yrejectBooking,ygotCancelled,ysuccess,yearnings)

def yearlyReport(ynotRent,yrejectBooking,ygotCancelled,ysuccess,yearnings): # Yearly Report

    labels = [f'Cars Not Rented:{ynotRent}', f'Cars Rejected:{yrejectBooking}', f'Bookings Cancelled:{ygotCancelled}', f'Cars Rented:{ysuccess}']
    slices = [ynotRent, yrejectBooking, ygotCancelled, ysuccess]
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
    
    # Create a figure for the pie 
    global yfig
    yfig = Figure(figsize=(3.9, 2.3), dpi=100, constrained_layout=True)
    ax = yfig.add_subplot(111)
    ax.pie(slices,labels=labels, colors=colors, autopct='%1.1f%%',wedgeprops={'edgecolor': 'white', 'linewidth': 2, 'width': 0.9},textprops={'fontsize': 8, 'color': 'black'})
    ax.legend(labels=labels, fontsize=7,loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=2)
    
    # Embed figure in tkinter canvas
    global yearcanvas
    yearcanvas = FigureCanvasTkAgg(yfig, master=yearStatsFrame)
    yearcanvas.draw()
    yearcanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    global ytoolbar
    ytoolbar = VerticalToolbar(yearcanvas, yearNavFrame)
    ytoolbar.update()

    # Add a yearly earnings label
    yearlyEarnings = ctk.CTkLabel(yearlyFrame, text=f"RM {yearnings}", width=100, anchor="center", font=("Tw Cen MT Condensed Extra Bold", 16), text_color="#000000")
    yearlyEarnings.place(x=160,y=300)


# Custom function to reconfigure the toolbar layout
class VerticalToolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Reconfigure the toolbar to stack buttons vertically
        for child in self.winfo_children():
            child.pack_forget()  # Remove the default layout
            child.pack(side=tkinter.TOP, fill=tkinter.Y, expand=True)  # Stack vertically