from pathlib import Path
from PIL import Image
from tkinter import Toplevel, messagebox, ttk
from MainCar2U_UserInfo import get_user_info,set_user_info
from tkcalendar import Calendar
from datetime import datetime,date
from calendar import monthrange
import pandas as pd
import customtkinter as ctk 
import pywinstyles
import sqlite3

# Set up the asset path
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Admin-Home")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def Database(): #creating connection to database and creating table
    global conn, cursor
    conn = sqlite3.connect("car2u.db")
    # Enable access to columns by name
    cursor = conn.cursor()

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
def open_history(current_window, list_callback):
    current_window.destroy()  # Close the signup window
    list_callback()

# Function to handle profile button click
def open_profile(current_window, profile_callback):
    current_window.destroy()  # Close the signup window
    profile_callback()

# Function to handle car details button click
def open_Cdetail(current_window, detail_callback):
    current_window.destroy()  # Close the signup window
    detail_callback()

# Function to handle bookings button click
def open_bookings(current_window, booking_callback):
    current_window.destroy()  # Close the signup window
    booking_callback()

def accManage(current_window, login_callback,profile_callback):
    global pfpState, droptabFrame

    if pfpState == 1:
        droptabFrame = ctk.CTkFrame(current_window,width=160,height=170, bg_color="#E6F6FF",fg_color="#E6F6FF")
        droptabFrame.place(x=16, y=413)

        if userinfo == "":
            droptabFrame.configure(height=57)
            logoin = ctk.CTkButton(master=droptabFrame, text="Log In", text_color="#000000", fg_color=("#E6F6FF","#D9D9D9"), 
                                    bg_color="#E6F6FF", font=("SegoeUI Bold", 20), command=lambda:open_login(current_window, login_callback))
            logoin.place(x=30,y=13)

        else:
            myAcc = ctk.CTkButton(master=droptabFrame, text="My Account", text_color="#000000", fg_color=("#E6F6FF","#D9D9D9"), anchor='center', width=110,
                                        bg_color="#E6F6FF", font=("SegoeUI Bold", 20), command=lambda:open_profile(current_window, profile_callback))
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

# Function to support tkcalendar view
def refresh_CalendarEvent():
    try:
        Database()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""SELECT pickupDate,dropoffDate
                            FROM BookingDetails B 
                            INNER JOIN CarDetails C ON B.carID = C.carID
                            WHERE agencyID = ?""",(userinfo,))
        calendarData = cursor.fetchall()

        for row in calendarData:
            start_date = row[0]
            end_date = row[1]

            date_range = pd.date_range(start=start_date, end=end_date)
            for date in date_range:
                task_calendar.calevent_create(date, "Booking(s)","reminder")
                task_calendar.tag_config('reminder', background='#85BCDA', foreground='white')

    except sqlite3.Error as e:
        messagebox.showerror("Error", "Error occurred during registration: {}".format(e))
    finally:
        conn.close()

def select_calendar(event):
    global calendarTreeview
    for row in calendarTreeview.get_children():
        calendarTreeview.delete(row)
    for widget in cTaskFrame.winfo_children():
        if isinstance(widget, ctk.CTkLabel):
            widget.destroy()
    
    global selected_date
    selected_date = task_calendar.get_date()
    setDate = ctk.CTkLabel(cTaskFrame, text=selected_date, anchor='center', width=250, height=28, font=("Segoe UI", 20))
    setDate.place(x=5, y=8)
    selected_month = task_calendar.get_displayed_month()

    # Filter month and year from selection
    start_month = f"{selected_month[1]}-{selected_month[0]:02d}-01"

    # Find last date of the month
    last_day = monthrange(selected_month[1],selected_month[0])
    end_month = f"{selected_month[1]}-{selected_month[0]:02d}-{last_day[1]:02d}"

    try:
        Database()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""SELECT C.registrationNo, pickupDate,pickupLocation,pickupTime,dropoffDate,dropoffLocation,dropoffTime,bookingID
                            FROM BookingDetails B 
                                INNER JOIN CarDetails C ON B.carID = C.carID
                                WHERE agencyID = ? AND ((pickupDate >= ? AND pickupDate <= ?) or (dropoffDate >= ? AND dropoffDate <= ?))""",(userinfo,start_month,end_month,start_month,end_month))
        fetchData = cursor.fetchall()

        if not fetchData:
            calendarTreeview.insert('', '0', 'noBooking', text ='No Bookings Today')

        i=0
        for row in fetchData:
            global carNo,start_date,pickLocate,pickTime,end_date,dropLocate,dropTime,date_range
            carNo = row[0]
            start_date = row[1]
            pickDate = row[1]
            pickLocate = row[2]
            pickTime = row[3]
            end_date = row[4]
            dropDate = row[4]
            dropLocate = row[5]
            dropTime = row[6]
            bookingID = row[7]

            onRent_content = f"Pick-Up Time (Client) : {pickTime} || Drop-Off Time (Client) : {dropTime}\nLocation : {pickLocate}\t\t"
            pickdate_content = f"Time : {pickTime} || Location : {pickLocate}\t\t"
            dropdate_content = f"Time : {dropTime} || Location : {dropLocate}\t\t"
            
            # checking if date selected is within the period
            start_date = pd.Timestamp(start_date)
            end_date = pd.Timestamp(end_date)
            date_range = pd.date_range(start=start_date, end=end_date)
            
            if selected_date == pickDate:
                if not calendarTreeview.exists('o2'):
                    calendarTreeview.insert('', '1', 'o2', text ='Car Pick-Up')
                carNoKey = carNo+"pick"
                if not calendarTreeview.exists(carNoKey):
                    calendarTreeview.insert('', i, carNoKey, text = carNo) # for pickup
                calendarTreeview.insert(carNoKey, 'end', bookingID, text = onRent_content)
                calendarTreeview.move(carNoKey, 'o2', 'end')
                i+=1
            elif selected_date == dropDate:
                if not calendarTreeview.exists('o3'):
                    calendarTreeview.insert('', '2', 'o3', text ='Car Drop-Off')
                carNoKey = carNo+"drop"
                if not calendarTreeview.exists(carNoKey):
                    calendarTreeview.insert('', i, carNoKey, text = carNo) # for dropoff
                calendarTreeview.insert(carNoKey, 'end', bookingID, text = pickdate_content)
                calendarTreeview.move(carNoKey, 'o3', 'end')
                i+=1
            elif selected_date in date_range: # Check if the selected date is within the booking period
                if not calendarTreeview.exists('o1'):
                    calendarTreeview.insert('', '0', 'o1', text ='On Rent')
                carNoKey = carNo+"renting"
                if not calendarTreeview.exists(carNoKey):
                    calendarTreeview.insert('', i, carNoKey, text = carNo) # Rejected
                calendarTreeview.insert(carNoKey, 'end', bookingID, text = dropdate_content)
                calendarTreeview.move(carNoKey, 'o1', 'end')
                i+=1

    except sqlite3.Error as e:
        messagebox.showerror("Error", "Error occurred during registration: {}".format(e))
    finally:
        conn.close()
    

