import tkinter as tk
import customtkinter as ctk
import pywinstyles
from pathlib import Path
from PIL import Image
from tkinter import Toplevel, messagebox
from tkcalendar import DateEntry
from MainCar2U_UserInfo import get_user_info,set_user_info

# Set up the asset path
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Cust-Home")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Function to handle login button click
def open_login(current_window, login_callback):
    current_window.destroy()  # Close the signup window
    userInfo = ""
    set_user_info(userInfo)
    login_callback()

# Function to handle profile button click
def open_home():
    messagebox.showinfo("You are on the Home page")

# Function to handle selection button click
def open_listing(current_window, list_callback):
    current_window.destroy()  # Close the signup window
    list_callback()

# Function to handle profile button click
def open_profile(current_window, profile_callback):
    current_window.destroy()  # Close the signup window
    profile_callback()

def open_upRent(current_window, uprent_callback):
    current_window.destroy()  # Close the login window
    uprent_callback()

# Function to handle about us button click
def open_aboutUs(current_window, about_callback):
    current_window.destroy()  # Close the signup window
    about_callback()
    
# Function to handle profile button click
def open_review(current_window, review_callback):
    current_window.destroy()  # Close the signup window
    review_callback()
"""
def accManage(current_window, login_callback,profile_callback,review_callback):
    global pfpState, droptabFrame

    if pfpState == 1:
        droptabFrame = ctk.CTkFrame(current_window,width=190,height=240, bg_color="#E6F6FF",fg_color="#E6F6FF")
        droptabFrame.place(x=1090, y=60)

        if userInfo == "":
            droptabFrame.configure(height=57)
            logoin = ctk.CTkButton(master=droptabFrame, text="Log In", text_color="#000000", fg_color=("#E6F6FF","#D9D9D9"), 
                                    bg_color="#E6F6FF", font=("SegoeUI Bold", 20), command=lambda:open_login(current_window, login_callback))
            logoin.place(x=30,y=13)

        else:
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
"""
def create_navigation_bar():
    # Navigation Tab
    nav_img = ctk.CTkImage(Image.open(relative_to_assets("image_2.png")),size=(1280,60))
    nav_label = ctk.CTkLabel(chatFrame, image=nav_img, text="", width=1280, height=60)
    nav_label.place(x=0, y=0)

    logo_img = ctk.CTkImage(Image.open(relative_to_assets("image_3.png")),size=(75,40))
    logo_label = ctk.CTkLabel(chatFrame, image=logo_img, text="", bg_color="#F47749", width=95, height=50)
    logo_label.place(x=5, y=5)
    pywinstyles.set_opacity(logo_label,color="#F47749")
    
    pfp_img = ctk.CTkImage(Image.open(relative_to_assets("image_4.png")),size=(40,40))
    pfp_label = ctk.CTkButton(chatFrame, image=pfp_img, text="", bg_color="#F47749", fg_color="#F47749",
                              width=40, height=40, command=lambda:print("a"))
    pfp_label.place(x=1180, y=5)
    pywinstyles.set_opacity(pfp_label,color="#F47749")

    # Relocate buttons
    home_button = ctk.CTkButton(master=chatFrame, text="Home", width=120, fg_color=("#F95C41","#FA5740"), bg_color="#FA5740", 
                                text_color="#FFF6F6", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_home())
    home_button.place(x=627, y=14)
    pywinstyles.set_opacity(home_button,color="#FA5740")

    selections_button = ctk.CTkButton(master=chatFrame, text="Selections", width=120, fg_color=("#FA5740","#FB543F"), bg_color="#FB543F", 
                                      text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda:open_home())
    selections_button.place(x=763, y=14)
    pywinstyles.set_opacity(selections_button,color="#FB543F")

    contact_us_button = ctk.CTkButton(master=chatFrame, text="Contact Us", width=120, fg_color=("#FB543F","#FC503E"), bg_color="#FC503E", 
                                      text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_home())
    contact_us_button.place(x=910, y=14)
    pywinstyles.set_opacity(contact_us_button,color="#FC503E")

    about_us_button = ctk.CTkButton(master=chatFrame, text="About Us", width=120, fg_color=("#FC503E","#FC4D3D"), bg_color="#FC4D3D", 
                                    text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_home())
    about_us_button.place(x=1055, y=14)
    pywinstyles.set_opacity(about_us_button,color="#FC4D3D")


def create_left_panel():
    left_panel = ctk.CTkFrame(chatFrame, width=320, height=595, corner_radius=0, fg_color="#111333")
    left_panel.place(x=55,y=105)

    left_title = ctk.CTkLabel(left_panel, text="Rental Agencies", font=("Arial", 16, "bold"), text_color="white")
    left_title.pack(pady=10)

    # Example user buttons
    user_buttons = ["Pravin", "John", "Martha"]
    for user in user_buttons:
        user_button = ctk.CTkButton(
            left_panel, text=user, width=180, height=40, fg_color="#FFD6A6", text_color="#000000"
        )
        user_button.pack(pady=5)

def create_right_panel():
    right_panel = ctk.CTkFrame(chatFrame, fg_color="#0F0F3A", width=850, height=595)
    right_panel.place(x=370,y=105)

    right_label = ctk.CTkLabel(right_panel, text="Chat Area", font=("Arial", 14), text_color="white")
    right_label.pack(pady=10)

    chat_display = ctk.CTkTextbox(right_panel, width=600, height=400, fg_color="#111333", text_color="white")
    chat_display.pack(pady=10)

    chat_input = ctk.CTkEntry(right_panel, placeholder_text="Type your message...", width=500)
    chat_input.pack(pady=10)

    def send_message():
        message = chat_input.get()
        if message:
            chat_display.insert("end", f"You: {message}\n")
            chat_input.delete(0, "end")

    send_button = ctk.CTkButton(right_panel, text="Send", width=100, command=send_message)
    send_button.pack(pady=10)

def main():
    global chatFrame
    chatFrame = ctk.CTk()
    chatFrame.title("User Chat Interface")
    chatFrame.geometry("1280x720")
    #chatFrame.resizable(False,False)

    # Build interface
    create_navigation_bar()
    create_left_panel()
    create_right_panel()

    chatFrame.mainloop()


main()
