import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime

# Connect to the database
conn = sqlite3.connect('CAR2U.db')
cursor = conn.cursor()

# Verify if BookingDetails exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in database:", tables)

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

# Create main window
root = tk.Tk()
root.title("Your Bookings")
root.geometry("1280x720")

# Load the background image
bg_image_path = r"C:\Users\chewy\OneDrive\Car rental\Your Bookings.png"
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((1280, 720), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a canvas to hold the background image
canvas = tk.Canvas(root, width=bg_image.width, height=bg_image.height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Set up the Treeview on the canvas
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
selected_rating = tk.IntVar()
selected_bookingID = tk.IntVar()
selected_carID = tk.IntVar()  # New variable for carID
selected_userID = tk.IntVar()  # New variable for userID

# Load star images
black_star_img = ImageTk.PhotoImage(Image.open(r"C:\Users\chewy\OneDrive\Car rental\black star.png").resize((32, 32)))
yellow_star_img = ImageTk.PhotoImage(Image.open(r"C:\Users\chewy\OneDrive\Car rental\yellow star.png").resize((32, 32)))

# Star labels for rating
star_labels = []
for i in range(5):
    star_label = tk.Label(canvas, image=black_star_img, cursor="hand2", bg="#D9D9D9")
    star_label.place(x=842 + (i * 48), y=381)
    star_label.bind("<Button-1>", lambda e, rating=i+1: set_rating(rating))
    star_labels.append(star_label)

# Text box for review
review_entry = tk.Text(canvas, width=39, height=9, bg="white")
review_entry.place(x=845, y=426)

# Upload button
upload_button = tk.Button(root, text="UPLOAD", bg="#FF865A", command=upload_review, bd=0, font=("Arial", 14, "bold"), width=8)
upload_button.place(x=952, y=614)

# Labels to display additional details, placed on the canvas
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

# Run the main loop
root.mainloop()
