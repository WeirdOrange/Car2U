# Import required modules
import socket
import threading
import tkinter as tk
import customtkinter as ctk
import pywinstyles
import sqlite3
from MainCar2U_UserInfo import get_user_info,set_user_info, store_messages,fetch_messages
from tkinter import Toplevel,scrolledtext, messagebox, ttk
from pathlib import Path
from PIL import Image

HOST = '127.0.0.1'
PORT = 1234

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

# Set up the asset path
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Admin-Chat")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def Database(): #creating connection to database and creating table
    global conn, cursor
    conn = sqlite3.connect("car2u.db")
    # Enable access to columns by name
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
 
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
def open_bookings(current_window, booking_callback):
    current_window.destroy()  # Close the window
    booking_callback()

# Function to handle profile button click
def open_profile(current_window, profile_callback):
    current_window.destroy()  # Close the window
    profile_callback()

# Function to handle car details button click
def open_Cdetail(current_window, detail_callback):
    current_window.destroy()  # Close the window
    detail_callback()

# Function to handle chats button click
def open_chat():
    messagebox.showinfo("You are on the Chat page")

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

    connectServer.configure(state="disabled")
    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()
    
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
    message = message_textbox.get()
    if message != '':
        if message.startswith("@"):
            # Direct message format: @username message
            client.sendall(message.encode())
        else:
            # Broadcast message
            client.sendall(message.encode())
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

def refresh_chatlist():
    try:
        Database()
        cursor.execute("""SELECT name FROM UserDetails""")
        result = cursor.fetchall()
        conn.close()
        
        # Clear existing entries
        for widget in selectCustFrame.winfo_children():
            widget.destroy()

        all_button = ctk.CTkButton(selectCustFrame, text="All", width=270, height=45, 
                                    fg_color="#FFD6A6", text_color="#000000")
        all_button.pack(pady=5)

        # Add user-specific options
        for i, row in enumerate(result):
            cust_name = row[0]

            cust_name = str(cust_name).replace(" ","")
            user_button = ctk.CTkButton(selectCustFrame, text=cust_name, width=270, height=45,
                                        fg_color="#FFD6A6", text_color="#000000", command=lambda cust_name=cust_name: message_directed(cust_name))
            user_button.pack(pady=5)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

def message_directed(cust_id):
    if message_textbox.get() != "":
        message_textbox.delete(0, tk.END)
    message_textbox.insert(0, f"@{cust_id} ")
def fetchName():
    global agencyName, userinfo
    userinfo = get_user_info()
    print(f"Home: {userinfo}")
    Database()
    cursor.execute("""SELECT agencyName FROM RentalAgency WHERE agencyID = ?""",(userinfo,))
    agencyName = cursor.fetchone()[0]
    conn.close()
    print(agencyName)
    return agencyName

