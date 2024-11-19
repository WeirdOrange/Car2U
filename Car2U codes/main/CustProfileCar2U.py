import customtkinter as ctk
import pywinstyles
import sqlite3
from MainCar2U_UserInfo import get_user_info,set_user_info
from tkinter import Toplevel, messagebox, filedialog
from tkcalendar import Calendar, DateEntry
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageTk
from io import BytesIO

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Cust-Profile")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Function to handle login button click
def open_login(current_window, login_callback):
    current_window.destroy()  # Close the signup window
    userInfo = ""
    set_user_info(userInfo)
    login_callback()

# Function to handle selection button click
def open_home(current_window, home_callback):
    current_window.destroy()  # Close the signup window
    home_callback()

# Function to handle selection button click
def open_listing(current_window, list_callback):
    current_window.destroy()  # Close the signup window
    list_callback()

# Function to handle profile button click
def open_profile():
    messagebox.showinfo("Oops.","You are on the profile page")

# Function to handle about us button click
def open_aboutUs(current_window, about_callback):
    current_window.destroy()  # Close the signup window
    about_callback()

# Function to handle profile button click
def open_review(current_window, review_callback):
    current_window.destroy()  # Close the signup window
    review_callback()

# Function to handle chats button click
def open_chat(current_window, chat_callback):
    current_window.destroy()  # Close the window
    chat_callback()

def Database(): #creating connection to database and creating table
    global conn, cursor
    conn = sqlite3.connect("car2u.db")
    # Enable access to columns by name
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

def fetch_user_data():
    global result
    Database()
    userInfo = get_user_info()
    print(f"UserID : {userInfo}")
    query = f"""SELECT *,(date()-dob) AS age FROM UserDetails where userID = '{userInfo}'"""
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    accInfo()

def accInfo():
    for widget in info_frame.winfo_children():
        if isinstance(widget, (ctk.CTkFrame,ctk.CTkLabel,ctk.CTkEntry,ctk.CTkComboBox,ctk.CTkButton)):
            widget.destroy()
    # Check if dobEntry and nameEntry exists before trying to destroy it
    if 'nameEntry' in globals() and isinstance(nameEntry, ctk.CTkEntry):
        if isinstance(nameEntry,ctk.CTkEntry):
            nameEntry.destroy()
    if 'dobEntry' in globals() and isinstance(dobEntry, DateEntry):
        if isinstance(dobEntry,DateEntry):
            dobEntry.destroy()

    global name,email,gender,dob,contact,nationality, infoData, user_name_label,pfp_image
    infoData = []
    for row in result:
        name = row[1]
        infoData.append(name)
        email = row[2]
        infoData.append(email)
        gender = row[4]
        if gender == 0:
            gender = "Male"
            infoData.append(gender)
        else:
            gender = "Female"
            infoData.append(gender)
        infoData.append(row[5])
        age = row[10]
        contact = row[6]
        infoData.append(contact)
        nationality = row[7]
        infoData.append(nationality)
        pfp = row[8]

        if pfp != None:
            pfp_img = convert_data(pfp)
        else:
            pfp_img = ctk.CTkImage(Image.open(relative_to_assets("image_6.png")),size=(240,240))

        dob = datetime.strptime(row[5],"%Y-%m-%d")
        dob = dob.date()
        print(dob)
    
    # Placeholder for user image
    user_image = ctk.CTkButton(profileFrame, image=pfp_img, text="", width=240, height=240, fg_color="#D9D9D9", 
                               command=lambda: convertToBinaryData())
    user_image.place(x=40, y=153)
    pywinstyles.set_opacity(user_image,color="#D9D9D9")

    info_labels = [("Email:", 10), ("Date Of Birth:", 50), ("Phone Number:", 90), ("Gender:", 130), ("Nationality:", 170)]
    for text, y_pos in info_labels:
        label = ctk.CTkLabel(info_frame, text=text, font=("Skranji", 20), text_color="#000000")
        label.place(x=15, y=y_pos)

    info_labels = [(email, 10), (age, 50), (contact, 90), (gender, 130), (nationality, 170)]
    for text, y_pos in info_labels:
        label = ctk.CTkLabel(info_frame, text=text, font=("Skranji", 20), text_color="#000000")
        label.place(x=175, y=y_pos)

    dob_label = ctk.CTkLabel(info_frame, text="Birth Date: ", font=("Skranji", 20), text_color="#000000")
    dob_label.place(x=400, y=50)
    userDOB = ctk.CTkLabel(info_frame, text=dob, font=("Skranji", 20), text_color="#000000")
    userDOB.place(x=500, y=50)

    user_name_label = ctk.CTkLabel(profileFrame, text=name, font=("Cooper Black", 40), text_color="#000000")
    user_name_label.place(x=346, y=90)
    
    edit_info = ctk.CTkButton(info_frame, text="Edit", width=80, corner_radius=50, fg_color="#F95F43", bg_color="#FFFFFF",
                              font=("Tw Cen MT Condensed Extra Bold", 16), command=lambda: editInfo())
    edit_info.place(x=625, y=218)
        
    print(infoData)

