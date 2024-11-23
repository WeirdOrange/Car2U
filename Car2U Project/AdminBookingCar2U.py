import customtkinter as ctk
import pywinstyles
import sqlite3
import smtplib
import ssl
from easygui import buttonbox
from email.message import EmailMessage
from MainCar2U_UserInfo import get_user_info,set_user_info
from tkinter import Toplevel, ttk, messagebox, PhotoImage
from PIL import Image, ImageTk
from pathlib import Path
from io import BytesIO

# Set up the asset path (same as original)
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Admin-Booking")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def Database(): #creating connection to database and creating table
    global conn, cursor
    conn = sqlite3.connect("car2u.db")

# Function to handle login button click
def open_login(current_window, login_callback):
    current_window.destroy()  # Close the window
    userInfo = ""
    set_user_info(userInfo)
    login_callback()

# Function to handle selection button click
def open_home(current_window, home_callback):
    current_window.destroy()  # Close the window
    home_callback()

# Function to handle bookings button click
def open_bookings():
    messagebox.showinfo("You are on the Home page")

# Function to handle profile button click
def open_profile(current_window, profile_callback):
    current_window.destroy()  # Close the window
    profile_callback()

# Function to handle car details button click
def open_Cdetail(current_window, detail_callback):
    current_window.destroy()  # Close the window
    detail_callback()

# Function to handle chats button click
def open_chat(current_window, chat_callback):
    current_window.destroy()  # Close the window
    chat_callback()

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
   
def convert_data(data):
    global receiptIMG
    img_byte = BytesIO(data)
    img = Image.open(img_byte)
    return img
    
# Email notification
def emailNotif(email_receiver,subject,body):
    # Define email sender and receiver
    email_sender = 'cartwoyouofficial@gmail.com'
    email_password = 'asjy kqjh eizl wgnu'

    # Set up the email
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

# Function to refresh treeview
def refresh_Pending_treeview():
    for row in pendingTreeview.get_children():
        pendingTreeview.delete(row)

    Database()
    cursor = conn.cursor()
    cursor.execute("""SELECT bookingID,registrationNo,model,email,pickupDate,pickupTime,dropoffDate,dropoffTime,bookingRemark,bookingStatus
                        FROM BookingDetails B
                        INNER JOIN CarDetails C ON B.carID = C.carID
                        INNER JOIN UserDetails U ON B.userID = U.userID
						WHERE bookingStatus = 'Pending' AND agencyID = ?""", (userinfo,))
    result = cursor.fetchall()
    conn.commit()
    conn.close()

    for row in result:
        pendingTreeview.insert("", "end", values=row)

