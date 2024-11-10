# Import required modules
import socket
import threading
import tkinter as tk
import customtkinter as ctk
import pywinstyles
import sqlite3
from tkinter import scrolledtext, messagebox
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

# Creating a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message):
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

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

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

chatpage = ctk.CTk()
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

# Chatting Frame
chatFrame = ctk.CTkFrame(chatpage, width=700,height=665, bg_color="#2E3773", fg_color="#2E3773")
chatFrame.place(x=550,y=25)

top_frame = ctk.CTkFrame(chatFrame, width=600, height=30, bg_color="#2E3773", fg_color="#2E3773")
top_frame.place(x=0,y=0)

middle_frame = ctk.CTkFrame(chatFrame, width=610, height=480, bg_color="#0D112B", fg_color="#0D112B")
middle_frame.place(x=0,y=30)

bottom_frame = ctk.CTkFrame(chatFrame, width=610, height=70, bg_color="#2E3773", fg_color="#2E3773")
bottom_frame.place(x=0,y=630)

username_label = ctk.CTkLabel(top_frame, text="Enter username:", font=FONT, bg_color="#2E3773", fg_color="#2E3773", text_color="#FFFFFF")
username_label.pack(side="left", padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=46)
username_textbox.pack(side="left")

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
username_button.pack(side="left", padx=15)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=59)
message_textbox.pack(side="left", padx=10)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
message_button.pack(side="left", padx=10,fill="both")

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=95, height=39)
message_box.config(state=tk.DISABLED)
message_box.pack(side="top",fill="both")

def listen_for_messages_from_server(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]

            # Displaying whether it's a direct message or not
            if " (direct)" in username:
                add_message(f"[{username}] {content} (Private Message)")
            else:
                add_message(f"[{username}] {content}")
        else:
            messagebox.showerror("Error", "Message received from client is empty")

# Main function
def main():
    chatpage.mainloop()

if __name__ == '__main__':
    main()
