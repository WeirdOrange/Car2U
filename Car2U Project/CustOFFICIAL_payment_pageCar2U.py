import sqlite3
import tkinter as tk
import customtkinter as ctk
import pywinstyles
import webbrowser  # Import webbrowser module
import smtplib
import easygui
from tkinter import messagebox, Toplevel, filedialog
from pathlib import Path
from PIL import Image, ImageTk
from MainCar2U_UserInfo import get_user_info,set_user_info,get_BookingInfo
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Set up the asset path
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U Project\assets\Cust-Payment")

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
        logout.place(x=30,y=195)
        pfpState = 0
    else:
        droptabFrame.destroy()
        pfpState = 1


# Function to fetch booking, user, and car details using userID and carID
def fetch_booking_user_car_details(booking_id):
    conn = sqlite3.connect('CAR2U.db')
    conn.row_factory = sqlite3.Row
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

# Function to upload receipt and save as BLOB in Transactions.receipt
def upload_receipt(transact_id,review_callback):
    # Open file dialog for image selection
    receipt_path = filedialog.askopenfilename(title="Select Receipt Image", 
                                              filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if receipt_path:
        # Convert image to binary for storage
        with open(receipt_path, 'rb') as file:
            receipt_blob = file.read()
        
        try:
            conn = sqlite3.connect('CAR2U.db')
            cursor = conn.cursor()
            
            # Update Transactions table with receipt blob
            cursor.execute('''
                UPDATE Transactions 
                SET receipt = ? 
                WHERE transactID = ?
            ''', (receipt_blob, transact_id))
            conn.commit()
            conn.close()
            easygui.msgbox("Receipt Uploaded", "Receipt has been uploaded successfully!")
            
            # Send confirmation email to the user
            send_confirmation_email(email, booking_details)

            # Reopen Review Page
            open_review(paymentFrame, review_callback)

        except sqlite3.Error as e:
            print("Failed to upload receipt:", e)
        finally:
            if conn:
                conn.close()
    else:
        messagebox.showinfo("No File Selected", "No receipt image was uploaded.")

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
    ''', (booking_id,))  

    # Fetch result as a tuple (price, numberOfDays)
    data = cursor.fetchone()
    conn.close()

    return data

# Function to update name, email, and contactNo in UserDetails table
def update_user_details(name, email, contactNo):
    try:
        conn = sqlite3.connect('CAR2U.db')
        cursor = conn.cursor()

        # Updating only name, email, and contactNo fields in UserDetails
        cursor.execute('''
            UPDATE UserDetails
            SET name = ?, email = ?, contactNo = ?
            WHERE userID = ?
        ''', (name, email, contactNo, userInfo))

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("An error occurred:", e)  # Print error if it fails
    finally:
        conn.close()

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
        print("Payment is recorded")  # Confirmation message
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

# Updated confirm_payment function to include receipt upload prompt
def confirm_payment(review_callback):
    # Get updated details from entry fields
    updated_name = entry_name.get()
    updated_contactNo = entry_contactNo.get()

    # Update user details in the database
    update_user_details(updated_name, email, updated_contactNo)

    # Calculate total amount if booking and price data are available
    if booking_and_price_data:
        total_amount = car_price * number_of_days

    # Add transaction details and get transactID
    if selected_payment and total_amount:
        transact_id = add_transaction(selected_payment, total_amount, booking_id)
        
        # Update BookingDetails with transactID if transactID was successfully returned
        if transact_id:
            try:
                conn = sqlite3.connect('CAR2U.db')
                cursor = conn.cursor()
                
                # Set transactID and bookingStatus to "Paid" if transactID exists
                cursor.execute('''
                    UPDATE BookingDetails
                    SET bookingStatus = 'Paid'
                    WHERE bookingID = ?
                ''', (booking_id,))
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
            except sqlite3.Error as e:
                print("An error occurred:", e)  # Print error if it fails
            finally:
                if conn:
                    conn.close()

            # Calculate total amount and map booking data to a dictionary
            total_amount = booking_data[7] * booking_data[17]
            global booking_details
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


        # Redirect to the appropriate payment page
        if selected_payment == "TNG":
            webbrowser.open("https://payment.tngdigital.com.my/sc/bDLnXXwSUR")
        elif selected_payment == "Bank":
            messagebox.showerror("Feature unavailable","We are sorry to say that this feature is still a work in progress.")
            #webbrowser.open("https://www.cimbclicks.com.my/clicks/#/")
        elif selected_payment == "Paypal":
            messagebox.showerror("Feature unavailable","We are sorry to say that this feature is still a work in progress.")
            #webbrowser.open("https://www.paypal.com/signin")

        # Show receipt upload prompt
        easygui.msgbox("Upload Receipt", "Please upload a receipt image for the transaction.")
        upload_receipt(transact_id,review_callback)

# Define actions for each button with image switching
def tng_action():
    global selected_payment
    selected_payment = "TNG"
    highlight_selected(tng, tng_clicked_photo)

def bank_action():
    global selected_payment
    messagebox.showerror("Feature unavailable","We are sorry to say that this feature is still a work in progress.")
    selected_payment = "Bank"
    highlight_selected(bank, bank_clicked_photo)

def card_action():
    global selected_payment
    messagebox.showerror("Feature unavailable","We are sorry to say that this feature is still a work in progress.")
    selected_payment = "Paypal"
    highlight_selected(card, paypal_clicked_photo)

# Function to highlight the selected button by changing the image and resetting others
def highlight_selected(selected_button, clicked_image):
    # Reset the images for all buttons to default
    tng.configure(image=tng_photo)
    bank.configure(image=bank_photo)
    card.configure(image=paypal_photo)

    # Change the selected button to the "clicked" version of the image
    selected_button.configure(image=clicked_image)

def paymentGUI(login_callback, home_callback, listing_callback, aboutUs_callback, profile_callback, review_callback):
    # Initialize main CustomTkinter window
    global paymentFrame
    paymentFrame = Toplevel()
    paymentFrame.title("Payment Page")
    paymentFrame.geometry("1280x720")
    paymentFrame.resizable(False,False)
    
    # Fetch details with a specific bookingID
    global booking_id, userInfo, pfpState
    booking_id = get_BookingInfo()
    print(booking_id)
    userInfo = get_user_info()
    pfpState = 1

    # Load and set the background image
    bg_photo = ctk.CTkImage(Image.open(relative_to_assets("Payment Page official.png")), size=(1280, 720))
    bg_label = ctk.CTkLabel(paymentFrame, width=1280, height=720, text="", image=bg_photo)
    bg_label.place(x=0, y=0)

    # Navigation Bar
    header = ctk.CTkFrame(paymentFrame, width=1280, height=60, fg_color="#FFFFFF")
    header.place(x=0, y=0)

    navbg_img = ctk.CTkImage(Image.open(relative_to_assets("nav.png")), size=(1280, 60))
    navbg_label = ctk.CTkLabel(header, image=navbg_img, text="")
    navbg_label.place(x=0, y=0)

    # Navigation buttons
    home_button = ctk.CTkButton(
        header, text="Home", width=120, bg_color="#FA5740", fg_color="#FA5740", text_color="#000000", 
        font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_home(paymentFrame, home_callback))
    home_button.place(x=627, y=14)
    pywinstyles.set_opacity(home_button,color="#F47749")

    selections_button = ctk.CTkButton(
        header, text="Selections", width=120, bg_color="#FB543F", fg_color="#FB543F", text_color="#000000",
        font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_listing(paymentFrame, listing_callback)
    )
    selections_button.place(x=763, y=14)
    pywinstyles.set_opacity(selections_button,color="#F47749")

    contact_us_button = ctk.CTkButton(
        header, text="Contact Us", width=120, bg_color="#FC503E", fg_color="#FC503E", text_color="#000000",
        font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: print("Contact Us clicked")
    )
    contact_us_button.place(x=910, y=14)
    pywinstyles.set_opacity(contact_us_button,color="#F47749")

    about_us_button = ctk.CTkButton(
        header, text="About Us", width=120, bg_color="#FC4D3D", fg_color="#FC4D3D", text_color="#000000",
        font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_aboutUs(paymentFrame, aboutUs_callback))
    about_us_button.place(x=1055, y=14)
    pywinstyles.set_opacity(about_us_button,color="#F47749")

    # Logo
    logo_img = ctk.CTkImage(Image.open(relative_to_assets("logo.png")), size=(75, 40))
    logo_label = ctk.CTkLabel(header, image=logo_img, text="", bg_color="#F47749", fg_color="#F47749", width=95, height=50)
    logo_label.place(x=5, y=5)
    pywinstyles.set_opacity(logo_label,color="#F47749")

    # Profile Picture Button
    pfp_img = ctk.CTkImage(Image.open(relative_to_assets("image_6.png")), size=(40, 40))
    pfp_button = ctk.CTkButton(header, image=pfp_img, text="", bg_color="#F47749", fg_color="#F47749", width=40, height=40,
                                command=lambda: accManage(paymentFrame, login_callback, profile_callback, review_callback))
    pfp_button.place(x=1180, y=5)
    pywinstyles.set_opacity(pfp_button,color="#F47749")

    # Back to Review button
    back_button = ctk.CTkButton(
        paymentFrame, text="< Payment", fg_color="#D4D6D4", bg_color="#D4D6D4", text_color="#000000", 
        width=200, height=40, font=("Tw Cen MT Condensed Extra Bold", 34), 
        command=lambda: open_review(paymentFrame, review_callback)
    )
    back_button.place(x=20, y=125)
    pywinstyles.set_opacity(back_button,color="#D4D6D4")
    
    details = fetch_booking_user_car_details(booking_id)

    # Fetch car price and number of days from the database
    global booking_and_price_data,car_price,number_of_days
    booking_and_price_data = fetch_booking_and_price()

    # Display total amount
    if booking_and_price_data:
        car_price, number_of_days = booking_and_price_data
        total_amount = car_price * number_of_days

        carPrice = ctk.CTkLabel(paymentFrame,text=f"MYR {car_price}", font=("Tw Cen MT", 14), text_color="black", width=90, height=20, anchor="e", 
                                   bg_color="#FFFFFF",fg_color="#FFFFFF")
        carPrice.place(x=627,y=434)
        pywinstyles.set_opacity(carPrice,color="#FFFFFF")

        numDays = ctk.CTkLabel(paymentFrame, text=f"{number_of_days} days", font=("Tw Cen MT", 14), text_color="black", width=90, height=20, anchor="e", 
                                   bg_color="#FFFFFF",fg_color="#FFFFFF")
        numDays.place(x=627,y=469)
        pywinstyles.set_opacity(numDays,color="#FFFFFF")

        # Small and bold font totals
        total_label_small = ctk.CTkLabel(
            paymentFrame, text=f"MYR {total_amount:.2f}", font=("Tw Cen MT", 14), text_color="black", width=90, height=20, anchor="e", 
                                   bg_color="#FFFFFF",fg_color="#FFFFFF"
        )
        total_label_small.place(x=627, y=503)
        pywinstyles.set_opacity(total_label_small,color="#FFFFFF")

        total_label_large = ctk.CTkLabel(
            paymentFrame, text=f"MYR {total_amount:.2f}", font=("Tw Cen MT Bold", 23), text_color="black", 
                                   bg_color="#FFFFFF",fg_color="#FFFFFF"
        )
        total_label_large.place(x=560, y=540)
        pywinstyles.set_opacity(total_label_large,color="#FFFFFF")

    # User and Booking Details
    global entry_name,entry_email,entry_contactNo
    if details:
        global email
        email = details[1]
        entry_name = ctk.CTkEntry(paymentFrame, font=("Sono", 14), text_color="black", placeholder_text="Name", width=266, height=40)
        entry_name.insert(0, details[0])
        entry_name.place(x=130, y=348)

        entry_email = ctk.CTkLabel(paymentFrame, font=("Sono", 14), text_color="black", text=details[1], width=266, height=40)
        entry_email.place(x=130, y=435)

        entry_contactNo = ctk.CTkEntry(paymentFrame, font=("Sono", 14), text_color="black", placeholder_text="Contact", width=266, height=40)
        entry_contactNo.insert(0, details[2])
        entry_contactNo.place(x=130, y=522)
        
        label_model = ctk.CTkLabel(paymentFrame, text=f"{details[3]}", font=("Tw Cen MT", 14), text_color="black", width=90, height=20, anchor="e", 
                                   bg_color="#FFFFFF",fg_color="#FFFFFF")
        label_model.place(x=627, y=399)
        pywinstyles.set_opacity(label_model,color="#FFFFFF")

    # Confirm Payment Button
    confirm_button = ctk.CTkButton(
        paymentFrame, text="CONFIRM PAYMENT", font=("Arial Bold", 23), fg_color="white", text_color="black", width=360, height=50, 
        command= lambda: confirm_payment(review_callback)
    )
    confirm_button.place(x=825, y=604)

    # Track the currently selected payment method
    selected_payment = None

    # Load default and clicked versions of TNG image
    global tng_photo,bank_photo,paypal_photo,tng_clicked_photo,bank_clicked_photo,paypal_clicked_photo
    tng_image = Image.open(relative_to_assets("tng button.png"))
    tng_image = tng_image.resize((305, 60), Image.Resampling.LANCZOS)
    tng_photo = ImageTk.PhotoImage(tng_image)

    tng_clicked_image = Image.open(relative_to_assets("tng click.png"))
    tng_clicked_image = tng_clicked_image.resize((305, 60), Image.Resampling.LANCZOS)
    tng_clicked_photo = ImageTk.PhotoImage(tng_clicked_image)

    # Load default and clicked versions of bank image
    bank_image = Image.open(relative_to_assets("online banking button.png"))
    bank_image = bank_image.resize((305, 60), Image.Resampling.LANCZOS)
    bank_photo = ImageTk.PhotoImage(bank_image)

    bank_clicked_image = Image.open(relative_to_assets("bank click.png"))
    bank_clicked_image = bank_clicked_image.resize((305, 60), Image.Resampling.LANCZOS)
    bank_clicked_photo = ImageTk.PhotoImage(bank_clicked_image)

    # Load default and clicked versions of card image
    paypal_image = Image.open(relative_to_assets("paypal button.png"))
    paypal_image = paypal_image.resize((305, 60), Image.Resampling.LANCZOS)
    paypal_photo = ImageTk.PhotoImage(paypal_image)

    paypal_clicked_image = Image.open(relative_to_assets("paypal clicked.png"))
    paypal_clicked_image = paypal_clicked_image.resize((305, 60), Image.Resampling.LANCZOS)
    paypal_clicked_photo = ImageTk.PhotoImage(paypal_clicked_image)

    # Payment Method Buttons
    global tng,bank,card
    tng = ctk.CTkButton(paymentFrame, image=tng_photo, text="", command=tng_action, bg_color="#FFFFFF")
    tng.place(x=854, y=312)

    bank = ctk.CTkButton(paymentFrame, image=bank_photo, text="", command=bank_action, bg_color="#FFFFFF")
    bank.place(x=854, y=382)

    card = ctk.CTkButton(paymentFrame, image=paypal_photo, text="", command=card_action, bg_color="#FFFFFF")
    card.place(x=854, y=452)
