import LoginCar2U
import SignupCar2U
import UpRenterCar2U

import HomeCar2U
import ProfileCar2U
import BookingListCar2U
import AboutUsCar2U

import AdminHomeCar2U
#import OFFICIAL_car_details
import AdminBookingCar2U
import AdminProfileCar2U

import tkinter as tk

# Define the callbacks
def open_signup():
    SignupCar2U.signupgui(open_login,open_home)

def open_login():
    LoginCar2U.logingui(open_signup,open_home,open_admin_home)

def open_upRent():
    UpRenterCar2U.upRenter(open_login,open_home)

# User Callbacks
def open_home():
    HomeCar2U.homepage(open_login,open_upRent,open_listing,open_profile,open_aboutUs)

def open_listing():
    BookingListCar2U.booking(open_login,open_home,open_profile,open_aboutUs)

def open_profile():
    ProfileCar2U.profile(open_login,open_home,open_listing,open_aboutUs)

def open_aboutUs():
    AboutUsCar2U.aboutUspage(open_login,open_upRent,open_home,open_listing,open_profile)


# Admin Callbacks
def open_admin_home():
    AdminHomeCar2U.adminHome(open_login,open_car_details,open_admin_Booking,open_admin_Profile)

def open_car_details():
    print("awaits")
 #   OFFICIAL_car_details.carDetails(open_login,open_admin_home,open_admin_Booking,open_admin_Profile)

def open_admin_Booking():
    AdminBookingCar2U.carBooking(open_login,open_admin_home,open_car_details,open_admin_Profile)

def open_admin_Profile():
    AdminProfileCar2U.adminProfile(open_login,open_admin_home,open_car_details,open_admin_Booking)

global root
root = tk.Tk()
root.withdraw() #Hides root window
UserInfo = ""

# Start with the login screen
open_login()

root.mainloop()  # Only call mainloop once
