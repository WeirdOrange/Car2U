import socket
import threading
import tkinter as tk
import customtkinter as ctk
import pywinstyles
import sqlite3
from pathlib import Path
from PIL import Image
from tkinter import Toplevel, scrolledtext, messagebox, ttk
from tkcalendar import DateEntry
from MainCar2U_UserInfo import get_user_info,set_user_info,store_messages,fetch_messages,getRenter, fetch_file_path

file_path = fetch_file_path()
assetPath = f"{file_path}\\Cust-Chat"

# Set up the asset path
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(assetPath)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

HOST = '127.0.0.1'
PORT = 1234

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

def Database(): #creating connection to database and creating table
    global conn, cursor
    conn = sqlite3.connect("car2u.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

# Function to handle login button click
def open_login(current_window, login_callback):
    current_window.destroy()  # Close the window
    userInfo = ""
    set_user_info(userInfo)
    login_callback()

# Function to handle profile button click
def open_home(current_window, home_callback):
    current_window.destroy()  # Close the window
    home_callback()

# Function to handle selection button click
def open_listing(current_window, list_callback):
    current_window.destroy()  # Close the window
    list_callback()

# Function to handle profile button click
def open_profile(current_window, profile_callback):
    current_window.destroy()  # Close the window
    profile_callback()

# Function to handle about us button click
def open_aboutUs(current_window, about_callback):
    current_window.destroy()  # Close the window
    about_callback()
    
# Function to handle chats button click
def open_chat():
    messagebox.showinfo("Chat Page Clicked","You are on the on the Chatting Page")

# Function to handle profile button click
def open_review(current_window, review_callback):
    current_window.destroy()  # Close the window
    review_callback()

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
 
def add_message(message):
    message_box.config(state=tk.NORMAL)
    store_messages(message)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():
    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

    global username
    username = fetchName() # Enter username to server
    uesrname = str(username).replace(" ","")
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()
    connectServer.configure(state="disabled")
    previous_messages = fetch_messages()
    if previous_messages:
        for message in previous_messages:
            if message == "[SERVER] Successfully connected to the server":
                continue
            else:
                message_box.config(state=tk.NORMAL)
                message_box.insert(tk.END, message + '\n')
                message_box.config(state=tk.DISABLED)

def send_message():
    message = chat_input.get()
    if message != '':
        if message.startswith("@"):
            # Direct message format: @username message
            client.sendall(message.encode())
        else:
            # Broadcast message
            client.sendall(message.encode())
        chat_input.delete(0, len(message))
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

def refresh_chatlist():
    try:
        Database()
        cursor.execute("""SELECT agencyName FROM RentalAgency""")
        result = cursor.fetchall()
        conn.close()
        # Clear existing entries
        for widget in selectCustFrame.winfo_children():
            widget.destroy()

        all_button = ctk.CTkButton(selectCustFrame, text="All", width=185, height=45, font= ("Tw Cen MT",16),
                                    fg_color="#FFD6A6", text_color="#000000")
        all_button.pack(pady=5)

        # Add user-specific options
        for i, row in enumerate(result):
            cust_name = row[0]
            print(cust_name)

            cust_name = str(cust_name).replace(" ","")
            user_button = ctk.CTkButton(selectCustFrame, text=cust_name, width=185, height=45, font= ("Tw Cen MT",16),
                                        fg_color="#FFD6A6", text_color="#000000", command=lambda cust_name=cust_name: message_directed(cust_name))
            user_button.pack(pady=5)
        
        renter = getRenter()
        if renter:
            chat_input.insert(0, f"@{renter} ")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

def message_directed(cust_id):
    if chat_input.get() != "":
        chat_input.delete(0, tk.END)
    chat_input.insert(0, f"@{cust_id} ")

def fetchName():
    try:
        global agencyName, userInfo
        userInfo = get_user_info()
        print(f"Home: {userInfo}")
        Database()
        cursor.execute("""SELECT name FROM UserDetails WHERE userID = ?""",(userInfo,))
        agencyName = cursor.fetchone()[0]
        conn.close()
        print(agencyName)
    except Exception:
        messagebox.showerror("User Not Found","Please log in as user in order to use the Chatting System. Thanks.")
    return agencyName


def create_left_panel():
    left_panel = ctk.CTkFrame(chatFrame, width=225, height=595, corner_radius=0, fg_color="#111333")
    left_panel.place(x=55,y=105)

    left_title = ctk.CTkLabel(left_panel, text="Rental Agency", font=("Arial", 16, "bold"), text_color="white", width=220, anchor="center")
    left_title.place(x=0,y=10)
    
    global connectServer
    connectServer = ctk.CTkButton(left_panel, text="Connect to Server", width=200, height=30, bg_color="#067BC1", fg_color="#067BC1", text_color="white",
                                font=("Tw Cen MT", 24), corner_radius=10, command=connect)
    connectServer.place(x=10,y=60)
    
    global selectCustFrame
    selectCustFrame = ctk.CTkScrollableFrame(left_panel, width=215,height=545, bg_color="#191F48", fg_color="#191F48")
    selectCustFrame.place(x=0,y=110)
    refresh_chatlist()

def create_right_panel():
    name = fetchName()
    right_panel = ctk.CTkFrame(chatFrame, fg_color="#2E3773", width=950, height=595)
    right_panel.place(x=275,y=105)

    right_label = ctk.CTkLabel(right_panel, text=f"Your Name : {name}", font=("Tw Cen MT",20), text_color="white", bg_color="#2E3773", width=950, height=50, anchor="center")
    right_label.place(x=0,y=0)

    middle_frame = ctk.CTkFrame(right_panel, width=950, height=475, bg_color="#0D112B", fg_color="#0D112B")
    middle_frame.place(x=0,y=50)

    global message_box
    message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=110, height=25)
    message_box.config(state=tk.DISABLED)
    message_box.pack(side="top",fill="both")

    global chat_input
    chat_input = ctk.CTkEntry(right_panel, placeholder_text="Type your message...", fg_color="#000000", text_color="white", width=765, height=40)
    chat_input.place(x=30,y=545)

    send_button = ctk.CTkButton(right_panel, text="Send", width=80, height=30, command=send_message)
    send_button.bind('<Return>',send_message)
    send_button.place(x=827,y=550)

