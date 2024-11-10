import tkinter as tk
import customtkinter as ctk
import pywinstyles
import sqlite3
from tkinter import ttk, messagebox, Toplevel
from PIL import Image, ImageTk
from MainCar2U_UserInfo import get_user_info,set_user_info
from datetime import datetime

# Function to handle login button click
def open_login(current_window, login_callback):
    current_window.destroy()  # Close the signup window
    userInfo = ""
    set_user_info(userInfo)
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
def open_profile(current_window, profile_callback):
    current_window.destroy()  # Close the signup window
    profile_callback()

# Function to handle about us button click
def open_aboutUs(current_window, about_callback):
    current_window.destroy()  # Close the signup window
    about_callback()

# Function to handle about us button click
def open_payment(current_window, payment_callback):
    current_window.destroy()  # Close the signup window
    payment_callback()

def accManage(current_window, login_callback,profile_callback):
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

            history = ctk.CTkButton(master=droptabFrame, text="History", text_color="#000000", fg_color=("#E6F6FF","#D9D9D9"), 
                                        bg_color="#E6F6FF", font=("SegoeUI Bold", 20))
            history.place(x=30,y=80)

            setting = ctk.CTkButton(master=droptabFrame, text="Setting", text_color="#000000", fg_color=("#E6F6FF","#D9D9D9"), 
                                        bg_color="#E6F6FF", font=("SegoeUI Bold", 20))
            setting.place(x=30,y=137)

            logout = ctk.CTkButton(master=droptabFrame, text="Log Out", text_color="#000000", fg_color=("#E6F6FF","#D9D9D9"), 
                                        bg_color="#E6F6FF", font=("SegoeUI Bold", 20), command=lambda:open_login(current_window, login_callback))
            logout.place(x=30,y=184)
        pfpState = 0
    else:
        droptabFrame.destroy()
        pfpState = 1

# Connect to the database
conn = sqlite3.connect('CAR2U.db')
cursor = conn.cursor()

# Verify if BookingDetails exists
#cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#tables = cursor.fetchall()
#print("Tables in database:", tables)

# Function to format date as "21August2024"
def format_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%d %B %Y")

# Function to format time as "10.00am"
def format_time(time_str):
    time_obj = datetime.strptime(time_str, "%H:%M:%S")
    return time_obj.strftime("%I.%M%p").lower()

# Function to populate Treeview
def populate_treeview():
    for row in tree.get_children():
        tree.delete(row)

    # Query to get necessary data from BookingDetails and CarDetails tables
    cursor.execute('''
        SELECT CarDetails.registrationNo, CarDetails.model, 
               BookingDetails.dateCreated, BookingDetails.pickupDate, 
               BookingDetails.dropoffDate, BookingDetails.bookingStatus, BookingDetails.bookingID
        FROM BookingDetails
        JOIN CarDetails ON BookingDetails.carID = CarDetails.carID
    ''')

    # Insert data into Treeview
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

# Function to set the rating based on clicked star
def set_rating(rating):
    selected_rating.set(rating)
    update_stars(rating)

# Function to update star images based on rating
def update_stars(rating):
    for i in range(1, 6):
        star_label = star_labels[i - 1]
        if i <= rating:
            star_label.config(image=yellow_star_img)
        else:
            star_label.config(image=black_star_img)

# Function to upload the rating and review
def upload_review():
    rating = selected_rating.get()
    review_text = review_entry.get("1.0", "end-1c")
    bookingID = selected_bookingID.get()
    car_id = selected_carID.get()  # Use selected carID
    user_id = selected_userID.get()  # Use selected userID
    
    if rating == 0:
        messagebox.showwarning("Warning", "Please select a rating.")
        return
    
    cursor.execute('''
        INSERT INTO Reviews (ratings, statement, userID, carID, bookingID)
        VALUES (?, ?, ?, ?, ?)
    ''', (rating, review_text, user_id, car_id, bookingID))
    
    conn.commit()
    messagebox.showinfo("Success", "Review uploaded successfully.")
    selected_rating.set(0)
    update_stars(0)
    review_entry.delete("1.0", "end")