# Function to refresh Booking History Treeview
def refresh_history_treeview():
    for row in historyTreeview.get_children():
        historyTreeview.delete(row)

    try:
        # Fetch the selected car details from the database (including image path)
        Database()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT B.bookingID,C.registrationNo,CONCAT(CAST(B.pickupDate AS CHAR),' till ', CAST(B.dropoffDate AS CHAR)) AS period,B.bookingStatus
                            FROM BookingDetails B
                            INNER JOIN CarDetails C ON B.carID = C.carID
                            WHERE agencyID = ?''', (userinfo,))
        booking_data = cursor.fetchall()
        
        # First Layer
        historyTreeview.insert('', '0', 'h1', text ='Rented')
        historyTreeview.insert('', '1', 'h2', text ='Rejected / Cancelled')
        
        global bookingID,carNo,historyPeriod,bookingStatus
        for row in booking_data:
            bookingID = row[0]
            carNo = row[1]
            historyPeriod = row[2]
            bookingStatus = row[3]

            if bookingStatus == "Rented":
                carNoKey = carNo+"Rented"
                if not historyTreeview.exists(carNoKey):
                    historyTreeview.insert('', '2', carNoKey, text = carNo) # Rented
                historyTreeview.insert(carNoKey, 'end', bookingID, text = historyPeriod)
                historyTreeview.move(carNoKey, 'h1', 'end')
            elif bookingStatus == "Rejected" or bookingStatus == "Cancelled":
                carNoKey = carNo+"Cancelled"
                if not historyTreeview.exists(carNoKey):
                    historyTreeview.insert('', '3', carNoKey, text = carNo) # Rejected
                historyTreeview.insert(carNoKey, 'end', bookingID, text = historyPeriod)
                historyTreeview.move(carNoKey, 'h2', 'end')
            else:
                continue

    except sqlite3.Error as e:
        messagebox.showerror("Error", "Error occurred during registration: {}".format(e))
    finally:
        conn.close()
    
# Function to refresh Current Bookings Treeview
def refresh_currentTreeview():
    for row in currentTreeview.get_children():
        currentTreeview.delete(row)

    try:
        # Fetch the selected car details from the database (including image path)
        Database()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT B.bookingID,C.registrationNo,B.pickupDate,B.pickupTime,B.bookingStatus
                            FROM BookingDetails B
                            INNER JOIN CarDetails C ON B.carID = C.carID
                            WHERE agencyID = ? AND bookingStatus IN ('Approved','On Rent','Paid')
                            ORDER BY pickupDate''', (userinfo,))
        current_data = cursor.fetchall()
        
        i=0
        global bookingID,carNo,historyPeriod,bookingStatus
        for row in current_data:
            bookingID = str(row[0])
            carNo = str(row[1])
            pickDate = str(row[2])
            pickTime = str(row[3])
            
            carInfo = str(carNo)+' || '+str(pickTime)

            if not currentTreeview.exists(pickDate):
                currentTreeview.insert('', i, pickDate, text = pickDate)
            currentTreeview.insert(pickDate, 'end', bookingID, text = carInfo)
            i += 1
        
        if current_data == None:
            currentTreeview.insert('', '1', 'empty', text = "No more bookings")

    except sqlite3.Error as e:
        messagebox.showerror("Error", "Error occurred during registration: {}".format(e))
    finally:
        conn.close()

