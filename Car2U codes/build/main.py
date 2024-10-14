import LoginCar2U
import SignupCar2U
import tkinter as tk

# Define the callbacks
def open_signup():
    SignupCar2U.signupgui(open_login)

def open_login():
    LoginCar2U.logingui(open_signup)

global root
root = tk.Tk()
root.withdraw() #Hides root window

# Start with the login screen
open_login()

root.mainloop()  # Only call mainloop once
