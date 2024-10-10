import customtkinter as ctk
import tkinter as tk
import pywinstyles
from tkcalendar import DateEntry
from pathlib import Path
from PIL import Image

# Set up the asset path (same as original)
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Selections")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Hover over Items
def focus_frame(frame):
    frame.configure(fg_color="yellow")
def unfocus_frame(frame):
    frame.configure(fg_color="#FFFFFF")

# Create the main application window
root = tk.Tk()
root.title("Car Rental Interface")
root.geometry("1280x720")
root.resizable(False, False)

# Load the background image
bg_img = ctk.CTkImage(Image.open(relative_to_assets("image_1.png")),size=(1280,700))
bg_label = ctk.CTkLabel(root, image=bg_img, text="")
bg_label.place(x=185, y=40, relwidth=1, relheight=1)

# Navigation Tab
nav_img = ctk.CTkImage(Image.open(relative_to_assets("image_2.png")),size=(1280,60))
nav_label = ctk.CTkLabel(root, image=nav_img, text="", width=1280, height=60)
nav_label.place(x=0, y=0)

logo_img = ctk.CTkImage(Image.open(relative_to_assets("image_3.png")),size=(75,40))
logo_label = ctk.CTkLabel(root, image=logo_img, text="", bg_color="#F47749", width=95, height=50)
logo_label.place(x=5, y=5)
pywinstyles.set_opacity(logo_label,color="#F47749")

pfp_img = ctk.CTkImage(Image.open(relative_to_assets("image_4.png")),size=(40,40))
pfp_label = ctk.CTkLabel(root, image=pfp_img, text="", bg_color="#FE453B", width=95, height=50)
pfp_label.place(x=1170, y=5)
pywinstyles.set_opacity(pfp_label,color="#FE453B")

# Relocate buttons
home_button = ctk.CTkButton(master=root, text="Home", width=120, fg_color=("#F95C41","#FA5740"), bg_color="#FA5740", text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: print("Home clicked"))
home_button.place(x=627, y=14)
pywinstyles.set_opacity(home_button,color="#FA5740")

selections_button = ctk.CTkButton(master=root, text="Selections", width=120, fg_color=("#FA5740","#FB543F"), bg_color="#FB543F", text_color="#FFF6F6", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: print("Selections clicked"))
selections_button.place(x=763, y=14)
pywinstyles.set_opacity(selections_button,color="#FB543F")

contact_us_button = ctk.CTkButton(master=root, text="Contact Us", width=120, fg_color=("#FB543F","#FC503E"), bg_color="#FC503E", text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: print("Contact Us clicked"))
contact_us_button.place(x=910, y=14)
pywinstyles.set_opacity(contact_us_button,color="#FC503E")

about_us_button = ctk.CTkButton(master=root, text="About Us", width=120, fg_color=("#FC503E","#FC4D3D"), bg_color="#FC4D3D", text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: print("About Us clicked"))
about_us_button.place(x=1055, y=14)
pywinstyles.set_opacity(about_us_button,color="#FC4D3D")

# Locations frame
location_frame = ctk.CTkFrame(root, corner_radius=0, width=1090, height=90, fg_color="light grey")
location_frame.place(x=190, y=60)

# Pickup entry
locateIcon_img = ctk.CTkImage(Image.open(relative_to_assets("image_6.png")),size=(40,40))
locateIcon_label = ctk.CTkLabel(location_frame, image=locateIcon_img, text="")
locateIcon_label.place(x=30, y=40)

dateIcon_img = ctk.CTkImage(Image.open(relative_to_assets("image_7.png")),size=(40,40))
dateIcon_label = ctk.CTkLabel(location_frame, image=dateIcon_img, text="")
dateIcon_label.place(x=280, y=40)

pickup_text = ctk.CTkLabel(location_frame, text="Pick-up Details", fg_color="#D7D7D7", font=("Tw Cen MT Condensed Extra Bold", 20))
pickup_text.place(x=30,y=10)
pywinstyles.set_opacity(pickup_text,color="#D7D7D7")

pickup_entry = ctk.CTkEntry(location_frame, font=("Arial", 10), width=100, fg_color="#bbbbbb")
pickup_entry.place(x=85, y=50)
pickup_date = DateEntry(location_frame, width=12, background='orange', foreground='white', borderwidth=2, font=("Arial", 10))
pickup_date.place(x=345, y=50)