def editInfo():
    def genderSelect():
        global returnGender
        returnGender = genderEntry.get()
        if returnGender == "Male":
            returnGender = 1
        else:
            returnGender = 0
        return returnGender
    for widget in info_frame.winfo_children():
        if isinstance(widget, (ctk.CTkFrame,ctk.CTkLabel,ctk.CTkButton)):
            widget.destroy()
    if isinstance(user_name_label,ctk.CTkLabel):
        user_name_label.destroy()

    info_labels = [("Email:", 10), ("Date Of Birth:", 50), ("Phone Number:", 90), ("Gender:", 130), ("Nationality:", 170)]
    for text, y_pos in info_labels:
        label = ctk.CTkLabel(info_frame, text=text, font=("Skranji", 20), anchor='e', text_color="#000000")
        label.place(x=15, y=y_pos)
    # Entries 
    global nameEntry
    nameEntry = ctk.CTkEntry(profileFrame, width=438, height=50, font=("Skranji", 40), text_color="#000000")
    nameEntry.insert(0,name)
    nameEntry.place(x=346, y=90)

    emailEntry = ctk.CTkEntry(info_frame, width=438, height=28, font=("Skranji", 20), text_color="#000000")
    emailEntry.insert(0,email)
    emailEntry.place(x=175, y=10)

    contactEntry = ctk.CTkEntry(info_frame, width=438, height=28, font=("Skranji", 20), text_color="#000000")
    if contact != None:
        contactEntry.insert(0,contact)
    contactEntry.place(x=175, y=90)
    
    genderEntry = ctk.CTkComboBox(master=info_frame, width=438, height=28, state="readonly", values=["","Male", "Female"], font=("Skranji", 20))
    if gender != None:
        genderEntry.set(gender)
    else:
        genderEntry.set("")
    genderEntry.bind("<<ComboboxSelected>>", genderSelect())
    genderEntry.place(x=175, y=130)

    nationalityEntry = ctk.CTkEntry(info_frame, width=438, height=28, font=("Skranji", 20), text_color="#000000")
    if nationality != None:
        nationalityEntry.insert(0,nationality)
    nationalityEntry.place(x=175, y=170)
    
    global dobEntry
    dobEntry = DateEntry(profileFrame, date_pattern='yyyy-mm-dd', locale='en_US', font=("Skranji", 12), text_color="#000000")
    if dobEntry != None:
        dobEntry.set_date(dob)
    dobEntry.place(x=520, y=206)

    edit_info = ctk.CTkButton(info_frame, text="Done", width=80, corner_radius=50, fg_color="#F95F43", bg_color="#FFFFFF",
                              font=("Tw Cen MT Condensed Extra Bold", 16), 
                              command=lambda: info_Update_Checker(nameEntry.get(),emailEntry.get(),contactEntry.get(),returnGender,nationalityEntry.get()))
    edit_info.place(x=625, y=218)

def info_Update_Checker(returnName,returnEmail,returnContact,returnGender,returnNationality):
    Database()
    returnDOB = dobEntry.get_date()
    returnDOB = str(returnDOB)

    if not returnName or not returnEmail or not returnContact or not returnDOB or not returnNationality:
        messagebox.showerror("Input Error", "All fields are required!")
    elif returnName == name and returnEmail == email and returnContact == contact and returnDOB == dob and returnGender == gender and returnNationality == nationality:
        messagebox.showerror("Nothing Changed.")
        fetch_user_data()
    else:
        try:
            if returnGender == 'Male':
                returnGender = 1
            else:
                returnGender = 0
            cursor.execute(f"UPDATE UserDetails SET name=?,email=?,gender=?,dob=?,contactNo=?,nationality=? WHERE userID = {get_user_info()}",
                           (str(returnName),str(returnEmail),str(returnGender),returnDOB,str(returnContact),str(returnNationality)))
            conn.commit()
            messagebox.showinfo("Update Successful", "You have successfully update your info!")
            fetch_user_data()
        except sqlite3.Error as e:
            messagebox.showerror("Error", "Error occurred during registration: {}".format(e))
        finally:
            conn.close()