def adminHome(login_callback,detail_callback,booking_callback,profile_callback):
    # Create the main application window
    global adminHomeFrame
    adminHomeFrame = Toplevel()
    adminHomeFrame.title("Login")
    adminHomeFrame.geometry("1280x720")
    adminHomeFrame.resizable(False, False)
    adminHomeFrame.config(bg="white")

    bg_img = ctk.CTkImage(Image.open(relative_to_assets("admin_bg.png")),size=(1280,720))
    bg_label = ctk.CTkLabel(adminHomeFrame, image=bg_img,text="")
    bg_label.place(x=0, y=0)

    # Linking user data
    global userinfo
    userinfo = get_user_info()
    print(f"Home: {userinfo}")
    Database()
    cursor.execute("""SELECT agencyName FROM RentalAgency WHERE agencyID = ?""",(userinfo,))
    agencyName = cursor.fetchone()[0]
    conn.close()
    print(agencyName)

    # Navigation Tab
    nav_img = ctk.CTkImage(Image.open(relative_to_assets("nav.png")),size=(200,720))
    nav_label = ctk.CTkLabel(adminHomeFrame, image=nav_img, text="")
    nav_label.place(x=0, y=0)

    logo_img = ctk.CTkImage(Image.open(relative_to_assets("Logo.png")),size=(150,60))
    logo_label = ctk.CTkLabel(adminHomeFrame, image=logo_img, text="", bg_color="#F47749", width=95, height=50)
    logo_label.place(x=22, y=10)
    pywinstyles.set_opacity(logo_label,color="#F47749")
    
    global pfpState
    pfpState = 1
    pfp_img = ctk.CTkImage(Image.open(relative_to_assets("image_4.png")),size=(100,100))
    pfp_label = ctk.CTkButton(adminHomeFrame, image=pfp_img, text="", bg_color="#FE453B", fg_color="#FE453B",
                              width=40, height=40, command=lambda:accManage(adminHomeFrame,login_callback,profile_callback))
    pfp_label.place(x=41, y=590)
    pywinstyles.set_opacity(pfp_label,color="#FE453B")

    # Relocate buttons
    home_button = ctk.CTkButton(master=adminHomeFrame, text="Home", width=120, fg_color=("#F95C41","#FA5740"), bg_color="#FA5740", 
                                text_color="#FFF6F6", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_home())
    home_button.place(x=22, y=100)
    pywinstyles.set_opacity(home_button,color="#FA5740")

    booking_button = ctk.CTkButton(master=adminHomeFrame, text="Bookings", width=120, fg_color=("#FA5740","#FB543F"), bg_color="#FB543F", 
                                      text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda:open_bookings(adminHomeFrame,booking_callback))
    booking_button.place(x=22, y=165)
    pywinstyles.set_opacity(booking_button,color="#FB543F")

    inventory_button = ctk.CTkButton(master=adminHomeFrame, text="Inventory", width=120, fg_color=("#FB543F","#FC503E"), bg_color="#FC503E", 
                                      text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), 
                                      command=lambda: open_Cdetail(adminHomeFrame, detail_callback))
    inventory_button.place(x=22, y=230)
    pywinstyles.set_opacity(inventory_button,color="#FC503E")

    chat_button = ctk.CTkButton(master=adminHomeFrame, text="Chat", width=120, fg_color=("#FC503E","#FC4D3D"), bg_color="#FC4D3D", 
                                    text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: print("About Us clicked"))
    chat_button.place(x=22, y=295)
    pywinstyles.set_opacity(chat_button,color="#FC4D3D")

    rentalName = agencyName
    name = ctk.CTkLabel(adminHomeFrame, text=rentalName, font=("Segoe UI",36), fg_color="#5EC5FF", bg_color="#5EC5FF")
    name.place(x=249, y=20)
    pywinstyles.set_opacity(name,color="#5EC5FF")

    taskFrame = ctk.CTkFrame(adminHomeFrame, width=400,height=300,bg_color="#FFFFFF")
    taskFrame.place(x=220,y=80)
    taskFrame.pack_propagate(False) # Prevent the frame from shrinking to fit the calendar

    global task_calendar
    task_calendar = Calendar(taskFrame,date_pattern='y-mm-dd',showothermonthdays=False)
    task_calendar.pack(fill="both", expand=True)
    refresh_CalendarEvent()
    task_calendar.selection_set(date(int(datetime.now().year), int(datetime.now().month), (datetime.now().day)))
    task_calendar.bind("<<Enter>>",select_calendar)
    task_calendar.bind("<<CalendarSelected>>",select_calendar)
    
    global cTaskFrame
    cTaskFrame = ctk.CTkFrame(adminHomeFrame, width=260, height=300, fg_color="#FFFFFF", border_width=2, border_color="#000000")
    cTaskFrame.place(x=620,y=80)

    ##Treeview widget data
    global calendarTreeview
    calendarTreeview = ttk.Treeview(cTaskFrame, show="tree")
    calendarTreeview.place(x=5,y=45,width=250,height=250,bordermode='ignore')
    calendarTreeview.column('#0',width=500, stretch=True)

    h_scrollbar = ttk.Scrollbar(cTaskFrame, orient="horizontal", command=calendarTreeview.xview)
    calendarTreeview.configure(xscrollcommand=h_scrollbar.set)
    h_scrollbar.place(x=5,y=280, width=250, height=10)


    global notifFrame
    notifFrame = ctk.CTkFrame(adminHomeFrame, width=325, height=245,fg_color="#FFFFFF", bg_color="#DEF3FF", border_width=2, border_color="#000000")
    notifFrame.place(x=930,y=80)
    notifs()

    inventoryFrame = ctk.CTkFrame(adminHomeFrame, width=1020, height=300, fg_color="#2F59C1")
    inventoryFrame.place(x=220, y=400)
    inventorybg = ctk.CTkLabel(inventoryFrame,text="", bg_color="#2F59C1", fg_color="#2F59C1", width=1020, height=300, corner_radius=20)
    inventorybg.place(x=0,y=0)

    invenTitle = ctk.CTkLabel(inventoryFrame, text="Inventory", bg_color="#85BCDA", text_color="#CBECFF", font=("Segoe UI Bold",24))
    invenTitle.place(x=40,y=5)
    pywinstyles.set_opacity(invenTitle,color="#85BCDA")
    
    inven = ctk.CTkFrame(inventoryFrame, width=1000, height=200)
    inven.place(x=30,y=40)
    
    # Treeview for displaying saved data
    global treeview
    columns = ('registration_number', 'model', 'colour', 'fuel_type', 'seating_capacity', 'transmission_type', 'price_rate')
    treeview = ttk.Treeview(inven, columns=columns, show='headings', height=7)

    # Define the headings
    for col in columns:
        treeview.heading(col, text=col.capitalize())
        treeview.column(col, anchor='center', width=120)  # Adjust width as needed

    # Create scrollbars
    v_scrollbar = ttk.Scrollbar(inven, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=v_scrollbar.set)

    # Position the Treeview and scrollbars using grid
    treeview.grid(row=0, column=0, sticky="nsew")
    v_scrollbar.grid(row=0, column=1, sticky="ns")

    # Configure grid layout to make the treeview expand with the frame
    inven.grid_rowconfigure(0, weight=1)
    inven.grid_columnconfigure(0, weight=1)
    refresh_treeview()

    viewMore = ctk.CTkButton(inventoryFrame, text="View More", bg_color="#85BCDA", fg_color="#FED000", text_color="#000000", font=("Segoe UI",16), 
                             width=100, height=35, corner_radius=50)
    viewMore.place(x=885,y=240)
    pywinstyles.set_opacity(viewMore,color="#85BCDA")