# Drop-off entry
locateIcon2_img = ctk.CTkImage(Image.open(relative_to_assets("image_6.png")),size=(40,40))
locateIcon2_label = ctk.CTkLabel(location_frame, image=locateIcon2_img, text="")
locateIcon2_label.place(x=565, y=40)

dateIcon2_img = ctk.CTkImage(Image.open(relative_to_assets("image_7.png")),size=(40,40))
dateIcon2_label = ctk.CTkLabel(location_frame, image=dateIcon2_img, text="")
dateIcon2_label.place(x=815, y=40)

dropoff_text = ctk.CTkLabel(location_frame, text="Drop-off Details", fg_color="#D7D7D7", font=("Tw Cen MT Condensed Extra Bold", 20))
dropoff_text.place(x=565,y=5)
pywinstyles.set_opacity(dropoff_text,color="#D7D7D7")

dropoff_entry = ctk.CTkEntry(location_frame, font=("Arial", 10), width=100, fg_color="#bbbbbb")
dropoff_entry.place(x=620, y=50)
dropoff_date = DateEntry(location_frame, width=12, background='orange', foreground='white', borderwidth=2, font=("Arial", 10))
dropoff_date.place(x=880, y=50)

# Create a frame for the filter options
filter_frame = ctk.CTkFrame(root, corner_radius=0, width=190, height=670, fg_color="white")
filter_frame.place(x=0, y=60)

# Brand options
brand_label = ctk.CTkLabel(filter_frame, text="Brand", font=("Arial", 20))
brand_label.place(x=10, y=10)

brand_vars = []
brands = ["Toyota", "Mazda", "Perodua", "Mercedes"]
for i, brand in enumerate(brands):
    var = ctk.IntVar()
    chk = ctk.CTkCheckBox(filter_frame, text=brand, variable=var, font=("Arial", 16))
    chk.place(x=10, y=50 + i * 30)
    brand_vars.append(var)

# Seating Capacity options
capacity_label = ctk.CTkLabel(filter_frame, text="Seating Capacity", font=("Arial", 20))
capacity_label.place(x=10, y=180)

capacity_vars = []
capacities = ["2-seater", "4-seater", "6-seater"]
for i, capacity in enumerate(capacities):
    var = ctk.IntVar()
    chk = ctk.CTkCheckBox(filter_frame, text=capacity, variable=var, font=("Arial", 16))
    chk.place(x=10, y=210 + i * 30)
    capacity_vars.append(var)

# Transmission Type options
transmission_label = ctk.CTkLabel(filter_frame, text="Transmission Type", font=("Arial", 20))
transmission_label.place(x=10, y=310)

transmission_vars = []
transmissions = ["Manual", "Automatic"]
for i, transmission in enumerate(transmissions):
    var = ctk.IntVar()
    chk = ctk.CTkCheckBox(filter_frame, text=transmission, variable=var, font=("Arial", 16))
    chk.place(x=10, y=340 + i * 30)
    transmission_vars.append(var)

# Item List Framing
item_frame1 = ctk.CTkFrame(root,width=320, height=225, corner_radius=30, fg_color="#FFFFFF",bg_color="#FEFEFE")
item_frame1.place(x=210,y=190)
item_frame1.bind("<Enter>", lambda event, f=item_frame1: focus_frame(f))  # Hovering on frame
item_frame1.bind("<Leave>", lambda event, f=item_frame1: unfocus_frame(f))
pywinstyles.set_opacity(item_frame1, color="#FEFEFE")

item_frame2 = ctk.CTkFrame(root,width=320, height=225, corner_radius=30, fg_color="#FFFFFF",bg_color="#FEFEFE")
item_frame2.place(x=570,y=190)
item_frame2.bind("<Enter>", lambda event, f=item_frame2: focus_frame(f))  # Hovering on frame
item_frame2.bind("<Leave>", lambda event, f=item_frame2: unfocus_frame(f))
pywinstyles.set_opacity(item_frame2, color="#FEFEFE")

item_frame3 = ctk.CTkFrame(root,width=320, height=225, corner_radius=30, fg_color="#FFFFFF",bg_color="#FEFEFE")
item_frame3.place(x=930,y=190)
item_frame3.bind("<Enter>", lambda event, f=item_frame3: focus_frame(f))  # Hovering on frame
item_frame3.bind("<Leave>", lambda event, f=item_frame3: unfocus_frame(f))
pywinstyles.set_opacity(item_frame3, color="#FEFEFE")

