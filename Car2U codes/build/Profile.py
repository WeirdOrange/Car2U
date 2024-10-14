import customtkinter as ctk
import pywinstyles
from pathlib import Path
from PIL import Image

# Set appearance mode and theme for customtkinter
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Profile")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Main window setup
root = ctk.CTk()
root.geometry("1280x720")
root.title("Profile Page")
root.configure(fg_color="#FFFFFF")

# Background
bg_img = ctk.CTkImage(Image.open(relative_to_assets("image_1.png")),size=(1280,720))
bg_label = ctk.CTkLabel(root, image=bg_img, text="", width=1280, height=60)
bg_label.place(x=0, y=0)

# Navigation Bar
header = ctk.CTkFrame(root, width=1280, height=60, fg_color="#FFFFFF")
header.place(x=0, y=0)

navbg_img = ctk.CTkImage(Image.open(relative_to_assets("nav.png")),size=(1280,60))
navbg_label = ctk.CTkLabel(header, image=navbg_img, text="", width=1280, height=60)
navbg_label.place(x=0, y=0)

# Relocating buttons
home_button = ctk.CTkButton(master=root, text="Home", width=120, fg_color=("#F95C41","#FA5740"), bg_color="#FA5740", text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: print("Home clicked"))
home_button.place(x=647, y=14)
pywinstyles.set_opacity(home_button,color="#FA5740")

selections_button = ctk.CTkButton(master=root, text="Selections", width=120, fg_color=("#FA5740","#FB543F"), bg_color="#FB543F", text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: print("Selections clicked"))
selections_button.place(x=783, y=14)
pywinstyles.set_opacity(selections_button,color="#FB543F")

contact_us_button = ctk.CTkButton(master=root, text="Contact Us", width=120, fg_color=("#FB543F","#FC503E"), bg_color="#FC503E", text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: print("Contact Us clicked"))
contact_us_button.place(x=930, y=14)
pywinstyles.set_opacity(contact_us_button,color="#FC503E")

about_us_button = ctk.CTkButton(master=root, text="About Us", width=120, fg_color=("#FC503E","#FC4D3D"), bg_color="#FC4D3D", text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: print("About Us clicked"))
about_us_button.place(x=1075, y=14)
pywinstyles.set_opacity(about_us_button,color="#FC4D3D")

# User Info section
user_name_label = ctk.CTkLabel(root, text="A Random Name", font=("Skranji", 48), text_color="#000000")
user_name_label.place(x=346, y=100)

# Placeholder for user image
user_image = ctk.CTkLabel(root, text="Image Placeholder", width=270, height=230, fg_color="#D9D9D9")
user_image.place(x=40, y=153)

# Personal information section
info_frame = ctk.CTkFrame(root, width=757, height=260, fg_color="#FFFFFF", border_width=2, border_color="grey")
info_frame.place(x=346, y=152)

info_labels = [("Email:", 166), ("Age:", 206), ("Phone No.:", 246), ("Nationality:", 286), ("Country:", 326)]
for text, y_pos in info_labels:
    label = ctk.CTkLabel(root, text=text, font=("Skranji", 20), text_color="#000000")
    label.place(x=362, y=y_pos)

# Entries (you can bind these to data later)
entry_1 = ctk.CTkEntry(root, width=438, height=28)
entry_1.place(x=490, y=165)

entry_2 = ctk.CTkEntry(root, width=438, height=28)
entry_2.place(x=490, y=205)

entry_3 = ctk.CTkEntry(root, width=438, height=28)
entry_3.place(x=490, y=245)

entry_4 = ctk.CTkEntry(root, width=438, height=28)
entry_4.place(x=490, y=285)

entry_5 = ctk.CTkEntry(root, width=438, height=28)
entry_5.place(x=490, y=325)

edit_info = ctk.CTkButton(root, text="Edit", width=80, corner_radius=50, font=("Tw Cen MT Condensed Extra Bold", 16), command=lambda: print("Edit Personal Info clicked"))
edit_info.place(x=970, y=370)

# "Top Places to Visit" Section
places_label = ctk.CTkLabel(root, text="Top Places to Visit", font=("Skranji", 36), text_color="#000000")
places_label.place(x=70, y=427)
pywinstyles.set_opacity(places_label,color="#FFFFFF")

# Top places background
place_bg = ctk.CTkFrame(root, width=1170, height=210, border_width=2,fg_color="white")
place_bg.place(x=55,y=470)

# Placeholders for destination images
place_1_img = ctk.CTkImage(Image.open(relative_to_assets("image_2.png")),size=(260,190))
place_1_photo = ctk.CTkLabel(root,image=place_1_img,text="")
place_1_photo.place(x=65, y=480)
place_1 = ctk.CTkLabel(root, text="Penang", fg_color="#FFFFFF")
place_1.place(x=355, y=510)

place_2_img = ctk.CTkImage(Image.open(relative_to_assets("image_4.png")),size=(260,190))
place_2_photo = ctk.CTkLabel(root,image=place_2_img,text="")
place_2_photo.place(x=530, y=480)
place_2 = ctk.CTkLabel(root, text="Kuala\n\tLumpur", fg_color="#FFFFFF")
place_2.place(x=810, y=520)

place_3_img = ctk.CTkImage(Image.open(relative_to_assets("image_5.png")),size=(228,190))
place_3_photo = ctk.CTkLabel(root,image=place_3_img,text="")
place_3_photo.place(x=990, y=480)

# "Know more" links
know_more_1 = ctk.CTkLabel(root, text="Know more...", font=("Sriracha Regular", 15), text_color="#00A3FF")
know_more_1.bind('<Enter>', lambda event, label=know_more_1: label.configure(font=('SegoeUI Bold', 15, 'underline')))
know_more_1.bind('<Leave>', lambda event, label=know_more_1: label.configure(font=('SegoeUI Bold', 15)))
know_more_1.place(x=431, y=643)

know_more_2 = ctk.CTkLabel(root, text="Know more...", font=("Sriracha Regular", 15), text_color="#00A3FF")
know_more_2.bind('<Enter>', lambda event, label=know_more_2: label.configure(font=('SegoeUI Bold', 15, 'underline')))
know_more_2.bind('<Leave>', lambda event, label=know_more_2: label.configure(font=('SegoeUI Bold', 15)))
know_more_2.place(x=894, y=643)

# Footer buttons (optional)
nextbttn_img = ctk.CTkImage(Image.open(relative_to_assets("button_1.png")),size=(30,30))
nextPromo_button = ctk.CTkButton(root, text="", image=nextbttn_img, width=10, height=10, corner_radius=100, fg_color="#4B5B6C", bg_color="#4B5B6C", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: print("About Us clicked"))
nextPromo_button.place(x=1173, y=563)
pywinstyles.set_opacity(nextPromo_button,color="#4B5B6C")

root.resizable(False, False)
root.mainloop()