# Function to display detailed info on row selection
def on_row_selected(event):
    selected_row = tree.focus()
    if selected_row:
        # Get bookingID of the selected row
        bookingID = tree.item(selected_row)['values'][6]
        selected_bookingID.set(bookingID)

        # Query to get additional details for the selected bookingID
        cursor.execute('''
            SELECT CarDetails.registrationNo, RentalAgency.agencyName, BookingDetails.bookingStatus,
                   BookingDetails.pickupDate, BookingDetails.pickupTime, 
                   BookingDetails.pickupLocation, BookingDetails.dropoffDate, 
                   BookingDetails.dropoffTime, BookingDetails.dropoffLocation,
                   CarDetails.carID, BookingDetails.userID
            FROM BookingDetails
            JOIN CarDetails ON BookingDetails.carID = CarDetails.carID
            JOIN RentalAgency ON CarDetails.agencyID = RentalAgency.agencyID
            WHERE BookingDetails.bookingID = ?
        ''', (bookingID,))
        
        details = cursor.fetchone()
        if details:
            # Format dates and times
            pickup_date_formatted = format_date(details[3])
            pickup_time_formatted = format_time(details[4])
            dropoff_date_formatted = format_date(details[6])
            dropoff_time_formatted = format_time(details[7])

            # Display the detailed info
            registrationNo_label.config(text=f"{details[0]}")
            agency_label.config(text=f"{details[1]}")
            status_label.config(text=f"{details[2]}")
            pickup_date_label.config(text=f"{pickup_date_formatted}")
            pickup_time_label.config(text=f"{pickup_time_formatted}")
            pickup_location_label.config(text=f"{details[5]}")
            dropoff_date_label.config(text=f"{dropoff_date_formatted}")
            dropoff_time_label.config(text=f"{dropoff_time_formatted}")
            dropoff_location_label.config(text=f"{details[8]}")

            # Set the selected carID and userID
            selected_carID.set(details[9])
            selected_userID.set(details[10])

