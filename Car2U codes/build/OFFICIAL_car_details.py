import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk, Toplevel
from PIL import Image, ImageTk
from pathlib import Path
import pywinstyles
import sqlite3

# Set up the asset path (same as original)
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\\Ivan\\Ivan\\Ivan\\Deg CS\\ALL Project\\Car2U\\Car2U codes\\main\\assets\\Details")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Connect to the database and create the tables if they don't exist
def connect_db():
    conn = sqlite3.connect('CAR2U.db')
    cursor = conn.cursor()

    # Create CarDetails table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CarDetails (
            carID INTEGER PRIMARY KEY AUTOINCREMENT,
            registrationNo VARCHAR(10) UNIQUE,
            model VARCHAR(20) NOT NULL,
            colour VARCHAR(20) NOT NULL,
            fuelType VARCHAR(20) NOT NULL,
            seatingCapacity VARCHAR(20) NOT NULL,
            transmissionType VARCHAR(20) NOT NULL,
            price REAL NOT NULL,
            carImage BLOB,
            agencyID INTEGER NOT NULL,
            dateCreated DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (agencyID) REFERENCES RentalAgency(agencyID)
        )
    ''')

    # Create RentalAgency table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS RentalAgency (
            agencyID INTEGER PRIMARY KEY AUTOINCREMENT,
            agencyName VARCHAR(30) NOT NULL,
            agencyLocation VARCHAR(100) NOT NULL,
            agencyEmail VARCHAR(150) NOT NULL UNIQUE,
            agencyPassword VARCHAR(100) NOT NULL,
            agencyContactNo VARCHAR(15) NOT NULL,
            agencyLogo BLOB,
            dateCreated DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    return conn

# Function to save data to the database
def save_data(agencyName,registrationNo,model,colour,fuelType,seatingCapacity,transmissionType,price):
    try:
        price = float(price)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for the price rate.")
        return
   
       # Validate image path
    if not hasattr(upload_label, 'image_path'):
        messagebox.showerror("No Image", "Please upload an image.")
        return

    carImage = upload_label.image_path

    # Get agencyID from agency name
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT agencyID FROM RentalAgency WHERE agencyName = ?', (agencyName,))
    agency_data = cursor.fetchone()

    if agency_data:
        agencyID = agency_data[0]
    else:
        messagebox.showerror("Error", "Selected agency does not exist.")
        conn.close()
        return

    # Save data to the CarDetails table
    cursor.execute('''
        INSERT INTO CarDetails (registrationNo, model, colour, fuelType, seatingCapacity, transmissionType, price, carImage, agencyID)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (registrationNo, model, colour, fuelType, seatingCapacity, transmissionType, price, carImage, agencyID))

    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Data saved successfully!")
    refresh_treeview()

# Function to refresh treeview
def refresh_treeview():
    for row in treeview.get_children():
        treeview.delete(row)

    conn = connect_db()
    cursor = conn.cursor()

    # Join CarDetails with RentalAgency to fetch agency names
    cursor.execute('''
        SELECT c.carID, r.agencyName, c.registrationNo, c.model, c.colour, c.fuelType, c.seatingCapacity, c.transmissionType, c.price
        FROM CarDetails c
        JOIN RentalAgency r ON c.agencyID = r.agencyID
    ''')

    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        treeview.insert("", "end", values=row)

# Function to clear all entry boxes
def clear_entries():
    selected_agency.set("Select")
    entry_registration.delete(0, tk.END)
    entry_model.delete(0, tk.END)
    entry_colour.delete(0, tk.END)
    selected_fuel.set("Select")
    selected_seat.set("Select")
    selected_transmission.set("Select")
    entry_price.delete(0, tk.END)
    upload_label.config(image="", text="No Image Uploaded")
    if hasattr(upload_label, 'image_path'):
        del upload_label.image_path

# Function to delete selected car data
def delete_data():
    selected_item = treeview.selection()
    if selected_item:
        item_values = treeview.item(selected_item, 'values')
        carID = item_values[0]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM CarDetails WHERE carID = ?', (carID,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Car data deleted successfully!")
        refresh_treeview()
    else:
        messagebox.showwarning("No selection", "Please select a car record to delete.")

