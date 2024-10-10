from pathlib import Path
from PIL import Image
import customtkinter as ctk 
import pywinstyles

# Set up the asset path (same as original)
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Home")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

root = ctk.CTk()

root.geometry("1280x720")
root.configure(bg="#FFFFFF")  

searchbg_img = ctk.CTkImage(Image.open(relative_to_assets("image_1.png")),size=(1280,253))
searchbg_label = ctk.CTkLabel(root, image=searchbg_img, text="", width=1280, height=253)
searchbg_label.place(x=0, y=0)

# Navigation Tab
nav_img = ctk.CTkImage(Image.open(relative_to_assets("image_2.png")),size=(1280,60))
nav_label = ctk.CTkLabel(root, image=nav_img, text="", width=1280, height=60)
nav_label.place(x=0, y=0)

pfp_img = ctk.CTkImage(Image.open(relative_to_assets("image_3.png")),size=(75,40))
pfp_label = ctk.CTkLabel(root, image=pfp_img, text="", bg_color="#F47749", width=95, height=50)
pfp_label.place(x=5, y=5)
pywinstyles.set_opacity(pfp_label,color="#F47749")

# Relocate buttons
home_button = ctk.CTkButton(master=root, text="Home", width=120, fg_color=("#F95C41","#FA5740"), bg_color="#FA5740", text_color="#FFF6F6", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: print("Home clicked"))
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

# Search Function
search_frame = ctk.CTkLabel(root,text="", fg_color=("#FFFFFF","#D9D9D9"), bg_color="#D9D9D9", width=889, height=101, corner_radius=50)
search_frame.place(x=178,y=126)
pywinstyles.set_opacity(search_frame,color="#D9D9D9")

location_label = ctk.CTkLabel(master=root, text="Place of Rental:", text_color="#000000", fg_color=("#FFFFFF","#D9D9D9"), bg_color="#D9D9D9", font=("SegoeUI Bold", 16))
location_label.place(x=189,y=165)
pywinstyles.set_opacity(location_label,color="#D9D9D9")
date_label = ctk.CTkLabel(master=root, text="Date Of Visit:", text_color="#000000", fg_color=("#FFFFFF","#D9D9D9"), bg_color="#D9D9D9", font=("SegoeUI Bold", 16))
date_label.place(x=580,y=165)
pywinstyles.set_opacity(date_label,color="#D9D9D9")

entry_1 = ctk.CTkEntry(master=root, width=240, height=51, fg_color="#D9D9D9", text_color="#000716", placeholder_text="Place Of Rental")
entry_1.place(x=311, y=150)

entry_2 = ctk.CTkEntry(master=root, width=245, height=51, fg_color="#D9D9D9", text_color="#000716", placeholder_text="Date Of Visit")
entry_2.place(x=693, y=150)

submit_button = ctk.CTkButton(master=root, text="Find", width=85, height=35, fg_color="#067BC1", command=lambda: print("Submit clicked"))
submit_button.place(x=958, y=159)

# Promotions
promotions_label = ctk.CTkLabel(master=root, text="Promotions", text_color="#000000", font=("SegoeUI Bold", 24))
promotions_label.place(x=21, y=261)

promobg_label = ctk.CTkLabel(master=root, text="",fg_color="#EDEDED", width=1280, height=220)
promobg_label.place(x=26,y=300)

promo1_img = ctk.CTkImage(Image.open(relative_to_assets("image_5.png")),size=(275,150))
promo1_label = ctk.CTkLabel(root, image=promo1_img, text="")
promo1_label.place(x=50, y=300)

promo2_img = ctk.CTkImage(Image.open(relative_to_assets("image_6.png")),size=(275,150))
promo2_label = ctk.CTkLabel(root, image=promo2_img, text="")
promo2_label.place(x=364, y=300)

promo3_img = ctk.CTkImage(Image.open(relative_to_assets("image_7.png")),size=(275,150))
promo3_label = ctk.CTkLabel(root, image=promo3_img, text="")
promo3_label.place(x=667, y=300)

promo4_img = ctk.CTkImage(Image.open(relative_to_assets("image_8.png")),size=(275,150))
promo4_label = ctk.CTkLabel(root, image=promo4_img, text="")
promo4_label.place(x=970, y=300)

nextbttn_img = ctk.CTkImage(Image.open(relative_to_assets("button_2.png")),size=(30,30))
nextPromo_button = ctk.CTkButton(master=root, text="", image=nextbttn_img, width=10, height=10, corner_radius=100, fg_color="#4B5B6C", bg_color="#4B5B6C", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: print("About Us clicked"))
nextPromo_button.place(x=1200, y=360)
pywinstyles.set_opacity(nextPromo_button,color="#4B5B6C")

