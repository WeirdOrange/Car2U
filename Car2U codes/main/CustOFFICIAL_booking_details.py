import sqlite3
import tkinter as tk
import customtkinter as ctk
import smtplib
import pywinstyles
from pathlib import Path
from tkinter import messagebox, Toplevel
from pandas import date_range
from datetime import datetime, date, timedelta
from PIL import Image, ImageTk
from MainCar2U_UserInfo import get_user_info,set_user_info,get_Car_info
from CustBookingListCar2U import getPickLocate,getDropLocate,getPickDate,getDropDate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkcalendar import DateEntry
from io import BytesIO

# Set up the asset path
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Cust-Booking-Details")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

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

# Function to handle chats button click
def open_chat(current_window, chat_callback):
    current_window.destroy()  # Close the window
    chat_callback()

def accManage(current_window, login_callback,profile_callback,review_callback):
    global pfpState, droptabFrame

    if pfpState == 1:
        droptabFrame = ctk.CTkFrame(current_window,width=190,height=240, bg_color="#E6F6FF",fg_color="#E6F6FF")
        droptabFrame.place(x=1090, y=95)

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

def convert_data(data):
    global car_img
    img_byte = BytesIO(data)
    img = Image.open(img_byte)
    img = img.resize((400,220), Image.Resampling.LANCZOS)
    car_img = ImageTk.PhotoImage(img)
    return car_img

