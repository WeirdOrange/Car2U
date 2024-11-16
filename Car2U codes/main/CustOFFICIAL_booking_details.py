import sqlite3
import tkinter as tk
import customtkinter as ctk
import smtplib
import pywinstyles
from tkinter import messagebox, Toplevel
from datetime import datetime
from PIL import Image, ImageTk
from MainCar2U_UserInfo import get_user_info,set_user_info
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to handle login button click
def open_login(current_window, login_callback):
    current_window.destroy()  # Close the signup window
    userInfo = ""
    set_user_info(userInfo)
    login_callback()

# Function to handle selection button click
def open_listing(current_window, list_callback):
    current_window.destroy()  # Close the signup window
    list_callback()

# Function to handle profile button click
def open_profile(current_window, profile_callback):
    current_window.destroy()  # Close the signup window
    profile_callback()
    
# Function to handle profile button click
def open_review(current_window, review_callback):
    current_window.destroy()  # Close the signup window
    review_callback()

def accManage(current_window, login_callback,profile_callback,review_callback):
    global pfpState, droptabFrame

    if pfpState == 1:
        droptabFrame = ctk.CTkFrame(current_window,width=190,height=240, bg_color="#E6F6FF",fg_color="#E6F6FF")
        droptabFrame.place(x=1090, y=60)

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
        logout.place(x=30,y=184)
        pfpState = 0
    else:
        droptabFrame.destroy()
        pfpState = 1


# Function to connect and fetch data from the database
def fetch_car_and_agency_data():
    conn = sqlite3.connect('CAR2U.db')
    cursor = conn.cursor()

    # Fetch car and agency data with a JOIN on the RentalAgency table
    cursor.execute('''
        SELECT CarDetails.registrationNo, CarDetails.model, CarDetails.colour, 
               CarDetails.fuelType, CarDetails.seatingCapacity, 
               CarDetails.transmissionType, CarDetails.price,
               RentalAgency.agencyName, RentalAgency.agencyLocation, 
               RentalAgency.agencyContactNo, CarDetails.carImage
        FROM CarDetails
        INNER JOIN RentalAgency ON CarDetails.agencyID = RentalAgency.agencyID
        LIMIT 1
    ''')

    car_data = cursor.fetchone()
    conn.close()

    return car_data

def split_text(text, max_words_per_line=3):
    """
    Split the text into multiple lines with a maximum of `max_words_per_line` words per line.
    """
    words = text.split()
    lines = []
    for i in range(0, len(words), max_words_per_line):
        lines.append(' '.join(words[i:i + max_words_per_line]))
    return lines

# Function to format date and time
def format_datetime(date_str, time_str):
    # Convert SQL date string to Python datetime object
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')  # Assuming SQL date format is YYYY-MM-DD
    formatted_date = date_obj.strftime('%d %B %Y')  # e.g., '21 August 2024'
    
    # Convert SQL time string to Python time object and format it
    time_obj = datetime.strptime(time_str, '%H:%M:%S')  # Assuming SQL time format is HH:MM:SS
    formatted_time = time_obj.strftime('%I.%M%p').lower()  # e.g., '10.00am'
    
    return formatted_date, formatted_time

# Call this function after confirming the booking request
def request_booking(review_callback):
    try:
        conn = sqlite3.connect('CAR2U.db')
        cursor = conn.cursor()

        # Update the status of the booking (assuming bookingID is 1)
        cursor.execute('''
            UPDATE BookingDetails
            SET bookingStatus = ?
            WHERE bookingID = ?
        ''', ("Requested", 1))

        conn.commit()  # Save (commit) the changes to the database
        conn.close()

        # Send confirmation email
        send_booking_email(1)  # Replace '1' with the actual bookingID if needed

        # Show a message box confirming the payment
        messagebox.showinfo("Booking Request Made", "Thank you for choosing Car2U! Check your email for booking details.")
        open_review(detailsFrame,review_callback)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def fetch_booking_data():
    conn = sqlite3.connect('CAR2U.db')
    cursor = conn.cursor()

    # Fetch booking data from BookingDetails table
    cursor.execute('''
        SELECT pickupDate, pickupTime, pickupLocation, 
               dropoffDate, dropoffTime, dropoffLocation, numberOfDays
        FROM BookingDetails
        WHERE bookingID = ?
        LIMIT 1
    ''', (1,))  # Assuming booking ID is 1

    booking_data = cursor.fetchone()
    conn.close()

    return booking_data

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