def custChatGUI(login_callback,home_callback,listing_callback,aboutUs_callback,profile_callback,review_callback,chat_callback):
    # Creating a socket object
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    global chatFrame
    chatFrame = Toplevel()
    chatFrame.title("Messenge Client")
    chatFrame.geometry("1280x720")
    chatFrame.resizable(False,False)

    global pfpState
    pfpState = 1

    # Navigation Tab
    nav_img = ctk.CTkImage(Image.open(relative_to_assets("nav.png")),size=(1280,60))
    nav_label = ctk.CTkLabel(chatFrame, image=nav_img, text="", width=1280, height=60)
    nav_label.place(x=0, y=0)

    logo_img = ctk.CTkImage(Image.open(relative_to_assets("logo.png")),size=(75,40))
    logo_label = ctk.CTkLabel(chatFrame, image=logo_img, text="", bg_color="#F47749", width=95, height=50)
    logo_label.place(x=5, y=5)
    pywinstyles.set_opacity(logo_label,color="#F47749")
    
    pfp_img = ctk.CTkImage(Image.open(relative_to_assets("image_1.png")),size=(40,40))
    pfp_label = ctk.CTkButton(chatFrame, image=pfp_img, text="", bg_color="#F47749", fg_color="#F47749",
                              width=40, height=40, command=lambda:accManage(chatFrame,login_callback,profile_callback,review_callback))
    pfp_label.place(x=1203, y=5)
    pywinstyles.set_opacity(pfp_label,color="#F47749")

    # Relocate buttons
    home_button = ctk.CTkButton(master=chatFrame, text="Home", width=120, fg_color=("#F95C41","#FA5740"), bg_color="#FA5740", 
                                text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_home(chatFrame,home_callback))
    home_button.place(x=667, y=14)
    pywinstyles.set_opacity(home_button,color="#FA5740")

    selections_button = ctk.CTkButton(master=chatFrame, text="Selections", width=120, fg_color=("#FA5740","#FB543F"), bg_color="#FB543F", 
                                      text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda:open_listing(chatFrame,listing_callback))
    selections_button.place(x=783, y=14)
    pywinstyles.set_opacity(selections_button,color="#FB543F")

    contact_us_button = ctk.CTkButton(master=chatFrame, text="Contact Us", width=120, fg_color=("#FB543F","#FC503E"), bg_color="#FC503E", 
                                      text_color="#FFF6F6", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_chat())
    contact_us_button.place(x=930, y=14)
    pywinstyles.set_opacity(contact_us_button,color="#FC503E")

    about_us_button = ctk.CTkButton(master=chatFrame, text="About Us", width=120, fg_color=("#FC503E","#FC4D3D"), bg_color="#FC4D3D", 
                                    text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_aboutUs(chatFrame,aboutUs_callback))
    about_us_button.place(x=1075, y=14)
    pywinstyles.set_opacity(about_us_button,color="#FC4D3D")
    
    # Build interface
    create_left_panel()
    create_right_panel()


def listen_for_messages_from_server(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            global username
            username = message.split("~")[0]
            content = message.split('~')[1]

            # Displaying whether it's a direct message or not
            if " (direct)" in username:
                add_message(f"[{username}] {content} (Private Message)")
            else:
                add_message(f"[{username}] {content}")
        else:
            messagebox.showerror("Error", "Message received from client is empty")