def accManage(current_window, login_callback,review_callback):
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
                                        bg_color="#E6F6FF", font=("SegoeUI Bold", 20), command=lambda:open_profile())
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

def convertToBinaryData(): 
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        try:
            # Convert binary format to images
            with open(file_path, 'rb') as file: 
                blobData = file.read() 
                insertBLOB(blobData)
            return blobData 
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload image: {e}")
            
def convert_data(data):
    global pfp_img
    img_byte = BytesIO(data)
    img = Image.open(img_byte)
    img = img.resize((240,240), Image.Resampling.LANCZOS)
    pfp_img = ImageTk.PhotoImage(img)
    return pfp_img

def insertBLOB(data): 
    try: 
        Database()
        # insert query 
        sqlite_insert_blob_query = f"""UPDATE UserDetails SET profilePic=? WHERE userID = {get_user_info()}"""
        
        # using cursor object executing our query 
        cursor.execute(sqlite_insert_blob_query, (data,))
        conn.commit() 
        print("Image and file inserted successfully as a BLOB into a table") 
        cursor.close() 
  
    except sqlite3.Error as error: 
        print("Failed to insert blob data into sqlite table", error) 
        messagebox.showinfo("Failed to insert blob data into sqlite table", error) 
      
    finally: 
        if conn: 
            conn.close() 
            print("the sqlite connection is closed") 
            fetch_user_data()