def bookingdetails(login_callback,list_callback,profile_callback,review_callback):
    # Create main window
    global detailsFrame
    detailsFrame = Toplevel()
    detailsFrame.title("Booking Details")
    detailsFrame.geometry("1280x720")
    detailsFrame.resizable(False, False)

    # Load the background image
    bg_image_path = r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Cust-Booking-Details\Booking Details.png"
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    """
    pfp_img = ctk.CTkImage(Image.open(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Cust-Booking-Details\image_1.png"),size=(40,40))
    pfp_label = ctk.CTkButton(detailsFrame, image=pfp_img, text="", bg_color="#F47749", fg_color="#F47749",
                              width=40, height=40, command=lambda:accManage(detailsFrame,login_callback,profile_callback,review_callback))
    pfp_label.place(x=1203, y=5)
    pywinstyles.set_opacity(pfp_label,color="#F47749")

    backBttn = ctk.CTkButton(detailsFrame, text="Back to Selection", command=lambda:open_listing(detailsFrame,list_callback))
    backBttn.place(x=50,y=115)
    """

    # Create a canvas to hold the background image
    canvas = tk.Canvas(detailsFrame, width=bg_image.width, height=bg_image.height)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")


    # Fetch car and agency data from the database
    car_data = fetch_car_and_agency_data()

    if car_data:
        # Define positions for each label
        positions = {
            "registrationNo": (155, 505),
            "model": (351, 445),
            "colour": (379, 445),
            "fuelType": (155, 569),
            "transmissionType": (451, 571),
            "seatingCapacity": (451, 503),
            "price": (1212, 466),
            "agencyName": (954, 249),
            "agencyLocation": (1014, 280),
            "agencyContactNo": (1014, 343),
        }

    # Place the labels with specific font sizes and bold styling for model and colour
    canvas.create_text(positions["registrationNo"][0], positions["registrationNo"][1], 
                    text=f"{car_data[0]}", font=("Arial", 14), fill="black", anchor="w")  # Left-aligned for registration number

    canvas.create_text(positions["model"][0], positions["model"][1], 
                    text=f"{car_data[1]}", font=("Arial",23, "bold"), fill="black", anchor="e")  # Right-aligned and bold for model

    canvas.create_text(positions["colour"][0], positions["colour"][1], 
                    text=f"{car_data[2]}", font=("Arial", 23, "bold"), fill="black", anchor="w")  # Left-aligned and bold for colour

    canvas.create_text(positions["fuelType"][0], positions["fuelType"][1], 
                    text=f"{car_data[3]}", font=("Arial", 14), fill="black", anchor="w")  # Left-aligned for fuel type

    canvas.create_text(positions["transmissionType"][0], positions["transmissionType"][1], 
                    text=f"{car_data[5]}", font=("Arial", 14), fill="black", anchor="w")  # Left-aligned for transmission type

    canvas.create_text(positions["seatingCapacity"][0], positions["seatingCapacity"][1], 
                    text=f"{car_data[4]}", font=("Arial", 14), fill="black", anchor="w")  # Left-aligned for seating capacity

    canvas.create_text(positions["price"][0], positions["price"][1], 
                    text=f"MYR {float(car_data[6]):.2f}", font=("Arial", 10), fill="black", anchor="e")  # Right-aligned for price

    canvas.create_text(positions["agencyName"][0], positions["agencyName"][1], 
                    text=f"{car_data[7]}", font=("Arial", 14), fill="black", anchor="w")  # Left-aligned for agency name

    # Split and display dropoffLocation text
    agencyLocation_lines = split_text(car_data[8])
    for idx, line in enumerate(agencyLocation_lines):
        canvas.create_text(positions["agencyLocation"][0], positions["agencyLocation"][1] + (idx * 15), 
                        text=line, font=("Arial", 10), fill="black", anchor="w")  # agencyLocation

    canvas.create_text(positions["agencyContactNo"][0], positions["agencyContactNo"][1], 
                    text=f"{car_data[9]}", font=("Arial", 10), fill="black", anchor="w")  # Left-aligned for agency contact number

    # Load and display carImage
    car_image_path = car_data[10]  # Assuming carImage is stored as a file path
    try:
        car_img = Image.open(car_image_path)
        car_img = car_img.resize((360, 230))  # Resize as necessary
        car_photo = ImageTk.PhotoImage(car_img)
        canvas.create_image(110, 180, image=car_photo, anchor="nw")  # Adjust position as needed
        detailsFrame.car_photo = car_photo  # Prevent garbage collection
    except Exception as e:
        print(f"Error loading car image: {e}")

    # Fetch only booking data
    booking_data = fetch_booking_data()

    # Define positions for booking details labels
    positions = {
        "pickupDate": (760, 325),
        "pickupTime": (687, 325),
        "pickupLocation": (692, 271),
        "dropoffDate": (765, 555),
        "dropoffTime": (692, 555),
        "dropoffLocation": (692, 501),
        "numberOfDays": (781, 411),
    }


    # Assuming you already have booking_data fetched
    pickupDate, pickupTime = format_datetime(booking_data[0], booking_data[1])
    dropoffDate, dropoffTime = format_datetime(booking_data[3], booking_data[4])

    # Check if booking_data exists and place it on the canvas
    if booking_data:
        canvas.create_text(positions["pickupDate"][0], positions["pickupDate"][1], 
                    text=f"{pickupDate}", font=("Arial", 10), fill="black", anchor="w")

        canvas.create_text(positions["pickupTime"][0], positions["pickupTime"][1], 
                    text=f"{pickupTime}", font=("Arial", 10), fill="black", anchor="w")

        # Split and display pickupLocation text
        pickup_lines = split_text(booking_data[2])
        for idx, line in enumerate(pickup_lines):
            canvas.create_text(positions["pickupLocation"][0], positions["pickupLocation"][1] + (idx * 15), 
                            text=line, font=("Arial", 10), fill="black", anchor="w")  # pickupLocation

        canvas.create_text(positions["dropoffDate"][0], positions["dropoffDate"][1], 
                    text=f"{dropoffDate}", font=("Arial", 10), fill="black", anchor="w")

        canvas.create_text(positions["dropoffTime"][0], positions["dropoffTime"][1], 
                    text=f"{dropoffTime}", font=("Arial", 10), fill="black", anchor="w")

        # Split and display dropoffLocation text
        dropoff_lines = split_text(booking_data[5])
        for idx, line in enumerate(dropoff_lines):
            canvas.create_text(positions["dropoffLocation"][0], positions["dropoffLocation"][1] + (idx * 15), 
                            text=line, font=("Arial", 10), fill="black", anchor="w")  # dropoffLocation

        canvas.create_text(positions["numberOfDays"][0], positions["numberOfDays"][1], 
                        text=f"{booking_data[6]} days", font=("Arial", 10), fill="black", anchor="w")  # numberOfDays
    else:
        # Display an error message if no booking data is found
        canvas.create_text(400, 300, text="No booking data found.", font=("Arial", 10), fill="red")

    # Fetch car price and number of days from the database
    booking_and_price_data = fetch_booking_and_price()

    if booking_and_price_data:
        # Use column index to access price and numberOfDays
        car_price = booking_and_price_data[0]  # First column: price
        number_of_days = booking_and_price_data[1]  # Second column: numberOfDays
        
        # Calculate the total amount
        total_amount = car_price * number_of_days

    # Define positions for both small and large totalAmount displays
    total_amount_position_small = (1212, 497)  # Position for smaller text
    total_amount_position_large = (1225, 560)  # Position for larger, bold text

    # Display totalAmount in small font
    canvas.create_text(total_amount_position_small[0], total_amount_position_small[1], 
                    text=f"MYR {total_amount:.2f}", 
                    font=("Arial", 10), fill="black", anchor="e")

    # Display totalAmount in larger bold font
    canvas.create_text(total_amount_position_large[0], total_amount_position_large[1], 
                    text=f"MYR {total_amount:.2f}", 
                    font=("Arial", 23, "bold"), fill="black", anchor="e")

    """
        button is not showing because ur using canvas and pack, canvas filled the entire detailsFrame. so if you want request booking button to show on top,
        put it in another frame maybe.
    """
    # Create the "Make Payment" button and place it on the canvas
    request_booking_button = tk.Button(detailsFrame, text="REQUEST BOOKING", font=("Arial", 19, "bold"), bd=0, width=17, bg="#FF865A", fg="black", 
                                       command=lambda:request_booking(review_callback))
    request_booking_button.place(x=513, y=645)


