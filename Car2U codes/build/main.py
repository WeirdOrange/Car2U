import LoginCar2U
import SignupCar2U
import ProfileCar2U
import HomeCar2U
import BookingListCar2U
import tkinter as tk

# Define the callbacks
def open_signup():
    SignupCar2U.signupgui(open_login,open_home)

def open_login():
    LoginCar2U.logingui(open_signup,open_home)

def open_home():
    HomeCar2U.homepage(open_login,open_listing,open_profile)

def open_listing():
    BookingListCar2U.booking(open_login,open_home,open_profile)

def open_profile():
    ProfileCar2U.profile(open_login,open_home,open_listing)


global root
root = tk.Tk()
root.withdraw() #Hides root window
UserInfo = ""

# Start with the login screen
open_login()

root.mainloop()  # Only call mainloop once