def profile(login_callback,home_callback,list_callback,about_callback,review_callback, chat_callback):
    # Create the main application window
    global profileFrame
    profileFrame = Toplevel()
    profileFrame.title("Profile Page")
    profileFrame.geometry("1280x720")
    profileFrame.resizable(False, False)
    profileFrame.config(bg="white")

    global userInfo
    userInfo = get_user_info()
    print(f"Profile : {userInfo}")

    # Background
    bg_img = ctk.CTkImage(Image.open(relative_to_assets("image_1.png")),size=(1280,720))
    bg_label = ctk.CTkLabel(profileFrame, image=bg_img, text="", width=1280, height=60)
    bg_label.place(x=0, y=0)

    # Navigation Bar
    header = ctk.CTkFrame(profileFrame, width=1280, height=60, fg_color="#FFFFFF")
    header.place(x=0, y=0)

    navbg_img = ctk.CTkImage(Image.open(relative_to_assets("nav.png")),size=(1280,60))
    navbg_label = ctk.CTkLabel(header, image=navbg_img, text="", width=1280, height=60)
    navbg_label.place(x=0, y=0)

    # Relocating buttons
    home_button = ctk.CTkButton(master=profileFrame, text="Home", width=120, fg_color=("#F95C41","#FA5740"), bg_color="#FA5740", 
                                text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), 
                                command=lambda: open_home(profileFrame,home_callback))
    home_button.place(x=627, y=14)
    pywinstyles.set_opacity(home_button,color="#FA5740")

    selections_button = ctk.CTkButton(master=profileFrame, text="Selections", width=120, fg_color=("#FA5740","#FB543F"), bg_color="#FB543F", 
                                      text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), 
                                      command=lambda: open_listing(profileFrame,list_callback))
    selections_button.place(x=763, y=14)
    pywinstyles.set_opacity(selections_button,color="#FB543F")

    contact_us_button = ctk.CTkButton(master=profileFrame, text="Contact Us", width=120, fg_color=("#FB543F","#FC503E"), bg_color="#FC503E", 
                                      text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), 
                                      command=lambda: open_chat(profileFrame, chat_callback))
    contact_us_button.place(x=910, y=14)
    pywinstyles.set_opacity(contact_us_button,color="#FC503E")

    about_us_button = ctk.CTkButton(master=profileFrame, text="About Us", width=120, fg_color=("#FC503E","#FC4D3D"), bg_color="#FC4D3D", 
                                    text_color="#000000", font=("Tw Cen MT Condensed Extra Bold", 20), 
                                    command=lambda: open_aboutUs(profileFrame, about_callback))
    about_us_button.place(x=1055, y=14)
    pywinstyles.set_opacity(about_us_button,color="#FC4D3D")

    logo_img = ctk.CTkImage(Image.open(relative_to_assets("logo.png")),size=(75,40))
    logo_label = ctk.CTkLabel(profileFrame, image=logo_img, text="", bg_color="#F47749", width=95, height=50)
    logo_label.place(x=5, y=5)
    pywinstyles.set_opacity(logo_label,color="#F47749")

    global pfpState
    pfpState = 1
    pfp_img = ctk.CTkImage(Image.open(relative_to_assets("image_6.png")),size=(40,40))
    pfp_label = ctk.CTkButton(profileFrame, image=pfp_img, text="", bg_color="#F47749", fg_color="#F47749",
                              width=40, height=40, command=lambda:accManage(profileFrame,login_callback,review_callback))
    pfp_label.place(x=1180, y=5)
    pywinstyles.set_opacity(pfp_label,color="#F47749")

    # User Info section
    # Personal information section
    global info_frame
    info_frame = ctk.CTkFrame(profileFrame, width=757, height=260, fg_color="#FFFFFF", border_width=2, border_color="grey")
    info_frame.place(x=345, y=152)

    fetch_user_data()

    # "Top Places to Visit" Section
    places_label = ctk.CTkLabel(profileFrame, text="Top Places to Visit", font=("Skranji", 36), text_color="#000000")
    places_label.place(x=70, y=427)
    pywinstyles.set_opacity(places_label,color="#FFFFFF")

    # Top places background
    place_bg = ctk.CTkFrame(profileFrame, width=1170, height=210, border_width=2,fg_color="white")
    place_bg.place(x=55,y=470)

    # Placeholders for destination images
    place_1_img = ctk.CTkImage(Image.open(relative_to_assets("image_2.png")),size=(260,190))
    place_1_photo = ctk.CTkLabel(profileFrame,image=place_1_img,text="")
    place_1_photo.place(x=65, y=480)
    place_1 = ctk.CTkLabel(profileFrame, text="Penang", fg_color="#FFFFFF")
    place_1.place(x=355, y=510)

    place_2_img = ctk.CTkImage(Image.open(relative_to_assets("image_4.png")),size=(260,190))
    place_2_photo = ctk.CTkLabel(profileFrame,image=place_2_img,text="")
    place_2_photo.place(x=530, y=480)
    place_2 = ctk.CTkLabel(profileFrame, text="Kuala\n\tLumpur", fg_color="#FFFFFF")
    place_2.place(x=810, y=520)

    place_3_img = ctk.CTkImage(Image.open(relative_to_assets("image_5.png")),size=(228,190))
    place_3_photo = ctk.CTkLabel(profileFrame,image=place_3_img,text="")
    place_3_photo.place(x=990, y=480)

    # "Know more" links
    know_more_1 = ctk.CTkLabel(profileFrame, text="Know more...", font=("Sriracha Regular", 15), text_color="#00A3FF")
    know_more_1.bind('<Enter>', lambda event, label=know_more_1: label.configure(font=('SegoeUI Bold', 15, 'underline')))
    know_more_1.bind('<Leave>', lambda event, label=know_more_1: label.configure(font=('SegoeUI Bold', 15)))
    know_more_1.place(x=431, y=643)

    know_more_2 = ctk.CTkLabel(profileFrame, text="Know more...", font=("Sriracha Regular", 15), text_color="#00A3FF")
    know_more_2.bind('<Enter>', lambda event, label=know_more_2: label.configure(font=('SegoeUI Bold', 15, 'underline')))
    know_more_2.bind('<Leave>', lambda event, label=know_more_2: label.configure(font=('SegoeUI Bold', 15)))
    know_more_2.place(x=894, y=643)

    # Footer buttons (optional)
    nextbttn_img = ctk.CTkImage(Image.open(relative_to_assets("button_1.png")),size=(30,30))
    nextPromo_button = ctk.CTkButton(profileFrame, text="", image=nextbttn_img, width=10, height=10, corner_radius=100, fg_color="#4B5B6C", bg_color="#4B5B6C", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: print("About Us clicked"))
    nextPromo_button.place(x=1173, y=563)
    pywinstyles.set_opacity(nextPromo_button,color="#4B5B6C")