def fetch_booking_data(selected_Pdate,selected_Ddate):
    if selected_Pdate and selected_Ddate:
        try:
            dateTaken = []
            conn = sqlite3.connect('CAR2U.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Fetch booking data from BookingDetails table
            cursor.execute('''
                SELECT pickupDate, dropoffDate, bookingStatus FROM BookingDetails
                WHERE bookingStatus NOT in
				(SELECT bookingStatus FROM BookingDetails 
				WHERE bookingStatus = "Rejected" or bookingStatus = 'Cancelled') and carID = ? and
				(pickupDate = ? or dropoffDate = ? or pickupDate = ? or dropoffDate = ?)
            ''', (carID,selected_Pdate,selected_Pdate,selected_Ddate,selected_Ddate))

            booking_data = cursor.fetchall()
            conn.close()

            for row in booking_data:
                startdate = row[0]
                enddate = row[1]

                dateRange = date_range(start=startdate,end=enddate)
                selecteRange = date_range(start=selected_Pdate,end=selected_Ddate)
                for date in selecteRange:
                    for day in dateRange:
                        if day == date:
                            result = "Rejected"
                            dateTaken.append(date)
            
            if dateTaken:
                messagebox.showinfo("Request Failed", f"Car is currently unavailable in the following dates:\n{dateTaken}")
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", "Error occurred during registration: {}".format(e))
        finally:
            conn.close()
    
    return result

# Function to connect and fetch data from the database
def fetch_car_and_agency_data():
    try:
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
            WHERE carID = ?
        ''',(carID,))

        car_data = cursor.fetchone()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Error", "Error occurred during registration: {}".format(e))
    finally:
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

def review_data(review_callback):
    global datePickup, timePickup, locatePickup, dateDropoff, timeDropoff, locateDropoff
    try:
        datePickup = pickupDate.get_date()
        timePickup = time_mapping.get(selectedTime.get()).time()
        locatePickup = pickupLocation.get()
        dateDropoff = dropoffDate.get_date()
        timeDropoff = time_mapping2.get(selectedTime2.get()).time()
        locateDropoff = dropoffLocation.get()
        
    except Exception as e:
        messagebox.showerror("Error", "Please make sure every Details are inserted.")
        return 0

    fetch_booking_data(datePickup,dateDropoff)
    if not datePickup or not timePickup or not locatePickup or not dateDropoff or not timeDropoff or not locateDropoff:
        messagebox.showinfo("Input Error", "Please make sure every Details are inserted.")
        
    else: # IF the values are inputted correctly
        print("Everything checks out")
        request_booking(review_callback)

# Call this function after confirming the booking request
def request_booking(review_callback):
    try:
        print(carID,userInfo,datePickup.strftime("%Y-%m-%d"),timePickup.strftime("%H:%M:%S"),str(locatePickup),dateDropoff.strftime("%Y-%m-%d"),timeDropoff.strftime("%H:%M:%S"),str(locateDropoff),float(total_amount))
        conn = sqlite3.connect('CAR2U.db')
        cursor = conn.cursor()

        # Insert the booking request
        cursor.execute('''
            INSERT into BookingDetails (carID,userID,pickupDate,pickupTime,pickupLocation,dropoffDate,dropoffTime,
                                        dropoffLocation,totalAmount,bookingStatus)
            VALUES(?,?,?,?,?,?,?,?,?,"Pending")
        ''', (carID,userInfo,datePickup.strftime("%Y-%m-%d"),timePickup.strftime("%H:%M:%S"),str(locatePickup),dateDropoff.strftime("%Y-%m-%d"),timeDropoff.strftime("%H:%M:%S"),str(locateDropoff),float(total_amount)))

        conn.commit()  # Save (commit) the changes to the database
        conn.close()

        # Send confirmation email
        send_booking_email()

        # Show a message box confirming the payment
        messagebox.showinfo("Booking Request Made", "Thank you for choosing Car2U! Check your email for booking details.")
        open_review(detailsFrame,review_callback)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        return 0

# Function to fetch car price and booking number of days using column index
def fetch_booking_and_price():
    pickDate = pickupDate.get_date()
    # Refuses users to select the same day or before the pickup date
    nexttoday = pickupDate.get_date()+timedelta(1)
    dropoffDate.config(mindate=nexttoday)

    dropDate = dropoffDate.get_date()
    number_of_days = (dropDate - pickDate).days
    if number_of_days < 0:
        number_of_days = 0
    print(number_of_days)
    
    # Calculate the total amount
    global total_amount
    total_amount = carPrice * number_of_days

    # Define positions for both small and large totalAmount displays
    total_amount_position_small = (1212, 497)  # Position for smaller text
    total_amount_position_large = (1225, 560)  # Position for larger, bold text

    global smallAmount, bigAmount
    canvas.delete(smallAmount)
    canvas.delete(bigAmount)
    # Display totalAmount in small font
    smallAmount = canvas.create_text(total_amount_position_small[0], total_amount_position_small[1], 
                    text=f"MYR {total_amount:.2f}", 
                    font=("Arial", 10), fill="black", anchor="e")

    # Display totalAmount in larger bold font
    bigAmount = canvas.create_text(total_amount_position_large[0], total_amount_position_large[1], 
                    text=f"MYR {total_amount:.2f}", 
                    font=("Arial", 23, "bold"), fill="black", anchor="e")

def bookingdetails(login_callback,list_callback,profile_callback,review_callback,chat_callback):
    # Create main window
    global detailsFrame
    detailsFrame = Toplevel()
    detailsFrame.title("Booking Details")
    detailsFrame.geometry("1280x720")
    detailsFrame.resizable(False, False)

    global carID, userInfo
    carID = get_Car_info()
    print("car: ",carID)
    userInfo = get_user_info()

    # Load the background image
    global bg_photo
    bg_image_path = relative_to_assets("Booking Details.png")
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    detailsFrame.bg_photo = bg_photo
    
    # Create a canvas to hold the background image
    global canvas
    canvas = tk.Canvas(detailsFrame, width=bg_image.width, height=bg_image.height)
    canvas.place(x=0,y=0)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Fetch car and agency data from the database
    car_data = fetch_car_and_agency_data()
    global carPrice
    carPrice = car_data[6]

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
            "agencyContactNo": (1014, 343)
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

    # Create the "Make Payment" button and place it on the canvas
    chatting = ctk.CTkButton(detailsFrame, text=f"Chat With Us", font=("Arial", 10, "bold"), text_color="white", width=90, height=30, bg_color="#FEBD71", fg_color="#FEBD71", 
                                       command=lambda: open_chat(detailsFrame, chat_callback))
    chatting.place(x=1130, y=330)

    # Split and display dropoffLocation text
    agencyLocation_lines = split_text(car_data[8])
    for idx, line in enumerate(agencyLocation_lines):
        canvas.create_text(positions["agencyLocation"][0], positions["agencyLocation"][1] + (idx * 15), 
                        text=line, font=("Arial", 10), fill="black", anchor="w")  # agencyLocation

    canvas.create_text(positions["agencyContactNo"][0], positions["agencyContactNo"][1], 
                    text=f"{car_data[9]}", font=("Arial", 10), fill="black", anchor="w")  # Left-aligned for agency contact number

    # Load and display carImage
    car_image_path = car_data[10]
    try:
        car_photo = convert_data(car_image_path)
        canvas.create_image(110, 180, image=car_photo, anchor="nw")  # Adjust position as needed
        detailsFrame.car_photo = car_photo  # Prevent garbage collection
    except Exception as e:
        print(f"Error loading car image: {e}")

    # Define positions for booking details labels
    positions = {
        "pickupDate": (785, 315),
        "pickupTime": (682, 310),
        "pickupLocation": (682, 260),
        "dropoffDate": (785, 545),
        "dropoffTime": (682, 540),
        "dropoffLocation": (682, 490),
        "numberOfDays": (781, 411),
    }

    # Fetch previous informations
    plocation = getPickLocate()
    pDate = getPickDate()
    dlocation = getDropLocate()
    dDate = getDropDate()

    global locations, pickupDate, dropoffDate
    locations = ["Choose A Location","Penang International Airport","Penang Komtar","Penang Sentral",
                 "Kuala Lumpur International Airport","Kuala Lumpur Sentral","Kuala Lumpur City Centre",
                 "Sultan Azlan Shah Airport","Bus Terminal Amanjaya Ipoh","Ipoh Railway Station",
                 "INTI INTERNATION COLLEGE PENANG"]
    time = ["10.00am","12.00am","3.00pm","5.00pm"]
    time2 = ["10.00am","12.00am","3.00pm","5.00pm"]
    timeVar = [datetime.strptime('10:00:00', "%H:%M:%S"),datetime.strptime('12:00:00', "%H:%M:%S"),datetime.strptime('15:00:00', "%H:%M:%S"),datetime.strptime('17:00:00', "%H:%M:%S")]
    timeVar2 = [datetime.strptime('10:00:00', "%H:%M:%S"),datetime.strptime('12:00:00', "%H:%M:%S"),datetime.strptime('15:00:00', "%H:%M:%S"),datetime.strptime('17:00:00', "%H:%M:%S")]
    
    # Create a mapping from displayed time to datetime objects
    global time_mapping, time_mapping2, selectedTime, selectedTime2, pickupLocation, dropoffLocation
    time_mapping = dict(zip(time, timeVar))
    time_mapping2 = dict(zip(time2, timeVar2))

    selectedTime = ctk.StringVar()
    selectedTime2 = ctk.StringVar()

    today = datetime.today()
    pickupDate = DateEntry(detailsFrame, width=12, background='orange', foreground='white', borderwidth=2, font=("Skranji", 10), mindate=today, date_pattern='yyyy/MM/dd')
    pickupDate.bind("<<DateEntrySelected>>", lambda event: fetch_booking_and_price())
    pickupDate.place(x=positions["pickupDate"][0],y=positions["pickupDate"][1])
    if pDate != None:
        pickupDate.set_date(pDate)
    else:
        pickupDate.set_date(today)
    
    pickupTime = ctk.CTkComboBox(master=detailsFrame, width=90, state="readonly", values=time, variable=selectedTime, fg_color="#FFFFFF", font=("Skranji", 12))
    pickupTime.place(x=positions["pickupTime"][0],y=positions["pickupTime"][1])

    pickupLocation = ctk.CTkComboBox(master=detailsFrame, width=200, state="readonly", values=locations, fg_color="#FFFFFF", font=("Skranji", 12))
    pickupLocation.place(x=positions["pickupLocation"][0],y=positions["pickupLocation"][1])
    if plocation != None:
        pickupLocation.set(plocation)
        
    dropoffDate = DateEntry(detailsFrame, width=12, background='orange', foreground='white', borderwidth=2, font=("Skranji", 10), mindate=today, date_pattern='yyyy/MM/dd')
    dropoffDate.place(x=positions["dropoffDate"][0],y=positions["dropoffDate"][1])
    dropoffDate.bind("<<DateEntrySelected>>", lambda event: fetch_booking_and_price())
    if dDate != None:
        dropoffDate.set_date(dDate)
    else:
        dropoffDate.set_date(today)
    
    dropoffTime = ctk.CTkComboBox(master=detailsFrame, width=90, state="readonly", values=time2, variable=selectedTime2, fg_color="#FFFFFF", font=("Skranji", 12))
    dropoffTime.place(x=positions["dropoffTime"][0],y=positions["dropoffTime"][1])

    dropoffLocation = ctk.CTkComboBox(master=detailsFrame, width=200, state="readonly", values=locations, fg_color="#FFFFFF", font=("Skranji", 12))
    dropoffLocation.place(x=positions["dropoffLocation"][0],y=positions["dropoffLocation"][1])
    if dlocation != None:
        dropoffLocation.set(dlocation)

    dateInfo = ctk.CTkLabel(detailsFrame, text="* check whether the date is available", bg_color="#FFFFFF", fg_color="#FFFFFF", font=("Tw Cen MT",12))
    dateInfo.place(x=680, y=595)
    pywinstyles.set_opacity(dateInfo, color="#FFFFFF")
    checkDate = ctk.CTkButton(detailsFrame, text="Check Date", width=120, height=25, command=lambda:fetch_booking_data(pickupDate.get_date(),dropoffDate.get_date()))
    checkDate.place(x=695, y=578)

    if pDate != None and dDate != None:
        number_of_days = (dDate-pDate).days
    else:
        number_of_days = 0
    # Calculate the total amount
    global total_amount
    total_amount = carPrice * (number_of_days + 1)

    # Define positions for both small and large totalAmount displays
    total_amount_position_small = (1212, 497)  # Position for smaller text
    total_amount_position_large = (1225, 560)  # Position for larger, bold text

    global smallAmount, bigAmount
    # Display totalAmount in small font
    smallAmount = canvas.create_text(total_amount_position_small[0], total_amount_position_small[1], 
                    text=f"MYR {total_amount:.2f}", 
                    font=("Arial", 10), fill="black", anchor="e")

    # Display totalAmount in larger bold font
    bigAmount = canvas.create_text(total_amount_position_large[0], total_amount_position_large[1], 
                    text=f"MYR {total_amount:.2f}", 
                    font=("Arial", 23, "bold"), fill="black", anchor="e")

    # Back to Booking List button
    back_button = ctk.CTkButton(
        detailsFrame, text="< Booking Details", fg_color="#FFFFFF", bg_color="#FFFFFF", text_color="#000000", 
        width=200, height=40, font=("Tw Cen MT Condensed Extra Bold", 34), 
        command=lambda: open_listing(detailsFrame, list_callback)
    )
    back_button.place(x=20, y=125)

    global pfpState
    pfpState = 1

    pfp_img = ctk.CTkImage(Image.open(relative_to_assets("image_1.png")),size=(50,50))
    pfp_label = ctk.CTkButton(detailsFrame, image=pfp_img, text="", bg_color="#AC2A4B", fg_color="#AC2A4B",
                              width=50, height=50, command=lambda:accManage(detailsFrame,login_callback,profile_callback,review_callback))
    pfp_label.place(x=1203, y=20)
    pywinstyles.set_opacity(pfp_label,color="#AC2A4B")
    
    # Create the "Make Payment" button and place it on the canvas
    request_booking_button = tk.Button(detailsFrame, text="REQUEST BOOKING", font=("Arial", 19, "bold"), bd=0, width=17, bg="#FF865A", fg="black", 
                                       command=lambda:review_data(review_callback))
    request_booking_button.place(x=513, y=645)


def send_booking_email():
    try:
        # Fetch user and booking details based on booking_id
        conn = sqlite3.connect('CAR2U.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT BookingDetails.bookingID, BookingDetails.pickupLocation, BookingDetails.pickupDate, BookingDetails.pickupTime,
                BookingDetails.dropoffLocation, BookingDetails.dropoffDate, BookingDetails.dropoffTime,
                CarDetails.registrationNo, CarDetails.model, CarDetails.colour, CarDetails.fuelType, 
                CarDetails.seatingCapacity, CarDetails.transmissionType, CarDetails.price,
                RentalAgency.agencyName, RentalAgency.agencyLocation, RentalAgency.agencyContactNo,
                UserDetails.email,RentalAgency.agencyEmail
            FROM BookingDetails
            INNER JOIN CarDetails ON BookingDetails.carID = CarDetails.carID
            INNER JOIN RentalAgency ON CarDetails.agencyID = RentalAgency.agencyID
            INNER JOIN UserDetails ON BookingDetails.userID = UserDetails.userID
            WHERE BookingDetails.userID = ?
			ORDER BY BookingDetails.dateCreated DESC, BookingDetails.bookingID DESC
			LIMIT 1
        ''', (userInfo,))

        data = cursor.fetchone()
        conn.close()

        if data:
            # Unpack data
            (bookingID, pickupLocation, pickupDate, pickupTime, dropoffLocation, dropoffDate, dropoffTime, 
            registrationNo, model, colour, fuelType, seatingCapacity, transmissionType, 
            price, agencyName, agencyLocation, agencyContactNo, user_email,agency_email) = data

            # Send email
            sender_email = "cartwoyouofficial@gmail.com"
            sender_password = "kcft xbdi orcq awzn"

            try:
                # Email content
                subject = "Car Rental Booking Details Confirmation"
                body = f"""
                Dear Customer,
                Your booking request have been made. Here are your booking details: 
                Booking ID: {bookingID}

                Car Details:
                \tRegistration No: {registrationNo}
                \tModel: {model}
                \tColour: {colour}
                \tFuel Type: {fuelType}
                \tSeating Capacity: {seatingCapacity}
                \tTransmission Type: {transmissionType}
                \tPrice per day: MYR {price:.2f}

                Pickup & Dropoff Details:
                \tPickup: {pickupLocation}, {pickupDate}, {pickupTime}
                \tDropoff: {dropoffLocation}, {dropoffDate}, {dropoffTime}
        
                Agency Details:
                \tName: {agencyName}
                \tAddress: {agencyLocation}
                \tContact: {agencyContactNo}


                Your booking request wil be processed within 2 business days. An email will be sent upon approval to proceed with payment. 
                Thank you for choosing Car2U. We hope you have a pleasant experience with us.
                
                Best regards,
                Car2U Team
                """

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

                # Email content 2
                subject = "Car Rental Booking Request Pending"
                body = f"""
                Dear Renter,
                A booking request have been made. Here are the booking details: 
                Booking ID: {bookingID}

                Car Details: 
                \tRegistration No: {registrationNo}
                \tModel: {model}
                \tColour: {colour}
                \tFuel Type: {fuelType}
                \tSeating Capacity: {seatingCapacity}
                \tTransmission Type: {transmissionType}
                \tPrice per day: MYR {price:.2f}

                Pickup & Dropoff Details:
                \tPickup: {pickupLocation}, {pickupDate}, {pickupTime}
                \tDropoff: {dropoffLocation}, {dropoffDate}, {dropoffTime}
        
                Agency Details:
                \tName: {agencyName}
                \tAddress: {agencyLocation}
                \tContact: {agencyContactNo}

                
                Please response to this booking request as soon as possible (within 2 business days). Do check if the vehicle's condition is viable to rent out.
                Booking Rejections are only allowed when the car had an accident or is under maintenance, else a warning would be issued. 
                Thank You for cooperating.
                
                Best regards,
                Car2U Team
                """
                
                # Create email message
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = agency_email
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
    except Exception as e:
        print(f"Failed to send email: {e}")