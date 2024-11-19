import MainLoginCar2U
import MainSignupCar2U
import CustUpRenterCar2U

import CustHomeCar2U
import CustProfileCar2U
import CustBookingListCar2U
import CustAboutUsCar2U
import CustOFFICIAL_booking_details
import CustOFFICIAL_payment_page
import CustOFFICIAL_review_page
import CustChatCar2U

import AdminHomeCar2U
import AdminOfficialUploadCar2U
import AdminBookingCar2U
import AdminProfileCar2U
import AdminChatCar2U

import tkinter as tk

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
    CustOFFICIAL_booking_details.bookingdetails(open_login,open_listing,open_profile,open_review,open_chat)

def open_payment():
    CustOFFICIAL_payment_page.paymentGUI(open_login,open_home,open_listing,open_aboutUs,open_profile,open_review)

def open_review():
    CustOFFICIAL_review_page.reviewGUI(open_login,open_home,open_listing,open_profile,open_aboutUs,open_payment,open_chat)

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

global root
root = tk.Tk()
root.withdraw() #Hides root window
UserInfo = ""

# Start with the login screen
open_login()

root.mainloop()  # Only call mainloop once