# Function to update existing car data
def update_data():
    selected_item = treeview.selection()
    if selected_item:
        carID = treeview.item(selected_item, 'values')[0]

        rentalAgency = selected_agency.get()
        registrationNo = entry_registration.get()
        model = entry_model.get()
        colour = entry_colour.get()
        fuelType = selected_fuel.get()
        seatingCapacity = selected_seat.get()
        transmissionType = selected_transmission.get()

        try:
            price = float(entry_price.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the price.")
            return

        if not hasattr(upload_label, 'image_path'):
            messagebox.showerror("No Image", "Please upload an image.")
            return

        carImage = upload_label.image_path

        # Get agencyID from agency name
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT agencyID FROM rentalAgency WHERE agencyName = ?', (rentalAgency,))
        agency_data = cursor.fetchone()

        if agency_data:
            agencyID = agency_data[0]
        else:
            messagebox.showerror("Error", "Selected agency does not exist.")
            conn.close()
            return

        cursor.execute('''
        UPDATE CarDetails
        SET registrationNo=?, model=?, colour=?, fuelType=?, seatingCapacity=?, transmissionType=?, price=?, carImage=?, agencyID=?
        WHERE carID=?
        ''', (registrationNo, model, colour, fuelType, seatingCapacity, transmissionType, price, carImage, agencyID, carID))  # carID added here

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Car data updated successfully!")
        refresh_treeview()
    else:
        messagebox.showwarning("No selection", "Please select a car record to update.")

# This function was duplicated
# Function to handle image upload 
def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        try:
            img = Image.open(file_path)
            img = img.resize((250, 300), Image.Resampling.LANCZOS)
            img_photo = ImageTk.PhotoImage(img)
            upload_label.config(image=img_photo, text="")
            upload_label.image = img_photo
            upload_label.image_path = file_path  # Store the path in the label widget
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload image: {e}")


# Function to handle row selection from treeview
def on_treeview_select(event):
    selected_item = treeview.selection()
    if selected_item:
        carID, agencyName, registrationNo, model, colour, fuelType, seatingCapacity, transmissionType, price = treeview.item(selected_item, 'values')

        # Populate fields with the selected row's data
        selected_agency.set(agencyName)
        entry_registration.delete(0, tk.END)
        entry_registration.insert(0, registrationNo)
        entry_model.delete(0, tk.END)
        entry_model.insert(0, model)
        entry_colour.delete(0, tk.END)
        entry_colour.insert(0, colour)
        selected_fuel.set(fuelType)
        selected_seat.set(seatingCapacity)
        selected_transmission.set(transmissionType)
        entry_price.delete(0, tk.END)
        entry_price.insert(0, price)

        # Retrieve the car image path from the database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT carImage FROM CarDetails WHERE carID = ?', (carID,))
        car_image_path = cursor.fetchone()
        conn.close()

        if car_image_path and car_image_path[0]:
            try:
                img = Image.open(car_image_path[0])
                img = img.resize((250, 300), Image.Resampling.LANCZOS)
                img_photo = ImageTk.PhotoImage(img)
                upload_label.config(image=img_photo, text="")
                upload_label.image = img_photo  
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")
        else:
            upload_label.config(image="", text="No Image Uploaded")


# Function to handle login button click
def open_login(current_window, login_callback):
    current_window.destroy()  # Close the signup window
    login_callback()

# Function to handle login button click
def open_home(current_window, home_callback):
    current_window.destroy()  # Close the signup window
    home_callback()

# Function to handle profile button click
def open_profile(current_window, profile_callback):
    current_window.destroy()  # Close the signup window
    profile_callback()

def accManage(current_window, login_callback,profile_callback):
    droptabFrame = ctk.CTkFrame(detailFrame,width=160,height=170, bg_color="#E6F6FF",fg_color="#E6F6FF")
    droptabFrame.place(x=16, y=413)
    
    myAcc = ctk.CTkButton(master=droptabFrame, text="My Account", text_color="#000000", fg_color=("#E6F6FF","#D9D9D9"), 
                        bg_color="#E6F6FF", font=("SegoeUI Bold", 20), command=lambda:open_profile(current_window, profile_callback))
    myAcc.place(x=24,y=15)

    setting = ctk.CTkButton(master=droptabFrame, text="Setting", text_color="#000000", fg_color=("#E6F6FF","#D9D9D9"), 
                            bg_color="#E6F6FF", font=("SegoeUI Bold", 20))
    setting.place(x=45,y=70)

    logout = ctk.CTkButton(master=droptabFrame, text="Log Out", text_color="#000000", fg_color=("#E6F6FF","#D9D9D9"), 
                            bg_color="#E6F6FF", font=("SegoeUI Bold", 20), command=lambda:open_login(current_window, login_callback))
    logout.place(x=42,y=125)

def carDetails(login_callback,home_callback,bookings_callback):
    # Create the main application window
    global detailFrame
    detailFrame = Toplevel()
    detailFrame.title("Login")
    detailFrame.geometry("1280x720")
    detailFrame.resizable(False, False)
    detailFrame.config(bg="white")

    # Load the background image
    bg_image = Image.open(relative_to_assets("bg cardetails.png"))
    bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Set the background image
    bg_label = tk.Label(detailFrame, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    pfp_img = ctk.CTkImage(Image.open(relative_to_assets("image_4.png")),size=(100,100))
    pfp_label = ctk.CTkButton(detailFrame, image=pfp_img, text="", bg_color="#FE453B", fg_color="#FE453B",
                              width=40, height=40, command=lambda:accManage(detailFrame,login_callback))
    pfp_label.place(x=41, y=590)
    pywinstyles.set_opacity(pfp_label,color="#FE453B")

    # Relocate buttons
    home_button = ctk.CTkButton(master=detailFrame, text="Home", width=120, fg_color=("#F95C41","#FA5740"), bg_color="#FA5740", 
                                text_color="#FFF6F6", font=("Tw Cen MT Condensed Extra Bold", 20), command=lambda: open_home(detailFrame,home_callback))
    home_button.place(x=22, y=100)
    pywinstyles.set_opacity(home_button,color="#FA5740")

    # Label to display uploaded image
    global upload_label
    upload_label = tk.Label(detailFrame, text="No Image Uploaded", fg="white", bg="#394552", width=25, height=15)
    upload_label.place(x=88, y=215, width=340, height=170)  

    # Upload the upload icon
    ori_image = Image.open(relative_to_assets("image-upload.png"))
    resized_image = ori_image.resize((180, 180), Image.Resampling.LANCZOS)
    icon_image = ImageTk.PhotoImage(resized_image)

    # Button to upload image
    upload_button = tk.Button(detailFrame, image= icon_image, command=upload_image, font= "Arial", bg="#394552", fg="black", bd=0, width=180, height=180)
    upload_button.place(x=175, y=210)

    # Agency Name
    global selected_agency
    selected_agency = tk.StringVar(value="Select")
    agency_options = ["J&C Agency", "Wheels Agency", "Auto Agency"]
    agency_menu = ttk.Combobox(detailFrame, textvariable=selected_agency, values=agency_options, font=("Arial", 10))
    agency_menu.place(x=243, y=461, width=176.0, height= 33.0)  

    # Entry for registration number
    global entry_registration
    entry_registration = tk.Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
    entry_registration.place(x=243.0, y=516.0, width=176.0, height=33.0)

    # Entry for model
    global entry_model
    entry_model = tk.Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
    entry_model.place(x=620.0, y=461.0, width=176.0, height=33.0)

    # Entry for colour
    global entry_colour
    entry_colour = tk.Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
    entry_colour.place(x=620.0, y=516.0, width=176.0, height=33.0)

    # Dropdown for Fuel Type
    global selected_fuel
    selected_fuel = tk.StringVar(value="Select")
    fuel_options = ["Petrol", "Diesel", "Electric", "Hybrid"]
    fuel_menu = ttk.Combobox(detailFrame, textvariable=selected_fuel, values=fuel_options, font=("Arial", 10))
    fuel_menu.place(x=620, y=569, width=176.0, height= 33.0)  

    # Dropdown for selecting seating capacity
    global selected_seat
    selected_seat = tk.StringVar(value="Select")
    seat_options = ["2-seater", "4-seater", "6-seater"]
    seat_menu = ttk.Combobox(detailFrame, textvariable=selected_seat, values=seat_options, font=("Arial", 10))
    seat_menu.place(x=997, y=461, width=176.0, height= 33.0)  

    # Dropdown for selecting transmission type
    global selected_transmission
    selected_transmission = tk.StringVar(value="Select")
    transmission_options = ["Manual", "Automatic"]
    transmission_menu = ttk.Combobox(detailFrame, textvariable=selected_transmission, values=transmission_options, font=("Arial", 10))
    transmission_menu.place(x=997, y=516, width=176.0, height= 33.0)  

    # Entry for price
    global entry_price
    entry_price = tk.Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
    entry_price.place(x=997.0, y=569.0, width=176.0, height=33.0)


    # Treeview for displaying saved data
    global treeview
    columns = ('id', 'rental_agency', 'registration_number', 'model', 'colour', 'fuel_type', 'seating_capacity', 'transmission_type', 'price_rate')
    treeview = ttk.Treeview(detailFrame, columns=columns, show='headings', height=9)

    # Define the headings
    for col in columns:
        treeview.heading(col, text=col.capitalize())
        treeview.column(col, width=75)

    treeview.place(x=517, y=199)  

    treeview.bind("<<TreeviewSelect>>", on_treeview_select)
    
    agencyName = selected_agency.get()
    registrationNo = entry_registration.get()
    model = entry_model.get()
    colour = entry_colour.get()
    fuelType = selected_fuel.get()
    seatingCapacity = selected_seat.get()
    transmissionType = selected_transmission.get()
    price = entry_price.get()

    # Button to save
    save_button = tk.Button(detailFrame, text="SAVE", font= "Arial", bg="#5DC122", fg="black", bd=0, width=10, command= save_data(agencyName,registrationNo,model,colour,fuelType,seatingCapacity,transmissionType,price))
    save_button.place(x=185, y=655)

    # Button to update
    update_button = tk.Button(detailFrame, text="UPDATE", font= "Arial", bg="#FFB300", fg="black", bd=0, width=10, command= update_data)
    update_button.place(x=455, y=655)

    # Button to delete
    delete_button = tk.Button(detailFrame, text="DELETE", font= "Arial", bg="#FF443B", fg="black", bd=0, width=10, command= delete_data)
    delete_button.place(x=724, y=655)

    # Button to clear
    clear_button = tk.Button(detailFrame, text="CLEAR", font= "Arial", bg="#D9D9D9", fg="black", bd=0, width=10, command= clear_entries)
    clear_button.place(x=994, y=655)


    # Call this function after the mainloop to initialize the display of existing data
    refresh_treeview()