def send_booking_email(booking_id):
    # Fetch user and booking details based on booking_id
    conn = sqlite3.connect('CAR2U.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT BookingDetails.bookingID, BookingDetails.pickupLocation, BookingDetails.pickupDate, BookingDetails.pickupTime,
               BookingDetails.dropoffLocation, BookingDetails.dropoffDate, BookingDetails.dropoffTime,
               CarDetails.registrationNo, CarDetails.model, CarDetails.colour, CarDetails.fuelType, 
               CarDetails.seatingCapacity, CarDetails.transmissionType, CarDetails.price,
               RentalAgency.agencyName, RentalAgency.agencyLocation, RentalAgency.agencyContactNo,
               UserDetails.email
        FROM BookingDetails
        INNER JOIN CarDetails ON BookingDetails.carID = CarDetails.carID
        INNER JOIN RentalAgency ON CarDetails.agencyID = RentalAgency.agencyID
        INNER JOIN UserDetails ON BookingDetails.userID = UserDetails.userID
        WHERE BookingDetails.bookingID = ?
    ''', (booking_id,))

    data = cursor.fetchone()
    conn.close()

    if data:
        # Unpack data
        (bookingID, pickupLocation, pickupDate, pickupTime, dropoffLocation, dropoffDate, dropoffTime, 
         registrationNo, model, colour, fuelType, seatingCapacity, transmissionType, 
         price, agencyName, agencyLocation, agencyContactNo, user_email) = data

        # Email content
        subject = "Car Rental Booking Details Confirmation"
        body = f"""
        Dear Customer,
        Your booking request have been made. Here are your booking details: 
        Booking ID: {bookingID}

        Car Details:
        Registration No: {registrationNo}
        Model: {model}
        Colour: {colour}
        Fuel Type: {fuelType}
        Seating Capacity: {seatingCapacity}
        Transmission Type: {transmissionType}
        Price per day: MYR {price:.2f}

        Pickup & Dropoff Details:
        Pickup: {pickupLocation}, {pickupDate}, {pickupTime}
        Dropoff: {dropoffLocation}, {dropoffDate}, {dropoffTime}
  
        Agency Details:
        Name: {agencyName}
        Location: {agencyLocation}
        Contact: {agencyContactNo}


        Your booking request wil be processed within 2 business days. An email will be sent upon approval to proceed with payment. 
        Thank you for choosing Car2U. We hope you have a pleasant experience with us.
        
        Best regards,
        Car2U Team
        """

        # Send email
        sender_email = "cartwoyouofficial@gmail.com"
        sender_password = "kcft xbdi orcq awzn"

        try:
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = user_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            # Setup server connection
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()

            print("Email sent successfully.")
        except Exception as e:
            print(f"Failed to send email: {e}")
    else:
        print("No booking data found.")