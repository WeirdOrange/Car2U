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

# Function to format date as "21 August 2024"
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

    cursor.execute(''' 
        SELECT CarDetails.registrationNo, CarDetails.model, 
               BookingDetails.dateCreated, BookingDetails.pickupDate, 
               BookingDetails.dropoffDate, BookingDetails.bookingStatus, BookingDetails.bookingID
        FROM BookingDetails
        JOIN CarDetails ON BookingDetails.carID = CarDetails.carID
    ''')

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
            star_label.config(image=root.yellow_star_img)
        else:
            star_label.config(image=root.black_star_img)

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
        default_image_label.place_forget()  # Hide the default image
        bookingID = tree.item(selected_row)['values'][6]
        selected_bookingID.set(bookingID)

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
            pickup_date_formatted = format_date(details[3])
            pickup_time_formatted = format_time(details[4])
            dropoff_date_formatted = format_date(details[6])
            dropoff_time_formatted = format_time(details[7])

            registrationNo_label.config(text=f"{details[0]}")
            agency_label.config(text=f"{details[1]}")
            status_label.config(text=f"{details[2]}")
            pickup_date_label.config(text=f"{pickup_date_formatted}")
            pickup_time_label.config(text=f"{pickup_time_formatted}")
            pickup_location_label.config(text=f"{details[5]}")
            dropoff_date_label.config(text=f"{dropoff_date_formatted}")
            dropoff_time_label.config(text=f"{dropoff_time_formatted}")
            dropoff_location_label.config(text=f"{details[8]}")

            selected_carID.set(details[9])
            selected_userID.set(details[10])

            # Show review UI elements
            show_review_ui()

            # Display "To Pay" image and "Pay Now" button if booking is approved
            if details[2] == "Approved":
                pay_image_label.place(x=818, y=200)
                pay_button.place(x=932, y=528)
            else:
                pay_image_label.place_forget()
                pay_button.place_forget()
    else:
        default_image_label.place(x=70, y=192)  # Show default image if no row is selected

# Function to show review UI elements
def show_review_ui():
    review_entry.place(x=845, y=426)
    upload_button.place(x=952, y=614)
    for i, star_label in enumerate(star_labels):
        star_label.place(x=842 + (i * 48), y=381)

# Create main window
root = tk.Tk()
root.title("Your Bookings")
root.geometry("1280x720")

# Background image
bg_image_path = r"C:\Users\chewy\OneDrive\Car rental\Your Bookings.png"
bg_image = Image.open(bg_image_path).resize((1280, 720), Image.LANCZOS)
root.bg_photo = ImageTk.PhotoImage(bg_image)
background_label = tk.Label(root, image=root.bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Treeview setup
tree = ttk.Treeview(root, columns=("Reg No", "Model", "Date Created", "Pickup Date", "Drop-off Date", "Status"), show="headings")
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
tree.bind("<ButtonRelease-1>", on_row_selected)

# Load and display default image if no row is selected
default_image_path = r"C:\Users\chewy\OneDrive\Car rental\review n payment frame.png"
root.default_image = ImageTk.PhotoImage(Image.open(default_image_path).resize((350, 450), Image.LANCZOS))
default_image_label = tk.Label(root, image=root.default_image, bg="#D9D9D9")

# Place the default image initially
default_image_label.place(x=818, y=198)

# Star images
root.black_star_img = ImageTk.PhotoImage(Image.open(r"C:\Users\chewy\OneDrive\Car rental\black star.png").resize((32, 32)))
root.yellow_star_img = ImageTk.PhotoImage(Image.open(r"C:\Users\chewy\OneDrive\Car rental\yellow star.png").resize((32, 32)))

# Star labels
selected_rating = tk.IntVar()
star_labels = []
for i in range(5):
    star_label = tk.Label(root, image=root.black_star_img, cursor="hand2", bg="#D9D9D9")
    star_label.place_forget()  # Hide initially
    star_label.bind("<Button-1>", lambda e, rating=i+1: set_rating(rating))
    star_labels.append(star_label)

# Review entry and upload button
review_entry = tk.Text(root, width=39, height=9, bg="white")
review_entry.place_forget()  # Hide initially

upload_button = tk.Button(root, text="UPLOAD", bg="#FF865A", command=upload_review, bd=0, font=("Arial", 14, "bold"), width=8)
upload_button.place_forget()  # Hide initially

# "To pay" image and "Pay Now" button
pay_image_path = r"C:\Users\chewy\OneDrive\Car rental\To pay.png"
root.pay_image = ImageTk.PhotoImage(Image.open(pay_image_path).resize((350, 450), Image.LANCZOS))
pay_image_label = tk.Label(root, image=root.pay_image, bg="#D9D9D9")

pay_button = tk.Button(root, text="PAY NOW", bg="#FF865A", bd=0, font=("Arial", 14, "bold"), width=10, command=lambda: messagebox.showinfo("Payment", "Redirecting to payment..."))

# Labels for booking details
registrationNo_label = tk.Label(root, text="", bg="#D9D9D9", font=('Arial', 17))
registrationNo_label.place(x=170, y=463)
agency_label = tk.Label(root, text="", bg="#D9D9D9", font=('Arial', 17))
agency_label.place(x=170, y=530)
status_label = tk.Label(root, text="", bg="#D9D9D9", font=('Arial', 17))
status_label.place(x=170, y=595)
pickup_date_label = tk.Label(root, text="", bg="#D9D9D9", font=('Arial', 8))
pickup_date_label.place(x=606, y=513)
pickup_time_label = tk.Label(root, text="", bg="#D9D9D9", font=('Arial', 8))
pickup_time_label.place(x=535, y=513)
pickup_location_label = tk.Label(root, text="", bg="#D9D9D9", font=('Arial', 8))
pickup_location_label.place(x=535, y=484)
dropoff_date_label = tk.Label(root, text="", bg="#D9D9D9", font=('Arial', 8))
dropoff_date_label.place(x=606, y=612)
dropoff_time_label = tk.Label(root, text="", bg="#D9D9D9", font=('Arial', 8))
dropoff_time_label.place(x=535, y=612)
dropoff_location_label = tk.Label(root, text="", bg="#D9D9D9", font=('Arial', 8))
dropoff_location_label.place(x=535, y=583)

# Variables for tracking selected booking details
selected_bookingID = tk.StringVar()
selected_carID = tk.StringVar()
selected_userID = tk.StringVar()

# Populate the Treeview
populate_treeview()

root.mainloop()