def select_item(event):
    global bookingID
    selected_treeview = event.widget
    selected_item = selected_treeview.selection()
    if selected_item:
        try:
            item = pendingTreeview.item(selected_item)
            values = item['values']
            bookingID = values[0]  # Get the ID of the selected car
        except:
            bookingID = selected_item[0] 

        try:
            # Fetch the selected car details from the database (including image path)
            Database()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''SELECT C.model,C.registrationNo,B.bookingRemark,
                            CONCAT(CAST(B.pickupDate AS CHAR), ' till ', CAST(B.dropoffDate AS CHAR)) AS period,
                            U.name,U.email,U.contactNo,B.bookingStatus,B.totalAmount,B.pickupLocation,
                            B.dropoffLocation,B.pickupTime,B.dropoffTime,B.bookingID,C.seatingCapacity,T.transactID,T.receipt, C.carImage
                            FROM BookingDetails B
                            INNER JOIN CarDetails C ON B.carID = C.carID
                            INNER JOIN UserDetails U ON B.userID = U.userID
                            LEFT JOIN transactions T ON B.bookingID = T.bookingID
                            WHERE B.bookingID = ?''', (bookingID,))
            car_data = cursor.fetchall()

            for widget in detailsFrame.winfo_children():
                if isinstance(widget, (ctk.CTkFrame,ctk.CTkButton)):
                    widget.destroy()
            # Car Content
            global model,carNo,addons,period,custName,email,contact,status,price,pickup,dropoff,pickTime,dropTime,seats,payStatus,receiptIMG,carImage
            for row in car_data:
                model = row[0]
                carNo = row[1]
                addons = row[2]
                if addons == "":
                    addons = "None"
                period = row[3]
                # Customer Content
                custName = row[4]
                email = row[5]
                contact = row[6]
                # Payments
                status = row[7]
                price = row[8]
                # Locatime & Time
                pickup = row[9]
                dropoff = row[10]
                pickTime = row[11]
                dropTime = row[12]
                bookingID = row[13]
                seats = row[14] if row[14] is not None else "N/A"
                payStatus = row[15]
                if payStatus == None:
                    payStatus = "Pending"
                else:
                    payStatus = "Done"
                receipt = row[16]
                if receipt != None:
                    img = convert_data(receipt)
                    receiptIMG = ctk.CTkImage(light_image=img, size=(280,480))
                else:
                    receiptIMG = ""

                car = row[17]
                if car != None:
                    img = convert_data(car)
                    carImage = ctk.CTkImage(light_image=img, size=(200,100))
                else:
                    carImage = ""
            refresh_detail()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            messagebox.showerror("Error", f"Error occurred during registration: {e}")
        except Exception as e:
            print(f"General error: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

        except sqlite3.Error as e:
            messagebox.showerror("Error", "Error occurred during registration: {}".format(e))
        finally:
            conn.close()

        return model,carNo,addons,period,custName,email,contact,status,price,pickup,dropoff,pickTime,dropTime,seats,payStatus,receiptIMG

def showReceipt():
    receiptFrame = Toplevel()
    receiptFrame.title("Receipt Evidence")
    receipt = ctk.CTkLabel(receiptFrame,width=480,height=480,text="", image=receiptIMG)
    receipt.place(x=0,y=0)

# Function to refresh booking details selected
def refresh_detail():
    for widget in detailsFrame.winfo_children():
        if isinstance(widget, (ctk.CTkFrame,ctk.CTkLabel,ctk.CTkButton)):
            widget.destroy()
            
    detail_title = ctk.CTkLabel(detailsFrame, text="Booking Details", font=("Segoe UI Bold",24))
    detail_title.place(x=280,y=5)

    global model,carNo,addons,period,custName,email,contact,status,price,pickup,dropoff,pickTime,dropTime,seats,payStatus,receiptIMG,carImage
    # Placeholder for car image
    if carImage:
        car_image = ctk.CTkLabel(detailsFrame, text="", image=carImage, width=200, height=100, fg_color="#D9D9D9", bg_color="#D9D9D9")
        car_image.place(x=50, y=45)
    else:
        car_image = ctk.CTkLabel(detailsFrame, text="Car Photo", width=200, height=100, fg_color="#D9D9D9", bg_color="#D9D9D9")
        car_image.place(x=50, y=45)

    statusTitle = ctk.CTkLabel(detailsFrame,text="Booking Status:",width=140,height=21,anchor='center', font=("Segoe UI Bold",16))
    statusTitle.place(x=300,y=45)
    statusFrame = ctk.CTkFrame(detailsFrame,width=140, height=30)
    statusFrame.place(x=300,y=70)
    
    costTitle = ctk.CTkLabel(detailsFrame,text="Total Cost:",width=95,height=21,anchor='center', font=("Segoe UI Bold",16))
    costTitle.place(x=450,y=45)
    costFrame = ctk.CTkFrame(detailsFrame,width=95, height=30)
    costFrame.place(x=460,y=70)
    costContent = ctk.CTkLabel(costFrame, text="RM "+str(price), font=("Segoe UI Bold",12))
    costContent.place(x=5,y=0)

    car_label = {"Model:":155,"Car No:":185,"Add Ons:":215,"Period:":255}
    car_contents = {model:155,carNo:185}
    cust_labels = {}
    for key,value in car_label.items():
        label = ctk.CTkLabel(detailsFrame, text=key, width=95, anchor="e", font=("Segoe UI",12))
        label.place(x=15,y=value)
    for key,value in car_contents.items():
        contentFrame = ctk.CTkFrame(detailsFrame, width=130, height=23)
        contentFrame.place(x=115,y=value)
        cust_labels[key] = ctk.CTkLabel(contentFrame, text=str(key), anchor="e", font=("Segoe UI",11))
        cust_labels[key].place(x=5,y=0)
    
    addOnFrame = ctk.CTkFrame(detailsFrame, width=130, height=35)
    addOnFrame.place(x=115,y=215)
    addOnLabel = ctk.CTkLabel(addOnFrame, text=str(addons), anchor="e", font=("Segoe UI",11))
    addOnLabel.place(x=5,y=0)

    periodFrame = ctk.CTkFrame(detailsFrame, width=130, height=35)
    periodFrame.place(x=115,y=255)
    periodLabel = ctk.CTkLabel(periodFrame, text=str(period), anchor="e", font=("Segoe UI",11))
    periodLabel.place(x=5,y=0)
    
    cust_label = {"Customer Name:":305,"Email:":335,"Contact no:":365}
    cust_contents = {custName:310,email:340,contact:370}
    cust_content_labels = {}
    for key,value in cust_label.items():
        label = ctk.CTkLabel(detailsFrame, text=key, width=95, anchor="e", font=("Segoe UI",12))
        label.place(x=15,y=value)
    for key,value in cust_contents.items():
        contentFrame = ctk.CTkFrame(detailsFrame, width=130, height=23)
        contentFrame.place(x=115,y=value)
        cust_content_labels[key] = ctk.CTkLabel(contentFrame, text=str(key), anchor="e", font=("Segoe UI",11))
        cust_content_labels[key].place(x=5,y=0)

    showPickup = ctk.CTkLabel(detailsFrame, text="Pick-Up Location:", fg_color="#FFFFFF", width=140, anchor="center", font=("Segoe UI",14))
    showPickup.place(x=300,y=115)

    pickupFrame = ctk.CTkFrame(detailsFrame,width=250, height=55)
    pickupFrame.place(x=300,y=140)
    pickupContent = ctk.CTkLabel(pickupFrame, text=str(pickup), font=("Segoe UI",14), wraplength=250)
    pickupContent.place(x=5,y=0)

    pickTimeLabel = ctk.CTkLabel(detailsFrame, text="Time:", fg_color="#FFFFFF", width=65, height=30, anchor="center", font=("Segoe UI",14))
    pickTimeLabel.place(x=570,y=115)
    pickTimeFrame = ctk.CTkFrame(detailsFrame,width=125, height=30)
    pickTimeFrame.place(x=570,y=140)
    pickTimeContent = ctk.CTkLabel(pickTimeFrame, text=str(pickTime), anchor='center', font=("Segoe UI",14))
    pickTimeContent.place(x=2,y=0)
    
    showDropOff = ctk.CTkLabel(detailsFrame, text="Drop-Off Location:", width=140, anchor="center", font=("Segoe UI",14))
    showDropOff.place(x=300,y=200)

    dropFrame = ctk.CTkFrame(detailsFrame,width=250, height=55)
    dropFrame.place(x=300,y=230)
    dropContent = ctk.CTkLabel(dropFrame, text=str(dropoff), font=("Segoe UI",14), wraplength=140)
    dropContent.place(x=5,y=0)

    dropTimeLabel = ctk.CTkLabel(detailsFrame, text="Time:", width=65, height=30, anchor="center", font=("Segoe UI",14))
    dropTimeLabel.place(x=570,y=200)
    dropTimeFrame = ctk.CTkFrame(detailsFrame,width=125, height=30)
    dropTimeFrame.place(x=570,y=230)
    dropTimeContent = ctk.CTkLabel(dropTimeFrame, text=str(dropTime), anchor='center', font=("Segoe UI",14))
    dropTimeContent.place(x=2,y=0)

    remarkTitle = ctk.CTkLabel(detailsFrame, text="Remark:", font=("Segoe UI",14))
    remarkTitle.place(x=300,y=295)

    remarkFrameContent = ctk.CTkEntry(detailsFrame,width=200, height=50, font=("Segoe UI",12))
    remarkFrameContent.place(x=300,y=325)

    if status == "Pending":
        statusContent = ctk.CTkLabel(statusFrame,width=140, height=30, text=str(status), font=("Segoe UI Bold",12), anchor="center")
        statusContent.place(x=0,y=0)
        statusFrame.configure(fg_color="#FFBE71")
        
        acceptBttn = ctk.CTkButton(detailsFrame,width=110,height=35, text="Accept", text_color="#FFFFFF", fg_color="#5DC122", font=("Segoe UI Bold",16),
                                command=lambda:approveBooking(remarkFrameContent.get()))
        acceptBttn.place(x=250, y=415)
        
        rejectBttn = ctk.CTkButton(detailsFrame,width=110,height=35, text="Reject", text_color="#FFFFFF", fg_color="#FE453B", font=("Segoe UI Bold",16),
                                command=lambda:rejectBooking(remarkFrameContent.get()))
        rejectBttn.place(x=390, y=415)
    elif status == "Rejected" or status == "Cancelled":
        statusContent = ctk.CTkLabel(statusFrame,width=140, height=30, text=str(status), font=("Segoe UI Bold",12), fg_color="#FE453B", anchor="center")
        statusContent.place(x=0,y=0)
        statusFrame.configure(fg_color="#FFBE71")

        editBttn = ctk.CTkButton(detailsFrame,width=110,height=35, text="Edit Remark", text_color="#FFFFFF", fg_color="#5DC122", font=("Segoe UI Bold",16),
                                command=lambda:rejectBooking(remarkFrameContent.get()))
        editBttn.place(x=250, y=415)
    elif status == "Approved" or status == "Paid":
        statusContent = ctk.CTkLabel(statusFrame,width=140, height=30, text=str(status), font=("Segoe UI Bold",12), fg_color="#46D1CA", anchor="center")
        statusContent.place(x=0,y=0)
        statusFrame.configure(fg_color="#FFBE71")

        paymentTitle = ctk.CTkLabel(detailsFrame, text="Payment Status:", width=126, font=("Segoe UI Bold",16))
        paymentTitle.place(x=570,y=45)

        if payStatus == "Pending":
            paymentStatus = ctk.CTkLabel(detailsFrame,text=payStatus, bg_color="#FFFFFF", fg_color="#FFA843", width=65, height=30, anchor="center", corner_radius=10)
            paymentStatus.place(x=570,y=70)
        else:
            paymentStatus = ctk.CTkLabel(detailsFrame,text=payStatus, bg_color="#FFFFFF", fg_color="#5DC122", width=65, height=30, anchor="center", corner_radius=10)
            paymentStatus.place(x=570,y=70)
            
            receiptButton = ctk.CTkButton(detailsFrame, text="View Receipt", width=80, height=30,command=lambda:showReceipt())
            receiptButton.place(x=640,y=70)
        paymentStatus.place(x=570,y=70)

        editBttn = ctk.CTkButton(detailsFrame,width=110,height=35, text="Edit Remark", text_color="#FFFFFF", fg_color="#5DC122", font=("Segoe UI Bold",16),
                                command=lambda:approveBooking(remarkFrameContent.get()))
        editBttn.place(x=250, y=415)

        rentedBttn = ctk.CTkButton(detailsFrame,width=110,height=35, text="On Rent", text_color="#FFFFFF", fg_color="#5DC122", font=("Segoe UI Bold",16),
                                command=lambda:onRent(remarkFrameContent.get()))
        rentedBttn.place(x=390, y=415)
        
        rejectBttn = ctk.CTkButton(detailsFrame,width=110,height=35, text="Reject", text_color="#FFFFFF", fg_color="#FE453B", font=("Segoe UI Bold",16),
                                command=lambda:rejectBooking(remarkFrameContent.get()))
        rejectBttn.place(x=530, y=415)
    elif status == "On Rent":
        statusContent = ctk.CTkLabel(statusFrame,width=140, height=30, text=str(status), font=("Segoe UI Bold",12), fg_color="#80F67C", anchor="center")
        statusContent.place(x=0,y=0)
        statusFrame.configure(fg_color="#FFBE71")

        paymentTitle = ctk.CTkLabel(detailsFrame, text="Payment Status:", width=126, font=("Segoe UI Bold",16))
        paymentTitle.place(x=570,y=45)

        if payStatus == "Pending":
            paymentStatus = ctk.CTkLabel(detailsFrame,text=payStatus, bg_color="#FFFFFF", fg_color="#FFA843", width=65, height=30, anchor="center", corner_radius=10)
            paymentStatus.place(x=570,y=70)
        else:
            paymentStatus = ctk.CTkLabel(detailsFrame,text=payStatus, bg_color="#FFFFFF", fg_color="#5DC122", width=65, height=30, anchor="center", corner_radius=10)
            paymentStatus.place(x=570,y=70)
            receiptButton = ctk.CTkButton(detailsFrame, text="View Receipt", width=80, height=30,command=lambda:showReceipt())
            receiptButton.place(x=640,y=70)
        
        editBttn = ctk.CTkButton(detailsFrame,width=110,height=35, text="Edit Remark", text_color="#FFFFFF", fg_color="#5DC122", font=("Segoe UI Bold",16),
                                command=lambda:onRent(remarkFrameContent.get()))
        editBttn.place(x=250, y=415)

        rentedBttn = ctk.CTkButton(detailsFrame,width=110,height=35, text="Completed", text_color="#FFFFFF", fg_color="#5DC122", font=("Segoe UI Bold",16),
                                command=lambda:rentDone(remarkFrameContent.get()))
        rentedBttn.place(x=390,y=415)
    else:
        statusContent = ctk.CTkLabel(statusFrame,width=140, height=30, text=str(status), font=("Segoe UI Bold",12), fg_color="#00C140", anchor="center")
        statusContent.place(x=0,y=0)
        
        editBttn = ctk.CTkButton(detailsFrame,width=110,height=35, text="Edit Remark", text_color="#FFFFFF", fg_color="#5DC122", font=("Segoe UI Bold",16),
                                command=lambda:rentDone(remarkFrameContent.get()))
        editBttn.place(x=250, y=415)


def approveBooking(remark):
    print("Booking Accepted")
    try:
        Database()
        cursor = conn.cursor()
        cursor.execute('''UPDATE BookingDetails SET bookingStatus = "Approved", bookingRemark = ?
                            WHERE bookingID = ?''', (remark,bookingID,))
        conn.commit()
        messagebox.showinfo("Booking Approved", "You have approved the booking. Remember to mark your calendar!")

        subject = "Car Rental Booking Approved"
        body = str(f"""Hi {custName},\nGreat News! Your reservation booking to rent the {model}, {carNo}, has been approved!
                   \nPlease proceed to Payment from booking history and pay for the rental.
                   \nReminder: Do pay for the car rental at least a day before the car rental date, the booking will be automatically rejected if booking is not paid
                   \n\nBest regards,\nCar2U Team""")
        emailNotif(email,subject,body)
        refresh_currentTreeview()
        select_item

    except sqlite3.Error as e:
        messagebox.showerror("Error", "Error occurred during editing: {}".format(e))
    finally:
        conn.close()
        
def rejectBooking(remark):
    print("Booking Rejected")
    if remark == None:
        messagebox.showinfo("Rejecting a booking", "Please leave a remark on why are you rejecting the booking.")
    else:
        try:
            Database()
            cursor = conn.cursor()
            cursor.execute('''UPDATE BookingDetails SET bookingStatus = "Rejected", bookingRemark = ?
                                WHERE bookingID = ?''', (remark,bookingID,))
            conn.commit()
            messagebox.showinfo("Booking Rejected", "Oh! It seems you have rejected the booking. If this was a mistake, please contact Car2U service.")
            
            subject = "Car Rental Booking Rejected"
            body = f"""Hi {custName},\nWe are sorry to say that your reservation booking to rent the {model}, {carNo}, has been rejected. 
                    \n\nRenter's Rejection Remark: {remark}
                    \n\nLate payment or sudden maintenance required for the car may had happened, 
                    do contact the rental agency or contact our customer service line to have a better understanding of what happened.\n\nBest regards,\nCar2U Team"""
            emailNotif(email,subject,body)
            refresh_currentTreeview()
            refresh_history_treeview()
            select_item

        except sqlite3.Error as e:
            messagebox.showerror("Error", "Error occurred during editing: {}".format(e))
        finally:
            conn.close()

def onRent(remark):
    print("Renting")
    try:
        Database()
        cursor = conn.cursor()
        cursor.execute('''UPDATE BookingDetails SET bookingStatus = "On Rent", bookingRemark = ?
                            WHERE bookingID = ?''', (remark,bookingID,))
        conn.commit()
        messagebox.showinfo("Booking On Rent", "The vehicle has been rented out, awaiting return...")
        refresh_currentTreeview()
        select_item

    except sqlite3.Error as e:
        messagebox.showerror("Error", "Error occurred during editing: {}".format(e))
    finally:
        conn.close()

def rentDone(remark):
    print("Renting Completed")
    try:
        Database()
        cursor = conn.cursor()
        cursor.execute('''UPDATE BookingDetails SET bookingStatus = "Rented", bookingRemark = ?
                            WHERE bookingID = ?''', (remark,bookingID,))
        conn.commit()
        messagebox.showinfo("Rental Completed", "Success! You have completed the rental request")
        refresh_history_treeview()
        refresh_currentTreeview()
        select_item

    except sqlite3.Error as e:
        messagebox.showerror("Error", "Error occurred during editing: {}".format(e))
    finally:
        conn.close()

def carBooking(login_callback,home_callback,detail_callback,profile_callback,chat_callback):
    # Create the main application window
    global aBookingFrame
    aBookingFrame = Toplevel()
    aBookingFrame.title("Admin Bookings")
    aBookingFrame.geometry("1280x720")
    aBookingFrame.resizable(False, False)
    aBookingFrame.config(bg="white")

    # Linking user data
    global userinfo
    userinfo = get_user_info()
    
    bg_img = ctk.CTkImage(Image.open(relative_to_assets("admin_bg.png")),size=(1280,720))
    bg_label = ctk.CTkLabel(aBookingFrame, image=bg_img,text="")
    bg_label.place(x=0, y=0)

    # Navigation Tab
    nav_img = ctk.CTkImage(Image.open(relative_to_assets("nav.png")),size=(200,720))
    nav_label = ctk.CTkLabel(aBookingFrame, image=nav_img, text="")
    nav_label.place(x=0, y=0)

    logo_img = ctk.CTkImage(Image.open(relative_to_assets("Logo.png")),size=(150,60))
    logo_label = ctk.CTkLabel(aBookingFrame, image=logo_img, text="", bg_color="#F47749", width=95, height=50)
    logo_label.place(x=22, y=10)
    pywinstyles.set_opacity(logo_label,color="#F47749")
    
    global pfpState
    pfpState = 1
    pfp_img = ctk.CTkImage(Image.open(relative_to_assets("image_4.png")),size=(100,100))
    pfp_label = ctk.CTkButton(aBookingFrame, image=pfp_img, text="", bg_color="#FE453B", fg_color="#FE453B",
                              width=40, height=40, command=lambda:accManage(aBookingFrame,login_callback,profile_callback))
    pfp_label.place(x=41, y=590)
    pywinstyles.set_opacity(pfp_label,color="#FE453B")

    # Relocate buttons
    home_button = ctk.CTkButton(master=aBookingFrame, text="Home", width=120, fg_color=("#F95C41","#FA5740"), bg_color="#FA5740", 
                                text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_home(aBookingFrame,home_callback))
    home_button.place(x=22, y=100)
    pywinstyles.set_opacity(home_button,color="#FA5740")

    booking_button = ctk.CTkButton(master=aBookingFrame, text="Bookings", width=120, fg_color=("#FA5740","#FB543F"), bg_color="#FB543F", 
                                      text_color="#FFF6F6", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda:open_bookings())
    booking_button.place(x=22, y=165)
    pywinstyles.set_opacity(booking_button,color="#FB543F")

    inventory_button = ctk.CTkButton(master=aBookingFrame, text="Inventory", width=120, fg_color=("#FB543F","#FC503E"), bg_color="#FC503E", 
                                      text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), 
                                      command=lambda: open_Cdetail(aBookingFrame, detail_callback))
    inventory_button.place(x=22, y=230)
    pywinstyles.set_opacity(inventory_button,color="#FC503E")

    chat_button = ctk.CTkButton(master=aBookingFrame, text="Chat", width=120, fg_color=("#FC503E","#FC4D3D"), bg_color="#FC4D3D", 
                                    text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_chat(aBookingFrame, chat_callback))
    chat_button.place(x=22, y=295)
    pywinstyles.set_opacity(chat_button,color="#FC4D3D")


    # Pending Bookings Section
    pending_label = ctk.CTkLabel(aBookingFrame, text="Pending Request", bg_color="#F47749", width=230, font=("Segoe UI Bold",24))
    pending_label.place(x=240, y=15)

    pendingFrame = ctk.CTkFrame(aBookingFrame, width=995, height=145,corner_radius=10, bg_color="#000000")
    pendingFrame.place(x=230,y=50)
    
    # Treeview for displaying saved data
    global pendingTreeview
    columns = ('bookingID', 'Car No', 'Car Model', 'Email', 'pickupDate', 'pickupTime', 'dropoffDate', 'dropoffTime', 'Remark', 'Status')
    pendingTreeview = ttk.Treeview(pendingFrame, columns=columns, show='headings', height=7)

    # Define the headings
    for col in columns:
        pendingTreeview.heading(col, text=col.capitalize())
        pendingTreeview.column(col, anchor='center', width=100)  # Adjust width as needed

    # Create scrollbars
    v_scrollbar = ttk.Scrollbar(pendingFrame, orient="vertical", command=pendingTreeview.yview)
    pendingTreeview.configure(yscrollcommand=v_scrollbar.set)

    # Position the Treeview and scrollbars using grid
    pendingTreeview.grid(row=0, column=0, sticky="nsew")
    v_scrollbar.grid(row=0, column=1, sticky="ns")

    # Configure grid layout to make the treeview expand with the frame
    pendingFrame.grid_rowconfigure(0, weight=1)
    pendingFrame.grid_columnconfigure(0, weight=1)
    pendingTreeview.bind("<<TreeviewSelect>>", select_item)
    refresh_Pending_treeview()

    
    # Booking History Section
    history_label = ctk.CTkLabel(aBookingFrame, text="Booking History", bg_color="#F47749", width=230, anchor='center', font=("Segoe UI Bold",24))
    history_label.place(x=230, y=470)
    
    historyFrame = ctk.CTkFrame(aBookingFrame, width=230, height=190,corner_radius=10, fg_color="#FFFFFF", bg_color="#FFFFFF",border_color="#000000",border_width=2)
    historyFrame.place(x=240,y=505)

    ##Treeview widget data
    global historyTreeview
    historyTreeview = ttk.Treeview(historyFrame, show="tree")
    historyTreeview.grid(padx=2)
    historyTreeview.bind("<<TreeviewSelect>>", select_item)
    refresh_history_treeview()

    # Create scrollbars
    v_scrollbar = ttk.Scrollbar(historyFrame, orient="vertical", command=historyTreeview.yview)
    historyTreeview.configure(yscrollcommand=v_scrollbar.set)

    # Position the Treeview and scrollbars using grid
    historyTreeview.grid(row=0, column=0, sticky="nsew")
    v_scrollbar.grid(row=0, column=1, sticky="ns")

    # Configure grid layout to make the treeview expand with the frame
    historyTreeview.grid_columnconfigure(0, weight=1)


    # Booking Details Section
    global detailsFrame
    detailsFrame = ctk.CTkFrame(aBookingFrame, width=745, height=470, corner_radius=10, fg_color="#FFFFFF", bg_color="#FFFFFF",border_color="#000000",border_width=2)
    detailsFrame.place(x=480,y=225)

    detail_title = ctk.CTkLabel(detailsFrame, text="Booking Details", font=("Segoe UI Bold",24))
    detail_title.place(x=280,y=5)
    
    global status,price,model,carNo,addons,period,custName,email,contact,pickup,dropoff,pickTime,dropTime
    # Payments
    status = "-"
    price = "RM -"
    # Car Content holder
    model = "Select Booking"
    carNo = "Select Booking "
    addons = "Select Booking  "
    period = "Select Booking  "
    # Customer Content holder
    custName = "Select Booking   "
    email = "Select Booking    "
    contact = "Select Booking     "
    # pick/drop location & time
    pickup = "-Select A Booking- "
    dropoff = "-Select A Booking-"
    pickTime = "Time"
    dropTime = "Time "

    #refresh_detail()

    #Current History Section
    current_label = ctk.CTkLabel(aBookingFrame, text="Current Bookings", bg_color="#F47749", width=230, anchor='center', font=("Segoe UI Bold",24))
    current_label.place(x=230, y=225)
    
    currentFrame = ctk.CTkFrame(aBookingFrame, width=230, height=180,corner_radius=10, fg_color="#FFFFFF", bg_color="#FFFFFF", border_color="#000000", border_width=2)
    currentFrame.place(x=240,y=260)

    ##Treeview widget data
    global currentTreeview
    currentPeriod = "yyyy-mm-dd"
    currentTreeview = ttk.Treeview(currentFrame, show="tree")
    currentTreeview.grid(padx=2)
    currentTreeview.bind("<<TreeviewSelect>>", select_item)
    refresh_currentTreeview()

    # Create scrollbars
    v_scrollbar = ttk.Scrollbar(currentFrame, orient="vertical", command=currentTreeview.yview)
    currentTreeview.configure(yscrollcommand=v_scrollbar.set)

    # Position the Treeview and scrollbars using grid
    currentTreeview.grid(row=0, column=0, sticky="nsew")
    v_scrollbar.grid(row=0, column=1, sticky="ns")

    # Configure grid layout to make the treeview expand with the frame
    currentTreeview.grid_columnconfigure(0, weight=1)