# Function to refresh treeview
def refresh_treeview():
    for row in treeview.get_children():
        treeview.delete(row)

    Database()
    cursor.execute("""SELECT registrationNo,model,colour,fuelType,seatingCapacity,transmissionType,price 
                    FROM CarDetails WHERE agencyID = ?""", (userinfo,))
    result = cursor.fetchall()
    conn.commit()
    conn.close()

    for row in result:
        treeview.insert("", "end", values=row)

def notifs():
    for widgets in notifFrame.winfo_children():
        if isinstance(widgets, ctk.CTkLabel):
            widgets.destroy()
    
    notifTitle = ctk.CTkLabel(notifFrame, text="Notification", font=("Segoe UI",24,"underline"))
    notifTitle.place(x=35,y=5)
    statusTitle = ctk.CTkLabel(notifFrame, text="Status", font=("Segoe UI",24,"underline"))
    statusTitle.place(x=235,y=5)

    notif1 = ctk.CTkLabel(notifFrame, text="Pending Booking Request", font=("Segoe UI",16))
    notif1.place(x=12,y=40)
    notif2 = ctk.CTkLabel(notifFrame, text="Cars Booked", font=("Segoe UI",16))
    notif2.place(x=12,y=75)
    notif3 = ctk.CTkLabel(notifFrame, text="Cars On Rent", font=("Segoe UI",16))
    notif3.place(x=12,y=110)

    try:
        Database()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""SELECT count(bookingID) as Pendings from BookingDetails b
                            INNER JOIN CarDetails r ON b.carID = r.carID
                            WHERE bookingStatus = 'Pending' AND agencyID = ?""",(userinfo,))
        result = cursor.fetchone()

        for row in result:
            if result == "" or result is None:
                status1 = ctk.CTkLabel(notifFrame, text="Done", width=64, justify="center", font=("Segoe UI",16))
                status1.place(x=230,y=40)
            else:
                status1 = ctk.CTkLabel(notifFrame, text=f"Pending({row})", width=64, justify="center", font=("Segoe UI",16))
                status1.place(x=230,y=40)

    except sqlite3.Error as e:
        messagebox.showerror("Error", "Error occurred during registration: {}".format(e))
    finally:
        conn.close()
    
    try:
        Database()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""SELECT count(bookingID) as Booked from BookingDetails b
                            INNER JOIN CarDetails r ON b.carID = r.carID
                            WHERE bookingStatus = 'Approved' AND agencyID = ?""",(userinfo,))
        result = cursor.fetchone()

        
        for row in result:
            if result == "" or result is None:
                status2 = ctk.CTkLabel(notifFrame, text="Done", width=64, justify="center", font=("Segoe UI",16))
                status2.place(x=230,y=75)
            else:
                status2 = ctk.CTkLabel(notifFrame, text=f"Pending ({row})", width=64, justify="center", font=("Segoe UI",16))
                status2.place(x=230,y=75)

    except sqlite3.Error as e:
        messagebox.showerror("Error", "Error occurred during registration: {}".format(e))
    finally:
        conn.close()

    try:
        Database()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""SELECT count(bookingID) as OnRent from BookingDetails b
                            INNER JOIN CarDetails r ON b.carID = r.carID
                            WHERE bookingStatus = 'On Rent' AND agencyID = ?""",(userinfo,))
        result = cursor.fetchone()

        for row in result:
            if result == "" or result is None:
                status3 = ctk.CTkLabel(notifFrame, text="Done", width=64, justify="center", font=("Segoe UI",16))
                status3.place(x=230,y=110)
            else:
                status3 = ctk.CTkLabel(notifFrame, text=f"Pending ({row})", width=64, justify="center", font=("Segoe UI",16))
                status3.place(x=230,y=110)

    except sqlite3.Error as e:
        messagebox.showerror("Error", "Error occurred during registration: {}".format(e))
    finally:
        conn.close()
    