# Import required modules
import socket
import threading
import tkinter as tk
import customtkinter as ctk
import pywinstyles
import sqlite3
from tkinter import scrolledtext, messagebox, ttk
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
    
def add_message(message, user="All"):
    chat_logs.setdefault(user, []).append(message)
    if current_chat_user == user:
        message_box.config(state=tk.NORMAL)
        message_box.insert(tk.END, message + '\n')
        message_box.config(state=tk.DISABLED)

def connect():
    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

    #global userinfo
    #userinfo = get_user_info()
    #print(f"Home: {userinfo}")
    Database()
    #cursor.execute("""SELECT agencyName FROM RentalAgency WHERE agencyID = ?""",(userinfo,))
    cursor.execute("""SELECT agencyName FROM RentalAgency WHERE agencyID = 1""")
    agencyName = cursor.fetchone()[0]
    conn.close()
    print(agencyName)

    username = agencyName # Enter username to server
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():
    message = message_textbox.get()
    if message:
        if current_chat_user == "All":
            # Broadcast message
            save_message_to_db("Admin", "All", message, is_direct=False)
            client.sendall(message.encode())
        else:
            # Direct message
            save_message_to_db("Admin", current_chat_user, message, is_direct=True)
            client.sendall(f"@{current_chat_user} {message}".encode())

        add_message(f"You: {message}", user=current_chat_user)
        message_textbox.delete(0, tk.END)
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

def save_message_to_db(sender, receiver, message, is_direct):
    Database()
    try:
        cursor.execute("""
            INSERT INTO Messages (sender, receiver, message, is_direct, timestamp) 
            VALUES (?, ?, ?, ?, datetime('now'))
        """, (sender, receiver, message, is_direct))
        conn.commit()
    except Exception as e:
        print(f"Error saving message to database: {e}")
    finally:
        conn.close()

def load_messages_from_db(user_id):
    global current_chat_user
    current_chat_user = user_id
    chat_logs[user_id] = []  # Reset chat log for this user

    Database()
    try:
        if user_id == "All":
            # Load broadcast messages
            cursor.execute("""
                SELECT sender, message, is_direct FROM Messages 
                WHERE receiver = 'All' OR receiver IS NULL
                ORDER BY timestamp ASC
            """)
        else:
            # Load direct messages between admin and the user
            cursor.execute("""
                SELECT sender, message, is_direct FROM Messages 
                WHERE (sender = ? AND receiver = ?) OR (sender = ? AND receiver = ?)
                ORDER BY timestamp ASC
            """, (user_id, "Admin", "Admin", user_id))
        
        messages = cursor.fetchall()
        for row in messages:
            sender = row[0]
            message = row[1]
            is_direct = row[2]
            formatted_message = f"[{sender}] {message}"
            if is_direct:
                formatted_message += " (Private Message)"
            chat_logs[user_id].append(formatted_message)
    except Exception as e:
        print(f"Error loading messages from database: {e}")
    finally:
        conn.close()

    update_chat_display()


def refresh_chatlist():
    Database()
    cursor.execute("""SELECT C.userID, U.name FROM ChatConnect C INNER JOIN UserDetails U ON U.userID = C.userID WHERE C.agencyID = 1""")
    result = cursor.fetchall()
    conn.close()

    # Clear existing entries
    for widget in selectCustFrame.winfo_children():
        widget.destroy()

    # Add "All" option
    def switch_to_all():
        switch_chat("All")
    all_button = ctk.CTkButton(selectCustFrame, text="All", width=270, height=45, 
                                fg_color="#FFD6A6", text_color="#000000", command=switch_to_all)
    all_button.pack(pady=5)

    # Add user-specific options
    for i, row in enumerate(result):
        cust_id = row[0]
        cust_name = row[1]

        def switch_to_user(user_id=cust_id):
            switch_chat(user_id)

        user_button = ctk.CTkButton(selectCustFrame, text=cust_name, width=270, height=45,
                                     fg_color="#FFD6A6", text_color="#000000", command=switch_to_user)
        user_button.pack(pady=5)

def switch_chat(user_id):
    global current_chat_user
    current_chat_user = user_id
    update_chat_display()

