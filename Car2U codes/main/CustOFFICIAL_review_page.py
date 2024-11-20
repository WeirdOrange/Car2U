import tkinter as tk
import customtkinter as ctk
import pywinstyles
import sqlite3
import easygui
from tkinter import ttk, messagebox, Toplevel
from pathlib import Path
from PIL import Image, ImageTk
from MainCar2U_UserInfo import get_user_info,set_user_info,set_BookingID
from datetime import datetime


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Cust-Review")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

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
def open_payment(current_window, payment_callback,bookingID):
    messagebox.showinfo("Payment", "Redirecting to payment...")
    set_BookingID(bookingID)
    current_window.destroy()  # Close the signup window
    payment_callback()

# Function to handle profile button click
def open_review():
    messagebox.showinfo("Oops.","You are on the profile page")

# Function to handle chats button click
def open_chat(current_window, chat_callback):
    current_window.destroy()  # Close the window
    chat_callback()

def accManage(current_window, login_callback,profile_callback):
    global pfpState, droptabFrame

    if pfpState == 1:
        droptabFrame = ctk.CTkFrame(current_window,width=190,height=240, bg_color="#E6F6FF",fg_color="#E6F6FF")
        droptabFrame.place(x=1090, y=60)

        myAcc = ctk.CTkButton(master=droptabFrame, text="My Account", text_color="#000000", fg_color=("#E6F6FF","#D9D9D9"), 
                                    bg_color="#E6F6FF", font=("SegoeUI Bold", 20), command=lambda:open_profile(current_window, profile_callback))
        myAcc.place(x=30,y=23)

        history = ctk.CTkButton(master=droptabFrame, text="My Bookings", text_color="#000000", fg_color=("#E6F6FF","#D9D9D9"), 
                                    bg_color="#E6F6FF", font=("SegoeUI Bold", 20), command=lambda:open_review())
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

def Database():
    # Connect to the database
    global conn,cursor
    conn = sqlite3.connect('CAR2U.db')
    cursor = conn.cursor()

# Verify if BookingDetails exists
#cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#tables = cursor.fetchall()
#print("Tables in database:", tables)

# Function to populate Treeview
def populate_treeview():
    for row in tree.get_children():
        tree.delete(row)

    try:
        Database()
        cursor.execute(''' SELECT CarDetails.registrationNo, CarDetails.model, 
                            BookingDetails.dateCreated, BookingDetails.pickupDate, 
                            BookingDetails.dropoffDate, BookingDetails.bookingStatus, BookingDetails.bookingID
                            FROM BookingDetails
                            JOIN CarDetails ON BookingDetails.carID = CarDetails.carID
                            WHERE userID = ? ORDER BY BookingDetails.pickupDate''', (userInfo,))
        result = cursor.fetchall()
        conn.commit()

        if result is not None:
            for row in result:
                tree.insert("", "end", values=row)
        else:
            tree.insert("","end", values=("No Data Yet", "No Data Yet", "No Data Yet", "No Data Yet", "No Data Yet", "No Data Yet"))
    
    except sqlite3.Error as e: 
        print("Error", "Error occurred during registration: {}".format(e))
    finally: 
        if conn:
            conn.close() 

# Function to set the rating based on clicked star
def set_rating(rating):
    selected_rating.set(rating)
    update_stars(rating)

# Function to update star images based on rating
def update_stars(rating):
    for i in range(1, 6):
        star_label = star_labels[i - 1]
        if i <= rating:
            star_label.configure(image=reviewFrame.yellow_star_img)
        else:
            star_label.configure(image=reviewFrame.black_star_img)

# Function to upload the rating and review
def upload_review():
    rating = selected_rating.get()
    review_text = review_entry.get("1.0", "end-1c")
    bookingID = selected_bookingID.get()
    car_id = selected_carID.get()  
    user_id = selected_userID.get()  

    if rating == 0:
        messagebox.showwarning("Warning", "Please select a rating.")
        return
    
    Database()
    cursor.execute('''
        INSERT INTO Reviews (ratings, statement, bookingID)
        VALUES (?, ?, ?)
    ''', (rating, review_text, bookingID))
    
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Review uploaded successfully.")
    selected_rating.set(0)
    update_stars(0)
    review_entry.delete("1.0", "end")