def reviewgui(login_callback,home_callback,list_callback,profile_callback,about_callback,payment_callback):
    # Create main window
    reviewFrame = Toplevel()
    reviewFrame.title("Your Bookings")
    reviewFrame.geometry("1280x720")
    reviewFrame.resizable(False, False)
    
    global userInfo
    userInfo = get_user_info()

    # Load the background image
    bg_image_path = r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Cust-Review\Your Bookings.png"
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    """
    # Create a canvas to hold the background image
    canvas = tk.Canvas(reviewFrame, width=bg_image.width, height=bg_image.height)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    """
    # Navigation Tab
    nav_img = ctk.CTkImage(Image.open(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Cust-Review\image_2.png"),size=(1280,60))
    nav_label = ctk.CTkLabel(reviewFrame, image=nav_img, text="", width=1280, height=60)
    nav_label.place(x=0, y=0)

    logo_img = ctk.CTkImage(Image.open(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Cust-Review\logo.png"),size=(75,40))
    logo_label = ctk.CTkLabel(reviewFrame, image=logo_img, text="", bg_color="#F47749", width=95, height=50)
    logo_label.place(x=5, y=5)
    pywinstyles.set_opacity(logo_label,color="#F47749")
    
    pfp_img = ctk.CTkImage(Image.open(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Cust-Review\image_1.png"),size=(40,40))
    pfp_label = ctk.CTkButton(reviewFrame, image=pfp_img, text="", bg_color="#F47749", fg_color="#F47749",
                              width=40, height=40, command=lambda:accManage(reviewFrame,login_callback,profile_callback))
    pfp_label.place(x=1203, y=5)
    pywinstyles.set_opacity(pfp_label,color="#F47749")

    # Relocate buttons
    home_button = ctk.CTkButton(master=reviewFrame, text="Home", width=120, fg_color=("#F95C41","#FA5740"), bg_color="#FA5740", 
                                text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_home(reviewFrame,home_callback))
    home_button.place(x=667, y=14)
    pywinstyles.set_opacity(home_button,color="#FA5740")

    selections_button = ctk.CTkButton(master=reviewFrame, text="Selections", width=120, fg_color=("#FA5740","#FB543F"), bg_color="#FB543F", 
                                      text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda:open_listing(reviewFrame,list_callback))
    selections_button.place(x=783, y=14)
    pywinstyles.set_opacity(selections_button,color="#FB543F")

    contact_us_button = ctk.CTkButton(master=reviewFrame, text="Contact Us", width=120, fg_color=("#FB543F","#FC503E"), bg_color="#FC503E", 
                                      text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: print("Contact Us clicked"))
    contact_us_button.place(x=930, y=14)
    pywinstyles.set_opacity(contact_us_button,color="#FC503E")

    about_us_button = ctk.CTkButton(master=reviewFrame, text="About Us", width=120, fg_color=("#FC503E","#FC4D3D"), bg_color="#FC4D3D", 
                                    text_color="#FFF6F6", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_aboutUs(reviewFrame,about_callback))
    about_us_button.place(x=1075, y=14)
    pywinstyles.set_opacity(about_us_button,color="#FC4D3D")

    # Create a canvas to hold the background image
    canvas = tk.Canvas(reviewFrame, width=bg_image.width, height=bg_image.height)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Set up the Treeview on the canvas
    global tree
    tree = ttk.Treeview(canvas, columns=("Reg No", "Model", "Date Created", "Pickup Date", "Drop-off Date", "Status"), show="headings")

    # Configure headings and column widths
    tree.heading("Reg No", text="Reg No")
    tree.column("Reg No", width=100)  # Adjust width as needed

    tree.heading("Model", text="Model")
    tree.column("Model", width=120)  # Adjust width as needed

    tree.heading("Date Created", text="Date Created")
    tree.column("Date Created", width=120)  # Adjust width as needed

    tree.heading("Pickup Date", text="Pickup Date")
    tree.column("Pickup Date", width=120)  # Adjust width as needed

    tree.heading("Drop-off Date", text="Drop-off Date")
    tree.column("Drop-off Date", width=120)  # Adjust width as needed

    tree.heading("Status", text="Status")
    tree.column("Status", width=100)  # Adjust width as needed

    # Place the Treeview on the canvas
    tree.place(x=70, y=192, width=700, height=170)  # Adjust x, y, width, and height as needed

    # Bind the row selection event
    tree.bind("<ButtonRelease-1>", on_row_selected)

    # Variables to store rating and bookingID
    global selected_rating,selected_bookingID,selected_carID,selected_userID
    selected_rating = tk.IntVar()
    selected_bookingID = tk.IntVar()
    selected_carID = tk.IntVar()  # New variable for carID
    selected_userID = tk.IntVar()  # New variable for userID

    # Load star images
    global black_star_img,yellow_star_img
    black_star_img = ImageTk.PhotoImage(Image.open(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Cust-Review\black star.png").resize((32, 32)))
    yellow_star_img = ImageTk.PhotoImage(Image.open(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Cust-Review\yellow star.png").resize((32, 32)))

    # Star labels for rating
    global star_labels
    star_labels = []
    for i in range(5):
        star_label = tk.Label(canvas, image=black_star_img, cursor="hand2", bg="#D9D9D9")
        star_label.place(x=842 + (i * 48), y=381)
        star_label.bind("<Button-1>", lambda e, rating=i+1: set_rating(rating))
        star_labels.append(star_label)

    # Text box for review
    global review_entry
    review_entry = tk.Text(canvas, width=39, height=9, bg="white")
    review_entry.place(x=845, y=426)

    # Upload button
    upload_button = tk.Button(reviewFrame, text="UPLOAD", bg="#FF865A", command=lambda:upload_review, bd=0, font=("Arial", 14, "bold"), width=8)
    upload_button.place(x=952, y=614)

    # Labels to display additional details, placed on the canvas
    global registrationNo_label, agency_label, status_label,pickup_date_label,pickup_time_label,pickup_location_label,dropoff_date_label,dropoff_time_label,dropoff_location_label

    registrationNo_label = tk.Label(canvas, text="", bg="#D9D9D9", font= ('Arial', 17))
    registrationNo_label.place(x=170, y=463)
    agency_label = tk.Label(canvas, text="", bg="#D9D9D9", font= ('Arial', 17))
    agency_label.place(x=170, y=530)
    status_label = tk.Label(canvas, text="", bg="#D9D9D9", font= ('Arial', 17))
    status_label.place(x=170, y=595)
    pickup_date_label = tk.Label(canvas, text="", bg="#D9D9D9", font= ('Arial', 8))
    pickup_date_label.place(x=606, y=513)
    pickup_time_label = tk.Label(canvas, text="", bg="#D9D9D9", font= ('Arial', 8))
    pickup_time_label.place(x=535, y=513)
    pickup_location_label = tk.Label(canvas, text="", bg="#D9D9D9", font= ('Arial', 8))
    pickup_location_label.place(x=535, y=484)
    dropoff_date_label = tk.Label(canvas, text="", bg="#D9D9D9", font= ('Arial', 8))
    dropoff_date_label.place(x=606, y=612)
    dropoff_time_label = tk.Label(canvas, text="", bg="#D9D9D9", font= ('Arial', 8))
    dropoff_time_label.place(x=535, y=612)
    dropoff_location_label = tk.Label(canvas, text="", bg="#D9D9D9", font= ('Arial', 8))
    dropoff_location_label.place(x=535, y=583)

    # Populate the Treeview with data
    populate_treeview()

    paybttn = ctk.CTkButton(reviewFrame,text="Payment",command=lambda:open_payment(reviewFrame,payment_callback))
    paybttn.place(x=700,y=650)