def update_chat_display():
    message_box.config(state=tk.NORMAL)
    message_box.delete(1.0, tk.END)
    for message in chat_logs.get(current_chat_user, []):
        message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def adminChatGUI():
    # Creating a socket object
    global client, chatpage
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    chatpage = ctk.CTk()
    chatpage.geometry("1280x720")
    chatpage.title("Messenger Client")
    chatpage.resizable(False, False)

    global current_chat_user, chat_logs
    current_chat_user = "All"  # Default to broadcast channel
    chat_logs = {"All": []}  # Store chat messages by user/channel

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
                                width=40, height=40, command=lambda:print("a"))
    pfp_label.place(x=41, y=590)
    pywinstyles.set_opacity(pfp_label,color="#FE453B")

    # Relocate buttons
    home_button = ctk.CTkButton(master=chatpage, text="Home", width=120, fg_color=("#F95C41","#FA5740"), bg_color="#FA5740", 
                                text_color="#FFF6F6", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: print("a"))
    home_button.place(x=22, y=100)
    pywinstyles.set_opacity(home_button,color="#FA5740")

    booking_button = ctk.CTkButton(master=chatpage, text="Bookings", width=120, fg_color=("#FA5740","#FB543F"), bg_color="#FB543F", 
                                        text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda:print("a"))
    booking_button.place(x=22, y=165)
    pywinstyles.set_opacity(booking_button,color="#FB543F")

    inventory_button = ctk.CTkButton(master=chatpage, text="Inventory", width=120, fg_color=("#FB543F","#FC503E"), bg_color="#FC503E", 
                                        text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), 
                                        command=lambda: print("a"))
    inventory_button.place(x=22, y=230)
    pywinstyles.set_opacity(inventory_button,color="#FC503E")

    chat_button = ctk.CTkButton(master=chatpage, text="Chat", width=120, fg_color=("#FC503E","#FC4D3D"), bg_color="#FC4D3D", 
                                    text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: print("About Us clicked"))
    chat_button.place(x=22, y=295)
    pywinstyles.set_opacity(chat_button,color="#FC4D3D")

    # Choose who to msg frame
    selectFrame = ctk.CTkFrame(chatpage, width=320,height=665, bg_color="#0D112B", fg_color="#0D112B")
    selectFrame.place(x=230,y=25)

    customerTitle = ctk.CTkLabel(selectFrame, text="Customer", width=320, height=35, anchor="center", font=("Tw Cen MT Condensed Extra Bold", 32), text_color="#FFFFFF")
    customerTitle.place(x=0,y=0)

    searchFrame = ctk.CTkFrame(selectFrame, width=310, height=40, bg_color="#4E6573", fg_color="#4E6573")
    searchFrame.place(x=5,y=60)

    global selectCustFrame
    selectCustFrame = ctk.CTkScrollableFrame(selectFrame, width=290,height=545, bg_color="#191F48", fg_color="#191F48")
    selectCustFrame.place(x=10,y=110)

    # Chatting Frame
    chatFrame = ctk.CTkFrame(chatpage, width=700,height=665, bg_color="#2E3773", fg_color="#2E3773")
    chatFrame.place(x=550,y=25)

    top_frame = ctk.CTkFrame(chatFrame, width=600, height=50, bg_color="#2E3773", fg_color="#2E3773")
    top_frame.place(x=0,y=0)

    middle_frame = ctk.CTkFrame(chatFrame, width=610, height=460, bg_color="#0D112B", fg_color="#0D112B")
    middle_frame.place(x=0,y=50)

    bottom_frame = ctk.CTkFrame(chatFrame, width=620, height=60, bg_color="#2E3773", fg_color="#2E3773")
    bottom_frame.place(x=0,y=620)

    username_label = ctk.CTkLabel(top_frame, text=f"Name:", font=FONT, bg_color="#2E3773", fg_color="#2E3773", text_color="#FFFFFF")
    username_label.pack(side="left", padx=10)

    global username_textbox
    username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=46)
    username_textbox.pack(side="left")

    global username_button
    username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
    username_button.pack(side="left", padx=15)

    global message_textbox
    message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=59)
    message_textbox.pack(side="left", padx=10)

    message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
    message_button.bind('<Return>',send_message)
    message_button.pack(side="left", padx=10,fill="both")

    global message_box
    message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=100, height=39)
    message_box.config(state=tk.DISABLED)
    message_box.pack(side="top",fill="both")
    refresh_chatlist()

    chatpage.mainloop()

def listen_for_messages_from_server(client):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                sender, content = message.split('~', 1)
                is_direct = " (direct)" in sender
                chat_user = sender.split(" ")[0] if is_direct else "All"

                # Save the message to the database
                save_message_to_db(sender, chat_user, content, is_direct=is_direct)

                # Add the message to the chat log
                add_message(f"[{sender}] {content}", user=chat_user)
            else:
                raise ValueError("Received an empty message from the server.")
        except Exception as e:
            messagebox.showerror("Error", f"Error receiving message: {e}")



adminChatGUI()
