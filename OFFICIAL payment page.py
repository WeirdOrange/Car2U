import sqlite3
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import webbrowser  # Import webbrowser module
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to fetch booking, user, and car details using userID and carID
def fetch_booking_user_car_details(booking_id):
    conn = sqlite3.connect('CAR2U.db')
    cursor = conn.cursor()

    # Query to join BookingDetails, UserDetails, and CarDetails based on bookingID
    cursor.execute('''
        SELECT u.name, u.email, u.contactNo, c.model, c.price, b.numberOfDays
        FROM BookingDetails b
        JOIN UserDetails u ON b.userID = u.userID
        JOIN CarDetails c ON b.carID = c.carID
        WHERE b.bookingID = ?
    ''', (booking_id,))
    
    details = cursor.fetchone()
    conn.close()

    return details

# Initialize main Tkinter window
root = tk.Tk()
root.title("Payment Page")
root.geometry("1280x720")

# Load the background image
bg_image_path = r"C:\Users\chewy\OneDrive\Car rental\Payment Page official.png"
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((1280, 720), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a canvas to hold the background image
canvas = tk.Canvas(root, width=bg_image.width, height=bg_image.height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Fetch details with a specific bookingID
booking_id = 1  # Replace with the actual bookingID or fetch dynamically as needed
details = fetch_booking_user_car_details(booking_id)

# Function to fetch car price and booking number of days using column index
def fetch_booking_and_price():
    conn = sqlite3.connect('CAR2U.db')
    cursor = conn.cursor()

    # Fetch price from CarDetails and numberOfDays from BookingDetails
    cursor.execute('''
        SELECT CarDetails.price, BookingDetails.numberOfDays
        FROM CarDetails
        INNER JOIN BookingDetails ON CarDetails.carID = BookingDetails.carID
        WHERE BookingDetails.bookingID = ?
        LIMIT 1
    ''', (1,))  # Assuming booking ID is 1

    # Fetch result as a tuple (price, numberOfDays)
    data = cursor.fetchone()
    conn.close()

    return data

# Function to update name, email, and contactNo in UserDetails table
def update_user_details(name, email, contactNo):
    conn = sqlite3.connect('CAR2U.db')
    cursor = conn.cursor()

    # Updating only name, email, and contactNo fields in UserDetails
    cursor.execute('''
        UPDATE UserDetails
        SET name = ?, email = ?, contactNo = ?
        WHERE userID = ?
    ''', (name, email, contactNo, 1))  # Replace '1' with dynamic userID as needed

    conn.commit()
    conn.close()

# Fetch car price and number of days from the database
booking_and_price_data = fetch_booking_and_price()

if booking_and_price_data:
    # Use column index to access price and numberOfDays
    car_price = booking_and_price_data[0]  # First column: price
    number_of_days = booking_and_price_data[1]  # Second column: numberOfDays
    
    # Calculate the total amount
    total_amount = car_price * number_of_days

# Define positions for both small and large totalAmount displays
total_amount_position_small = (715, 512)  # Position for smaller text
total_amount_position_large = (715, 580)  # Position for larger, bold text

# Display totalAmount in small font
canvas.create_text(total_amount_position_small[0], total_amount_position_small[1], 
                   text=f"MYR {total_amount:.2f}", 
                   font=("Arial", 10), fill="black", anchor="e")

# Display totalAmount in larger bold font
canvas.create_text(total_amount_position_large[0], total_amount_position_large[1], 
                   text=f"MYR {total_amount:.2f}", 
                   font=("Arial", 23, "bold"), fill="black", anchor="e")

# Display user and booking details in the UI
entry_name = tk.Entry(root, font=("Arial", 14), bd=0)
entry_name.insert(0, details[0])  # UserDetails.name
canvas.create_window(250, 369, window=entry_name, width=200, height=25)

entry_email = tk.Entry(root, font=("Arial", 14), bd=0)
entry_email.insert(0, details[1])  # UserDetails.email
canvas.create_window(250, 456, window=entry_email, width=200, height=25)

entry_contactNo = tk.Entry(root, font=("Arial", 14), bd=0)
entry_contactNo.insert(0, details[2])  # UserDetails.contactNo
canvas.create_window(250, 543, window=entry_contactNo, width=200, height=25)

# Display car details and booking days
label_model = tk.Label(root, text=f"{details[3]}", font=("Arial", 10), anchor="e", bg="#DEF3FF")  # CarDetails.model
canvas.create_window(679, 422, window=label_model)

label_price = tk.Label(root, text=f"MYR {float(details[4]):.2f}", font=("Arial", 10), anchor="e", bg="#DEF3FF")  # CarDetails.price
canvas.create_window(681, 452, window=label_price)

label_days = tk.Label(root, text=f"{details[5]} days", font=("Arial", 10), anchor="e", bg="#DEF3FF")  # BookingDetails.numberOfDays
canvas.create_window(696, 482, window=label_days)

def add_transaction(transaction_method, total_amount, booking_id):
    try:
        conn = sqlite3.connect('CAR2U.db')
        cursor = conn.cursor()
        
        # Insert transaction details into Transactions table
        cursor.execute('''
            INSERT INTO Transactions (transactionMethod, totalAmount, bookingID)
            VALUES (?, ?, ?)
        ''', (transaction_method, total_amount, booking_id))
        
        # Retrieve the last inserted transactID
        transact_id = cursor.lastrowid
        
        # Commit the transaction
        conn.commit()
        print("Transaction successfully saved!")  # Confirmation message
        return transact_id  # Return transactID
    except sqlite3.Error as e:
        print("An error occurred:", e)  # Print error if it fails
    finally:
        conn.close()



def send_confirmation_email(user_email, booking_details):
    # Email configuration
    sender_email = "cartwoyouofficial@gmail.com"
    sender_password = "kcft xbdi orcq awzn"
    subject = "Your CAR2U Payment is Received"

    # Format email content
    email_body = f"""
    Dear Customer,

    Your booking payment has been received. Here are your booking details:
    Booking ID: {booking_details['bookingID']}
    

    Total Amount for Your Booking: MYR {booking_details['totalAmount']:.2f}

    
    Car Details:
    Registration No: {booking_details['registrationNo']}
    Model: {booking_details['model']}
    Colour: {booking_details['colour']}
    Fuel Type: {booking_details['fuelType']}
    Seating Capacity: {booking_details['seatingCapacity']}
    Transmission Type: {booking_details['transmissionType']}
    Price per day: MYR {booking_details['price']:.2f}
    
    Pickup & Dropoff Details:
    Pickup: {booking_details['pickupLocation']}, {booking_details['pickupDate']}, {booking_details['pickupTime']}
    Dropoff: {booking_details['dropoffLocation']}, {booking_details['dropoffDate']}, {booking_details['dropoffTime']}
    
    Agency Details:
    Name: {booking_details['agencyName']}
    Location: {booking_details['agencyLocation']}
    Contact: {booking_details['agencyContactNo']}
    
    Thank you for choosing CAR2U! We hope you have an enjoyable journey with us!
    """

    # Create email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = user_email
    message["Subject"] = subject
    message.attach(MIMEText(email_body, "plain"))

    # Send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        print("Confirmation email sent successfully.")
    except Exception as e:
        print("Failed to send email:", e)

# Updated confirm_payment function to include totalAmount in the email
def confirm_payment():
    # Get updated details from entry fields
    updated_name = entry_name.get()
    updated_email = entry_email.get()
    updated_contactNo = entry_contactNo.get()

    # Update user details in the database
    update_user_details(updated_name, updated_email, updated_contactNo)

    # Calculate total amount if booking and price data are available
    if booking_and_price_data:
        total_amount = car_price * number_of_days

    # Add transaction details and get transactID
    if selected_payment and total_amount:
        transact_id = add_transaction(selected_payment, total_amount, booking_id)
        
        # Update BookingDetails with transactID if transactID was successfully returned
        if transact_id:
            conn = sqlite3.connect('CAR2U.db')
            cursor = conn.cursor()
            
            # Set transactID and bookingStatus to "Paid" if transactID exists
            cursor.execute('''
                UPDATE BookingDetails
                SET transactID = ?, bookingStatus = 'Paid'
                WHERE bookingID = ?
            ''', (transact_id, booking_id))
            conn.commit()
            
            # Fetch booking details to send in email
            cursor.execute('''
                SELECT b.bookingID, c.registrationNo, c.model, c.colour, c.fuelType, 
                       c.seatingCapacity, c.transmissionType, c.price,
                       b.pickupLocation, b.pickupDate, b.pickupTime, 
                       b.dropoffLocation, b.dropoffDate, b.dropoffTime,
                       a.agencyName, a.agencyLocation, a.agencyContactNo,
                       b.numberOfDays
                FROM BookingDetails b
                JOIN CarDetails c ON b.carID = c.carID
                JOIN RentalAgency a ON c.agencyID = a.agencyID
                WHERE b.bookingID = ?
            ''', (booking_id,))
            booking_data = cursor.fetchone()

            # Close database connection
            conn.close()

            # Calculate total amount and map booking data to a dictionary
            total_amount = booking_data[7] * booking_data[17]
            booking_details = {
                "bookingID": booking_data[0],
                "registrationNo": booking_data[1],
                "model": booking_data[2],
                "colour": booking_data[3],
                "fuelType": booking_data[4],
                "seatingCapacity": booking_data[5],
                "transmissionType": booking_data[6],
                "price": booking_data[7],
                "pickupLocation": booking_data[8],
                "pickupDate": booking_data[9],
                "pickupTime": booking_data[10],
                "dropoffLocation": booking_data[11],
                "dropoffDate": booking_data[12],
                "dropoffTime": booking_data[13],
                "agencyName": booking_data[14],
                "agencyLocation": booking_data[15],
                "agencyContactNo": booking_data[16],
                "totalAmount": total_amount
            }

            # Send confirmation email to the user
            send_confirmation_email(updated_email, booking_details)

        messagebox.showinfo("Complete Payment", "Your payment is confirmed. You will be redirected shortly to the payment page.")

        # Redirect to the appropriate payment page
        if selected_payment == "TNG":
            webbrowser.open("https://payment.tngdigital.com.my/sc/bDLnXXwSUR")
        elif selected_payment == "Bank":
            webbrowser.open("https://www.cimbclicks.com.my/clicks/#/")
        elif selected_payment == "Paypal":
            webbrowser.open("https://www.paypal.com/signin")



# Create a "Confirm Payment" button
confirm_button = tk.Button(root, text="CONFIRM PAYMENT", font=("Arial", 23, "bold"), bd=0, bg="white", command=confirm_payment)
canvas.create_window(1005, 630, window=confirm_button, width=310, height=50)

# Track the currently selected payment method
selected_payment = None

# Define actions for each button with image switching
def tng_action():
    global selected_payment
    selected_payment = "TNG"
    highlight_selected(tng, tng_clicked_photo)

def bank_action():
    global selected_payment
    selected_payment = "Bank"
    highlight_selected(bank, bank_clicked_photo)

def card_action():
    global selected_payment
    selected_payment = "Paypal"
    highlight_selected(card, paypal_clicked_photo)

# Function to highlight the selected button by changing the image and resetting others
def highlight_selected(selected_button, clicked_image):
    # Reset the images for all buttons to default
    tng.config(image=tng_photo)
    bank.config(image=bank_photo)
    card.config(image=paypal_photo)

    # Change the selected button to the "clicked" version of the image
    selected_button.config(image=clicked_image)
    
# Load default and clicked versions of TNG image
tng_image = Image.open(r"C:\Users\chewy\OneDrive\Car rental\tng button.png")
tng_image = tng_image.resize((290, 52), Image.LANCZOS)
tng_photo = ImageTk.PhotoImage(tng_image)

tng_clicked_image = Image.open(r"C:\Users\chewy\OneDrive\Car rental\tng click.png")
tng_clicked_image = tng_clicked_image.resize((290, 52), Image.LANCZOS)
tng_clicked_photo = ImageTk.PhotoImage(tng_clicked_image)

# Load default and clicked versions of bank image
bank_image = Image.open(r"C:\Users\chewy\OneDrive\Car rental\online banking button.png")
bank_image = bank_image.resize((290, 52), Image.LANCZOS)
bank_photo = ImageTk.PhotoImage(bank_image)

bank_clicked_image = Image.open(r"C:\Users\chewy\OneDrive\Car rental\bank click.png")
bank_clicked_image = bank_clicked_image.resize((290, 52), Image.LANCZOS)
bank_clicked_photo = ImageTk.PhotoImage(bank_clicked_image)

# Load default and clicked versions of card image
paypal_image = Image.open(r"C:\Users\chewy\OneDrive\Car rental\paypal button.png")
paypal_image = paypal_image.resize((290, 52), Image.LANCZOS)
paypal_photo = ImageTk.PhotoImage(paypal_image)

paypal_clicked_image = Image.open(r"C:\Users\chewy\OneDrive\Car rental\paypal clicked.png")
paypal_clicked_image = paypal_clicked_image.resize((290, 52), Image.LANCZOS)
paypal_clicked_photo = ImageTk.PhotoImage(paypal_clicked_image)

# Create buttons using the default images
tng = tk.Button(root, image=tng_photo, command=tng_action, borderwidth=0, bg="white", fg="white")
bank = tk.Button(root, image=bank_photo, command=bank_action, borderwidth=0, bg="white", fg="white")
card = tk.Button(root, image=paypal_photo, command=card_action, borderwidth=0, bg="white", fg="white")

# Add buttons to the canvas
canvas.create_window(1005, 342, window=tng)
canvas.create_window(1005, 410, window=bank)
canvas.create_window(1005, 482, window=card)

# Start the Tkinter main loop
root.mainloop()
