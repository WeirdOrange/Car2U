import MainLoginCar2U
import MainSignupCar2U
import CustUpRenterCar2U

import CustHomeCar2U
import CustProfileCar2U
import CustBookingListCar2U
import CustAboutUsCar2U
import CustOFFICIAL_booking_detailsCar2U
import CustOFFICIAL_payment_pageCar2U
import CustOFFICIAL_review_pageCar2U
import CustChatCar2U

import AdminHomeCar2U
import AdminOfficialUploadCar2U
import AdminBookingCar2U
import AdminProfileCar2U
import AdminChatCar2U

import tkinter as tk
import sqlite3

# Define the callbacks
def open_signup():
    MainSignupCar2U.signupgui(open_login,open_home)

def open_login():
    MainLoginCar2U.logingui(open_signup,open_home,open_admin_home,returnLogin)

def returnLogin():
    MainLoginCar2U.logingui(open_signup,open_home,open_admin_home,returnLogin)

def open_upRent():
    CustUpRenterCar2U.upRenter(open_login,open_home)


# User Callbacks
def open_home():
    CustHomeCar2U.homepage(open_login,open_upRent,open_listing,open_profile,open_aboutUs,open_review,open_chat)

def open_listing():
    CustBookingListCar2U.booking(open_login,open_home,open_profile,open_aboutUs,open_bookDetails,open_review,open_chat)

def open_profile():
    CustProfileCar2U.profile(open_login,open_home,open_listing,open_aboutUs,open_review,open_chat)

def open_aboutUs():
    CustAboutUsCar2U.aboutUspage(open_login,open_upRent,open_home,open_listing,open_profile,open_review,open_chat)

def open_bookDetails():
    CustOFFICIAL_booking_detailsCar2U.bookingdetails(open_login,open_listing,open_profile,open_review,open_chat)

def open_payment():
    CustOFFICIAL_payment_pageCar2U.paymentGUI(open_login,open_home,open_listing,open_aboutUs,open_profile,open_review)

def open_review():
    CustOFFICIAL_review_pageCar2U.reviewGUI(open_login,open_home,open_listing,open_profile,open_aboutUs,open_payment,open_chat)

def open_chat():
    CustChatCar2U.custChatGUI(open_login,open_home,open_listing,open_aboutUs,open_profile,open_review,open_chat)


# Admin Callbacks
def open_admin_home():
    AdminHomeCar2U.adminHome(open_login,open_car_details,open_admin_Booking,open_admin_Profile,open_admin_Chat)

def open_car_details():
    AdminOfficialUploadCar2U.uploadGUI(open_login,open_admin_home,open_admin_Booking,open_admin_Profile,open_admin_Chat)

def open_admin_Booking():
    AdminBookingCar2U.carBooking(open_login,open_admin_home,open_car_details,open_admin_Profile,open_admin_Chat)

def open_admin_Profile():
    AdminProfileCar2U.adminProfile(open_login,open_admin_home,open_car_details,open_admin_Booking,open_admin_Chat)

def open_admin_Chat():
    AdminChatCar2U.adminChat(open_login,open_admin_home,open_car_details,open_admin_Booking,open_admin_Profile)

def Database(): #creating connection to database and creating table
    try:
        global conn, cursor
        conn = sqlite3.connect("car2u.db")
        cursor = conn.cursor()

        query = """
            CREATE TABLE IF NOT EXISTS UserDetails (
                userID INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(150) NOT NULL UNIQUE,
                password VARCHAR(100) NOT NULL,
                gender BINARY,
                dob DATE NOT NULL,
                contactNo VARCHAR(15) NOT NULL,
                nationality VARCHAR(100),
                profilePic BLOB,
                dateCreated DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS CarDetails (
                carID INTEGER PRIMARY KEY AUTOINCREMENT,
                registrationNo VARCHAR(10) UNIQUE,
                model VARCHAR(20) NOT NULL,
                colour VARCHAR(20) NOT NULL,
                fuelType VARCHAR(20) NOT NULL,
                seatingCapacity VARCHAR(20) NOT NULL,
                transmissionType VARCHAR(20) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                carImage BLOB,
                agencyID INTEGER NOT NULL,
                dateCreated DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (agencyID) REFERENCES RentalAgency(agencyID)
            );

            CREATE TABLE IF NOT EXISTS RentalAgency (
                agencyID INTEGER PRIMARY KEY AUTOINCREMENT,
                agencyName VARCHAR(30) NOT NULL,
                agencyLocation VARCHAR(100) NOT NULL,
                agencyEmail VARCHAR(150) NOT NULL UNIQUE,
                agencyPassword VARCHAR(100) NOT NULL,
                agencyContactNo VARCHAR(15) NOT NULL,
                agencyLogo BLOB,
                dateCreated DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS BookingDetails (
                bookingID INTEGER PRIMARY KEY AUTOINCREMENT,
                carID INTEGER NOT NULL,
                userID INTEGER NOT NULL,
                pickupDate DATE NOT NULL,
                pickupTime TIME NOT NULL,
                pickupLocation VARCHAR(100) NOT NULL,
                dropoffDate DATE NOT NULL,
                dropoffTime TIME NOT NULL,
                dropoffLocation VARCHAR(100) NOT NULL,
                numberOfDays INTEGER GENERATED ALWAYS AS (JULIANDAY(dropoffDate) - JULIANDAY(pickupDate)),
                totalAmount REAL,
                bookingStatus VARCHAR (30),
                bookingRemark VARCHAR (100),
                dateCreated DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (carID) REFERENCES CarDetails(carID),
                FOREIGN KEY (userID) REFERENCES UserDetails(userID)
            );

            CREATE TABLE IF NOT EXISTS Transactions (
                transactID INTEGER PRIMARY KEY AUTOINCREMENT,
                transactionMethod VARCHAR(30) NOT NULL,
                totalAmount DECIMAL(10, 2) NOT NULL,
                receipt BLOB,
                bookingID INTEGER,
                dateCreated DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (bookingID) REFERENCES BookingDetails(bookingID)
            );

            CREATE TABLE IF NOT EXISTS Reviews (
                reviewID    INTEGER PRIMARY KEY AUTOINCREMENT,
                ratings    REAL NOT NULL,
                statement    VARCHAR(200),
                bookingID    INTEGER NOT NULL,
                dateCreated    DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (bookingID) REFERENCES BookingDetails(bookingID)
            );
        """

        cursor.executescript(query)
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error has happened: ",e)

global root
root = tk.Tk()
root.withdraw() #Hides root window
UserInfo = ""

Database()

# Start with the login screen
open_home()

root.mainloop()  # Only call mainloop once