item_frame4 = ctk.CTkFrame(root,width=320, height=225, corner_radius=30, fg_color="#FFFFFF",bg_color="#FEFEFE")
item_frame4.place(x=210,y=450)
item_frame4.bind("<Enter>", lambda event, f=item_frame4: focus_frame(f))  # Hovering on frame
item_frame4.bind("<Leave>", lambda event, f=item_frame4: unfocus_frame(f))
pywinstyles.set_opacity(item_frame4, color="#FEFEFE")

item_frame5 = ctk.CTkFrame(root,width=320, height=225, corner_radius=30, fg_color="#FFFFFF",bg_color="#FEFEFE")
item_frame5.place(x=570,y=450)
item_frame5.bind("<Enter>", lambda event, f=item_frame5: focus_frame(f))  # Hovering on frame
item_frame5.bind("<Leave>", lambda event, f=item_frame5: unfocus_frame(f))
pywinstyles.set_opacity(item_frame5, color="#FEFEFE")

item_frame6 = ctk.CTkFrame(root,width=320, height=225, corner_radius=30, fg_color="#FFFFFF",bg_color="#FEFEFE")
item_frame6.place(x=930,y=450)
item_frame6.bind("<Enter>", lambda event, f=item_frame6: focus_frame(f))  # Hovering on frame
item_frame6.bind("<Leave>", lambda event, f=item_frame6: unfocus_frame(f))
pywinstyles.set_opacity(item_frame6, color="#FEFEFE")

# Item Contents
# First Item
name_car1 = "Mercedes C250 | Silver"
seaters_car1 = "4-seater"
transmission_car1 = "Automatic"
price_car1 = "160"

car1_img =  ctk.CTkImage(Image.open(relative_to_assets("image_28.png")),size=(250,125))
car1_label = ctk.CTkLabel(item_frame1, image=car1_img, bg_color="#FFFFFF", text="")
car1_label.place(x=35, y=5)
pywinstyles.set_opacity(car1_label, color="#FFFFFF")

car1_name = ctk.CTkLabel(item_frame1, text=name_car1, fg_color="#FFFFFF", bg_color="#FFFFFF", font=("Tw Cen MT Condensed Extra Bold", 20))
car1_name.place(x=8,y=130)
pywinstyles.set_opacity(car1_name, color="#FFFFFF")

seats_img =  ctk.CTkImage(Image.open(relative_to_assets("image_11.png")),size=(30,30))
seatIcon1 = ctk.CTkLabel(item_frame1, image=seats_img, bg_color="#FFFFFF", text="")
seatIcon1.place(x=9, y=170)
pywinstyles.set_opacity(seatIcon1, color="#FFFFFF")
car1_seats = ctk.CTkLabel(item_frame1, text=seaters_car1, fg_color="#FFFFFF", bg_color="#FFFFFF", font=("Tw Cen MT Condensed Extra Bold", 16))
car1_seats.place(x=40,y=175)
pywinstyles.set_opacity(car1_seats, color="#FFFFFF")

transmission_img =  ctk.CTkImage(Image.open(relative_to_assets("image_12.png")),size=(30,30))
transIcon1 = ctk.CTkLabel(item_frame1, image=transmission_img, bg_color="#FFFFFF", text="")
transIcon1.place(x=110, y=170)
pywinstyles.set_opacity(transIcon1, color="#FFFFFF")
car1_trans = ctk.CTkLabel(item_frame1, text=transmission_car1, fg_color="#FFFFFF", bg_color="#FFFFFF", font=("Tw Cen MT Condensed Extra Bold", 16))
car1_trans.place(x=145,y=175)
pywinstyles.set_opacity(car1_trans, color="#FFFFFF")

price_img =  ctk.CTkImage(Image.open(relative_to_assets("image_13.png")),size=(30,30))
priceIcon1 = ctk.CTkLabel(item_frame1, image=price_img, bg_color="#FFFFFF", text="")
priceIcon1.place(x=220, y=170)
pywinstyles.set_opacity(priceIcon1, color="#FFFFFF")
car1_price = ctk.CTkLabel(item_frame1, text=(f"{price_car1}/day"), fg_color="#FFFFFF", bg_color="#FFFFFF", font=("Tw Cen MT Condensed Extra Bold", 16))
car1_price.place(x=250,y=175)
pywinstyles.set_opacity(car1_price, color="#FFFFFF")



# Start the main loop
root.mainloop()