def cancel_Request():
    bookingID = selected_bookingID.get()
    while True:
        cancel = easygui.buttonbox("You clicked Cancel Request. Are you sure about this action?", "Options", 
                                    choices=["Cancel Booking Request", "Back"])
          
        if cancel == "Cancel Booking Request":
            Database()
            cursor.execute('''
                UPDATE BookingDetails
                SET bookingStatus = "Cancelled"
                WHERE bookingID = ?
            ''', (bookingID))
            
            conn.commit()
            conn.close()
            easygui.msgbox(f"Booking Request Terminated", "Your booking request has been cancelled.")
        elif cancel == "Back":
            break

# Function to display detailed info on row selection
def on_row_selected(payment_callback,chat_callback,event):
    for widget in defaultFrame.winfo_children():
        if isinstance(widget, (tk.Button,ctk.CTkImage,ctk.CTkLabel,ctk.CTkTextbox)):
            widget.destroy()

    selected_row = tree.focus()
    
    if selected_row:
        default_image_label.place_forget()  # Hide the default image
        bookingID = tree.item(selected_row)['values'][6]
        selected_bookingID.set(bookingID)

        Database()
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
        conn.close()
        if details:

            registrationNo_label.config(text=f"{details[0]}")
            agency_label.config(text=f"{details[1]}")
            status_label.config(text=f"{details[2]}")
            pickup_date_label.config(text=f"{details[3]}")
            pickup_time_label.config(text=f"{details[4]}")
            pickup_location_label.config(text=f"{details[5]}")
            dropoff_date_label.config(text=f"{details[6]}")
            dropoff_time_label.config(text=f"{details[7]}")
            dropoff_location_label.config(text=f"{details[8]}")

            selected_carID.set(details[9])
            selected_userID.set(details[10])

            defaultFrame.place(x=811,y=194)

            # Display "To Pay" image and "Pay Now" button if booking is approved
            if details[2] == "Approved": # To Pay
                # Force frame to update
                defaultFrame.update_idletasks()

                # "To pay" image and "Pay Now" button
                global pay_image_label
                pay_image = ctk.CTkImage(Image.open(relative_to_assets("To pay.png")), size=(377,464))
                pay_image_label = ctk.CTkLabel(defaultFrame, text="", image=pay_image, bg_color="#D9D9D9")

                global pay_button
                pay_button = tk.Button(defaultFrame, text="PAY NOW", bg="#FF865A", bd=0, font=("Arial Bold", 16), 
                                    fg="#000000", command=lambda: open_payment(reviewFrame, payment_callback,bookingID),)

                pay_image_label.place(x=0, y=0)
                pay_button.place(x=140, y=345)
                
            elif details[2] == "Pending": # Waiting for Approval
                # Force frame to update
                defaultFrame.update_idletasks()

                global pending_image_label
                pending_image = ctk.CTkImage(Image.open(relative_to_assets("Awaits.png")),size=(377,464))
                pending_image_label = ctk.CTkLabel(defaultFrame, text="", image=pending_image, bg_color="#D9D9D9")

                global contact_button
                contact_button = tk.Button(defaultFrame, text="Contact Renter", bg="#FFB195", font=("Arial Bold", 12), bd=0,
                                    fg="#000000", command=lambda: open_chat(reviewFrame, chat_callback))
                global cancel_button
                cancel_button = tk.Button(defaultFrame, text="Cancel Request", bg="#FF865A", font=("Arial Bold", 14), bd=0,
                                    fg="#000000", command=lambda: cancel_Request())
                
                pending_image_label.place(x=0, y=0)
                contact_button.place(x=126,y=347)
                cancel_button.place(x=110, y=400)
            else: # ALLOWED to Rate
                # Force frame to update
                defaultFrame.lift()
                defaultFrame.update_idletasks()
                
                global review_image_label
                review_image = ctk.CTkImage(Image.open(relative_to_assets("To Review.png")),size=(377,464))
                review_image_label = ctk.CTkLabel(defaultFrame, text="", image=review_image, bg_color="#D9D9D9")

                # Review entry and upload button
                global review_entry
                review_entry = ctk.CTkTextbox(defaultFrame, width=318, height=143, bg_color="white")

                global upload_button
                upload_button = ctk.CTkButton(defaultFrame, text="UPLOAD", bg_color="#FF865A", fg_color="#FF865A",
                                            command=lambda:upload_review(), font=("Arial Bold", 14))
                    
                # Star images
                reviewFrame.black_star_img = ctk.CTkImage(Image.open((relative_to_assets("black star.png"))).resize((32, 32)))
                reviewFrame.yellow_star_img = ctk.CTkImage(Image.open(relative_to_assets("yellow star.png")).resize((32, 32)))

                # Star labels
                global selected_rating, star_labels
                selected_rating = tk.IntVar()
                star_labels = []
                for i in range(5):
                    star_label = ctk.CTkLabel(defaultFrame, text="", image=reviewFrame.black_star_img, cursor="hand2", bg_color="#D9D9D9")
                    star_label.bind("<Button-1>", lambda e, rating=i+1: set_rating(rating))
                    star_labels.append(star_label)
                
                # Show review UI elements
                review_image_label.place(x=0,y=0)
                review_entry.place(x=33, y=232)
                upload_button.place(x=120, y=410)
                for i, star_label in enumerate(star_labels):
                    star_label.place(x=33 + (i * 48), y=188)
    else:
        default_image_label.place(x=70, y=192)  # Show default image if no row is selected