def adminChat(login_callback,home_callback,detail_callback,booking_callback,profile_callback):
    # Creating a socket object
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    agencyName = fetchName()

    chatpage = Toplevel()
    chatpage.geometry("1280x720")
    chatpage.title("Messenger Client")
    chatpage.resizable(False, False)

    bg_img = ctk.CTkImage(Image.open(relative_to_assets("admin_bg.png")),size=(1280,720))
    bg_label = ctk.CTkLabel(chatpage, image=bg_img,text="")
    bg_label.place(x=0, y=0)

    # Navigation Tab
    nav_img = ctk.CTkImage(Image.open(relative_to_assets("nav.png")),size=(200,720))
    nav_label = ctk.CTkLabel(chatpage, image=nav_img, text="")
    nav_label.place(x=0, y=0)

    logo_img = ctk.CTkImage(Image.open(relative_to_assets("Logo.png")),size=(150,60))
    logo_label = ctk.CTkLabel(chatpage, image=logo_img, text="", bg_color="#F47749", width=95, height=50)
    logo_label.place(x=22, y=10)
    pywinstyles.set_opacity(logo_label,color="#F47749")

    global pfpState
    pfpState = 1
    pfp_img = ctk.CTkImage(Image.open(relative_to_assets("image_4.png")),size=(100,100))
    pfp_label = ctk.CTkButton(chatpage, image=pfp_img, text="", bg_color="#FE453B", fg_color="#FE453B",
                                width=40, height=40, command=lambda: accManage(chatpage, login_callback,profile_callback))
    pfp_label.place(x=41, y=590)
    pywinstyles.set_opacity(pfp_label,color="#FE453B")

    # Relocate buttons
    home_button = ctk.CTkButton(master=chatpage, text="Home", width=120, fg_color=("#F95C41","#FA5740"), bg_color="#FA5740", 
                                text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_home(chatpage, home_callback))
    home_button.place(x=22, y=100)
    pywinstyles.set_opacity(home_button,color="#FA5740")

    booking_button = ctk.CTkButton(master=chatpage, text="Bookings", width=120, fg_color=("#FA5740","#FB543F"), bg_color="#FB543F", 
                                        text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_bookings(chatpage, booking_callback))
    booking_button.place(x=22, y=165)
    pywinstyles.set_opacity(booking_button,color="#FB543F")

    inventory_button = ctk.CTkButton(master=chatpage, text="Inventory", width=120, fg_color=("#FB543F","#FC503E"), bg_color="#FC503E", 
                                        text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), 
                                        command=lambda: open_Cdetail(chatpage, detail_callback))
    inventory_button.place(x=22, y=230)
    pywinstyles.set_opacity(inventory_button,color="#FC503E")

    chat_button = ctk.CTkButton(master=chatpage, text="Chat", width=120, fg_color=("#FC503E","#FC4D3D"), bg_color="#FC4D3D", 
                                    text_color="#FFF6F6", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_chat())
    chat_button.place(x=22, y=295)
    pywinstyles.set_opacity(chat_button,color="#FC4D3D")

    # Choose who to msg frame
    selectFrame = ctk.CTkFrame(chatpage, width=320,height=665, bg_color="#0D112B", fg_color="#0D112B")
    selectFrame.place(x=230,y=25)

    customerTitle = ctk.CTkLabel(selectFrame, text="Customer", width=320, height=35, anchor="center", font=("Tw Cen MT Condensed Extra Bold", 32), text_color="#FFFFFF")
    customerTitle.place(x=0,y=0)

    connectFrame = ctk.CTkFrame(selectFrame, width=310, height=40, bg_color="#067BC1", fg_color="#067BC1")
    connectFrame.place(x=5,y=60)
    global connectServer
    connectServer = ctk.CTkButton(connectFrame, text="Connect to Server", width=300, height=30, bg_color="#067BC1", fg_color="#067BC1", text_color="white",
                                font=("Tw Cen MT", 24), command=connect)
    connectServer.place(x=5,y=0)

    global selectCustFrame
    selectCustFrame = ctk.CTkScrollableFrame(selectFrame, width=290,height=545, bg_color="#191F48", fg_color="#191F48")
    selectCustFrame.place(x=5,y=110)

    # Chatting Frame
    chatFrame = ctk.CTkFrame(chatpage, width=700,height=665, bg_color="#2E3773", fg_color="#2E3773")
    chatFrame.place(x=550,y=25)

    top_frame = ctk.CTkFrame(chatFrame, width=600, height=50, bg_color="#2E3773", fg_color="#2E3773")
    top_frame.place(x=0,y=0)

    middle_frame = ctk.CTkFrame(chatFrame, width=610, height=460, bg_color="#0D112B", fg_color="#0D112B")
    middle_frame.place(x=0,y=50)

    bottom_frame = ctk.CTkFrame(chatFrame, width=620, height=60, bg_color="#2E3773", fg_color="#2E3773")
    bottom_frame.place(x=0,y=620)

    username_label = ctk.CTkLabel(top_frame, text=f"Your Name : {agencyName}", font=("Tw Cen MT",20), bg_color="#2E3773", fg_color="#2E3773", text_color="#FFFFFF",
                                    width=550, height=40, anchor="center")
    username_label.place(x=30,y=5)

    global message_textbox
    message_textbox = ctk.CTkEntry(bottom_frame, placeholder_text="Type your message...", fg_color="#000000", text_color="white", width=583, height=40)
    message_textbox.pack(side="left", padx=10)

    message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
    message_button.bind('<Return>',send_message)
    message_button.pack(side="right", padx=10,fill="both")

    global message_box
    message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=100, height=39)
    message_box.config(state=tk.DISABLED)
    message_box.pack(side="top",fill="both")
    refresh_chatlist()

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
