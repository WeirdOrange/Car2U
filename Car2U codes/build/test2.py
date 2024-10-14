import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from customtkinter import CTkImage
from PIL import Image
from pathlib import Path

# Set up paths to your assets
ASSETS_PATH = Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\Testing\build\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Bind Canvas to Mousewheel Events
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

root = tk.Tk()
root.geometry("1280x720")
root.resizable(False, False)

# Scrolling menu
frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

# Creating Canvas and Scrollbar
canvas = tk.Canvas(frame, bg="#FFFFFF", height=720, width=1280)
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

# Frame for Scrollable Content
content_frame = tk.Frame(canvas)
content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.bind_all("<MouseWheel>", _on_mousewheel)

# Add widgets to the content_frame inside the canvas
canvas.create_window((0, 0), window=content_frame, anchor="nw", width=1280)

# Properly configure canvas and scrollbar placement
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# 1. Navigation Bar with gradient background
navbg_img = CTkImage(Image.open(relative_to_assets("image_1.png")), size=(1280, 150))
navbar = ctk.CTkLabel(content_frame, image=navbg_img)
navbar.place(x=0,y=0)

# Navigation Buttons
nav_frame = tk.Frame(content_frame)
nav_frame.pack(pady=10)

homeTab = ctk.CTkButton(nav_frame, text="Home", fg_color="#FFA843", font=("SegoeUIBlack", 24))
homeTab.place(x=667, y=14)

carSelectTab = ctk.CTkButton(nav_frame, text="Selections", fg_color="#FFA843", font=("SegoeUIBold", 24))
carSelectTab.place(x=783, y=14)

contactUsTab = ctk.CTkButton(nav_frame, text="Contact Us", fg_color="#FFA843", font=("SegoeUIBold", 24))
contactUsTab.place(x=930, y=14)

aboutUsTab = ctk.CTkButton(nav_frame, text="About Us", fg_color="#FFA843", font=("SegoeUIBold", 24))
aboutUsTab.place(x=1075, y=14)

# 2. Search Area with background
search_bgimg = CTkImage(Image.open(relative_to_assets("image_2.png")), size=(1280, 100))
search_label = ctk.CTkLabel(content_frame, image=search_bgimg)
search_label.place(x=0, y=150)

search_frame = tk.Frame(content_frame)
search_frame.pack(pady=10)

entry_1 = ctk.CTkEntry(search_frame, fg_color="#D9D9D9", text_color="#000716", border_width=0, width=300, height=40)
entry_1.place(x=200, y=180)

entry_2 = ctk.CTkEntry(search_frame, fg_color="#D9D9D9", text_color="#000716", border_width=0, width=300, height=40)
entry_2.place(x=550, y=180)

button_1 = ctk.CTkButton(search_frame, text="Find", fg_color="blue", width=85, height=40, command=lambda: print("button_1 clicked"))
button_1.place(x=900, y=180)

# 3. Promotions Section
promotions_label = ctk.CTkLabel(content_frame, text="Promotions", font=("SegoeUIBold", 24))
promotions_label.place(x=20, y=250)

promotions_frame = tk.Frame(content_frame)
promotions_frame.pack(pady=10)

# Promotion Images (Use your image paths)
promo1_img = CTkImage(Image.open(relative_to_assets("image_5.png")), size=(300, 200))
promo1 = ctk.CTkLabel(promotions_frame, image=promo1_img)
promo1.place(x=20, y=300)

promo2_img = CTkImage(Image.open(relative_to_assets("image_6.png")), size=(300, 200))
promo2 = ctk.CTkLabel(promotions_frame, image=promo2_img)
promo2.place(x=340, y=300)

promo3_img = CTkImage(Image.open(relative_to_assets("image_7.png")), size=(300, 200))
promo3 = ctk.CTkLabel(promotions_frame, image=promo3_img)
promo3.place(x=660, y=300)

promo4_img = CTkImage(Image.open(relative_to_assets("image_8.png")), size=(300, 200))
promo4 = ctk.CTkLabel(promotions_frame, image=promo4_img)
promo4.place(x=980, y=300)

# 4. Booking Steps Section
booking_label = ctk.CTkLabel(content_frame, text="How to book a car?", font=("SegoeUIBold", 24))
booking_label.place(x=20, y=520)

steps_frame = tk.Frame(content_frame)
steps_frame.pack(pady=10)

for i in range(5):
    step_label = ctk.CTkLabel(steps_frame, text=f"Step {i+1}: ", font=("SegoeUI", 16))
    step_label.place(x=40, y=560 + i*30)

# 5. Terms & Conditions Section
terms_label = ctk.CTkLabel(content_frame, text="Terms & Conditions", font=("SegoeUIBold", 24))
terms_label.place(x=20, y=720)

terms_frame = tk.Frame(content_frame)
terms_frame.pack(pady=10)

for i in range(5):
    term_label = ctk.CTkLabel(terms_frame, text=f"Step {i+1}: ", font=("SegoeUI", 16))
    term_label.place(x=20, y=720)

# 6. Footer (Accepted Payment Methods)
footer_label = ctk.CTkLabel(content_frame, text="Accepted Payment Methods", font=("SegoeUIBold", 18))
footer_label.place(x=20, y=1000)

# Payment method images
payment_img = CTkImage(Image.open(relative_to_assets("image_9.png")), size=(1000, 50))
payment_methods = ctk.CTkLabel(content_frame, image=payment_img)
payment_methods.place(x=140, y=1040)

# Footer links (About Us, Account, etc.)
footer_sections = [
    ("About Us", ["Home", "Promotions", "Collaborations", "Know More Of Us"]),
    ("Account", ["My Profile", "Sign Up", "Log Out", "Upgrade to Member"]),
    ("Support", ["Car2U Guide", "Upgrade to Member"]),
    ("Find Us", ["Facebook", "Instagram", "Twitter", "TikTok", "YouTube"])
]

# Place footer sections
footer_frame = tk.Frame(content_frame)
footer_frame.pack(pady=10)

for idx, (section_title, links) in enumerate(footer_sections):
    section_label = ctk.CTkLabel(footer_frame, text=section_title, font=("SegoeUIBold", 18))
    section_label.place(x=20 + idx*320, y=1100)

    for j, link in enumerate(links):
        link_label = ctk.CTkLabel(footer_frame, text=link, font=("SegoeUI", 14))
        link_label.place(x=20 + idx*320, y=1130 + j*30)

content_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

root.mainloop()