# Extra Content
# Remember to continue
manual_lbl = ctk.CTkLabel(root, text="How to book a car?", fg_color=("#FFFFFF", "25272A"), font=('SegoeUI Bold', 24))
manual_lbl.bind('<Enter>', lambda event, label=manual_lbl: label.configure(font=('SegoeUI Bold', 24, 'underline')))
manual_lbl.bind('<Leave>', lambda event, label=manual_lbl: label.configure(font=('SegoeUI Bold', 24)))
manual_lbl.place(x=251,y=490)
pywinstyles.set_opacity(manual_lbl,color="#FFFFFF")

tnc_lbl = ctk.CTkLabel(root, text="Terms & Conditions", fg_color=("#FFFFFF", "25272A"), font=('SegoeUI Bold', 24))
tnc_lbl.bind('<Enter>', lambda event, label=tnc_lbl: label.configure(font=('SegoeUI Bold', 24, 'underline')))
tnc_lbl.bind('<Leave>', lambda event, label=tnc_lbl: label.configure(font=('SegoeUI Bold', 24)))
tnc_lbl.place(x=754,y=490)
pywinstyles.set_opacity(tnc_lbl,color="#FFFFFF")

footer_frame = ctk.CTkLabel(root,text="", fg_color="#2A333D", width=1280, height=180)
footer_frame.place(x=0,y=550)

# Account section
account_label = ctk.CTkLabel(master=root, text="Account", fg_color="#4B5B6C", text_color="#4B5B6D", font=("Tw Cen MT Condensed Extra Bold", 32))
account_label.place(x=140,y=587)
pywinstyles.set_opacity(account_label,color="#4B5B6C")

myprofile_label = ctk.CTkLabel(master=root, text="My Profile", bg_color="#9DA2AA", text_color="#9EA3A9", font=("Tw Cen MT Condensed Extra Bold", 20))
myprofile_label.place(x=290,y=577)
pywinstyles.set_opacity(myprofile_label,color="#9DA2AA")
aboutus_label = ctk.CTkLabel(master=root, text="About Car2U", bg_color="#9DA2AA", text_color="#9EA3A9", font=("Tw Cen MT Condensed Extra Bold", 20))
aboutus_label.place(x=290,y=620)
pywinstyles.set_opacity(aboutus_label,color="#9DA2AA")
upRenter_label = ctk.CTkLabel(master=root, text="Upgrade to Renter", bg_color="#9DA2AA", text_color="#9EA3A9", font=("Tw Cen MT Condensed Extra Bold", 20))
upRenter_label.place(x=430,y=577)
pywinstyles.set_opacity(upRenter_label,color="#9DA2AA")
upMember_label = ctk.CTkLabel(master=root, text="Upgrade to Member", bg_color="#9DA2AA", text_color="#9EA3A9", font=("Tw Cen MT Condensed Extra Bold", 20))
upMember_label.place(x=430,y=620)
pywinstyles.set_opacity(upMember_label,color="#9DA2AA")

# Support section
support_label = ctk.CTkLabel(master=root, text="Support", fg_color="#4B5B6C", text_color="#4B5B6D", font=("Tw Cen MT Condensed Extra Bold", 32))
support_label.place(x=725, y=587)
pywinstyles.set_opacity(support_label,color="#4B5B6C")

guide_label = ctk.CTkLabel(master=root, text="Car2U Guide", bg_color="#9DA2AA", text_color="#9EA3A9", font=("Tw Cen MT Condensed Extra Bold", 24))
guide_label.place(x=880,y=577)
pywinstyles.set_opacity(guide_label,color="#9DA2AA")
findus_label = ctk.CTkLabel(master=root, text="Find Us", bg_color="#9DA2AA", text_color="#9EA3A9", font=("Tw Cen MT Condensed Extra Bold", 24))
findus_label.place(x=880,y=620)
pywinstyles.set_opacity(findus_label,color="#9DA2AA")

rights_label = ctk.CTkLabel(master=root, text="@All Rights Reserved", fg_color="#9EA3A9", text_color="#FFFFFF", font=("Tw Cen MT Condensed Extra Bold", 16))
rights_label.place(x=562, y=680)
pywinstyles.set_opacity(rights_label,color="#9EA3A9")

root.resizable(False, False)
root.mainloop()