def reviewGUI(login_callback,home_callback,listing_callback,profile_callback,aboutUs_callback,payment_callback, chat_callback):
    # Create main window
    global reviewFrame
    reviewFrame = Toplevel()
    reviewFrame.title("Your Bookings")
    reviewFrame.geometry("1280x720")
    reviewFrame.resizable(False, False)

    global userInfo
    userInfo = get_user_info()
    print(f"Review : {userInfo}")

    # Background image
    bg_image_path = relative_to_assets("Your Bookings.png")
    bg_image = Image.open(bg_image_path).resize((1280, 720), Image.Resampling.LANCZOS)
    reviewFrame.bg_photo = ImageTk.PhotoImage(bg_image)
    background_label = tk.Label(reviewFrame, image=reviewFrame.bg_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Navigation Bar
    header = ctk.CTkFrame(reviewFrame, width=1280, height=60, fg_color="#FFFFFF")
    header.place(x=0, y=0)

    navbg_img = ctk.CTkImage(Image.open(relative_to_assets("nav.png")),size=(1280,60))
    navbg_label = ctk.CTkLabel(header, image=navbg_img, text="", width=1280, height=60)
    navbg_label.place(x=0, y=0)

    # Relocating buttons
    home_button = ctk.CTkButton(master=reviewFrame, text="Home", width=120, fg_color=("#F95C41","#FA5740"), bg_color="#FA5740", 
                                text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), 
                                command=lambda: open_home(reviewFrame, home_callback))
    home_button.place(x=627, y=14)
    pywinstyles.set_opacity(home_button,color="#FA5740")

    selections_button = ctk.CTkButton(master=reviewFrame, text="Selections", width=120, fg_color=("#FA5740","#FB543F"), bg_color="#FB543F", 
                                        text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), 
                                        command=lambda: open_listing(reviewFrame, listing_callback))
    selections_button.place(x=763, y=14)
    pywinstyles.set_opacity(selections_button,color="#FB543F")

    contact_us_button = ctk.CTkButton(master=reviewFrame, text="Contact Us", width=120, fg_color=("#FB543F","#FC503E"), bg_color="#FC503E", 
                                        text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), 
                                        command=lambda: open_chat(reviewFrame, chat_callback))
    contact_us_button.place(x=910, y=14)
    pywinstyles.set_opacity(contact_us_button,color="#FC503E")

    about_us_button = ctk.CTkButton(master=reviewFrame, text="About Us", width=120, fg_color=("#FC503E","#FC4D3D"), bg_color="#FC4D3D", 
                                    text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), 
                                    command=lambda: open_aboutUs(reviewFrame, aboutUs_callback))
    about_us_button.place(x=1055, y=14)
    pywinstyles.set_opacity(about_us_button,color="#FC4D3D")

    logo_img = ctk.CTkImage(Image.open(relative_to_assets("logo.png")),size=(75,40))
    logo_label = ctk.CTkLabel(reviewFrame, image=logo_img, text="", bg_color="#F47749", width=95, height=50)
    logo_label.place(x=5, y=5)
    pywinstyles.set_opacity(logo_label,color="#F47749")

    global pfpState
    pfpState = 1
    pfp_img = ctk.CTkImage(Image.open(relative_to_assets("image_1.png")),size=(40,40))
    pfp_label = ctk.CTkButton(reviewFrame, image=pfp_img, text="", bg_color="#F47749", fg_color="#F47749",
                                width=40, height=40, command=lambda: accManage(reviewFrame, login_callback,profile_callback))
    pfp_label.place(x=1180, y=5)
    pywinstyles.set_opacity(pfp_label,color="#F47749")

    # Treeview setup
    global tree
    tree = ttk.Treeview(reviewFrame, columns=("Reg No", "Model", "Date Created", "Pickup Date", "Drop-off Date", "Status"), show="headings")
    tree.heading("Reg No", text="Reg No")
    tree.column("Reg No", width=100)
    tree.heading("Model", text="Model")
    tree.column("Model", width=120)
    tree.heading("Date Created", text="Date Created")
    tree.column("Date Created", width=120)
    tree.heading("Pickup Date", text="Pickup Date")
    tree.column("Pickup Date", width=120)
    tree.heading("Drop-off Date", text="Drop-off Date")
    tree.column("Drop-off Date", width=120)
    tree.heading("Status", text="Status")
    tree.column("Status", width=100)
    tree.place(x=70, y=192, width=700, height=170)
    tree.bind("<ButtonRelease-1>",lambda event: on_row_selected(payment_callback,chat_callback,event))

    # Load and display default image if no row is selected
    global default_image_label, defaultFrame
    default_image_path = relative_to_assets("review n payment frame.png")
    reviewFrame.default_image = ImageTk.PhotoImage(Image.open(default_image_path).resize((350, 450), Image.Resampling.LANCZOS))
    default_image_label = tk.Label(reviewFrame, image=reviewFrame.default_image, bg="#D9D9D9")

    # Place the default image initially
    default_image_label.place(x=818, y=198)

    defaultFrame = ctk.CTkFrame(reviewFrame, width=377, height=464, corner_radius=20)
    defaultFrame.place(x=811,y=194)

    # Labels for booking details
    global registrationNo_label,agency_label,status_label,pickup_date_label,pickup_time_label,pickup_location_label,dropoff_date_label,dropoff_time_label,dropoff_location_label
    registrationNo_label = tk.Label(reviewFrame, text="", bg="#D9D9D9", font=('Arial', 17))
    registrationNo_label.place(x=170, y=463)
    agency_label = tk.Label(reviewFrame, text="", bg="#D9D9D9", font=('Arial', 17))
    agency_label.place(x=170, y=530)
    status_label = tk.Label(reviewFrame, text="", bg="#D9D9D9", font=('Arial', 17))
    status_label.place(x=170, y=595)
    pickup_date_label = tk.Label(reviewFrame, text="", bg="#D9D9D9", font=('Arial', 8))
    pickup_date_label.place(x=606, y=513)
    pickup_time_label = tk.Label(reviewFrame, text="", bg="#D9D9D9", font=('Arial', 8))
    pickup_time_label.place(x=535, y=513)
    pickup_location_label = tk.Label(reviewFrame, text="", bg="#D9D9D9", font=('Arial', 8))
    pickup_location_label.place(x=535, y=484)
    dropoff_date_label = tk.Label(reviewFrame, text="", bg="#D9D9D9", font=('Arial', 8))
    dropoff_date_label.place(x=606, y=612)
    dropoff_time_label = tk.Label(reviewFrame, text="", bg="#D9D9D9", font=('Arial', 8))
    dropoff_time_label.place(x=535, y=612)
    dropoff_location_label = tk.Label(reviewFrame, text="", bg="#D9D9D9", font=('Arial', 8))
    dropoff_location_label.place(x=535, y=583)

    # Variables for tracking selected booking details
    global selected_bookingID, selected_carID, selected_userID
    selected_bookingID = tk.StringVar()
    selected_carID = tk.StringVar()
    selected_userID = tk.StringVar()

    # Populate the Treeview
    populate_treeview()
