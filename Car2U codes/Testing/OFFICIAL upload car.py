import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import sqlite3
from pathlib import Path
from io import BytesIO

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\main\assets\Admin-Upload-Car")

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
            price DECIMAL(10, 2) NOT NULL,
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
    return conn, cursor

# Function to convert image to BLOB
def convert_image_to_blob(image_path):
    with open(image_path, 'rb') as file:
        return file.read()

# Function to save data to the database
def save_data():
    agencyName = selected_agency.get()
    registrationNo = entry_registration.get()
    model = entry_model.get()
    colour = entry_colour.get()
    fuelType = selected_fuel.get()
    seatingCapacity = selected_seat.get()
    transmissionType = selected_transmission.get()
    try:
        price = float(entry_price.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for the price rate.")
        return

    # Validate image path
    if not hasattr(upload_label, 'image_path'):
        messagebox.showerror("No Image", "Please upload an image.")
        return

    carImage = convert_image_to_blob(upload_label.image_path)  # Convert image to BLOB

    # Get agencyID from agency name
    conn, cursor = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT agencyID FROM RentalAgency WHERE agencyName = ?', (agencyName,))
    agency_data = cursor.fetchone()
    conn.close()

    if agency_data:
        agencyID = agency_data[0]
    else:
        messagebox.showerror("Error", "Selected agency does not exist.")
        conn.close()
        return

    conn, cursor = connect_db()
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

    try:
        conn, cursor = connect_db()
        cursor = conn.cursor()

        # Join CarDetails with RentalAgency to fetch agency names
        cursor.execute('''
            SELECT c.carID, r.agencyName, c.registrationNo, c.model, c.colour, c.fuelType, c.seatingCapacity, c.transmissionType, c.price
            FROM CarDetails c
            JOIN RentalAgency r ON c.agencyID = r.agencyID
        ''')
        rows = cursor.fetchall()

        for row in rows:
            treeview.insert("", "end", values=row)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

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

        conn, cursor = connect_db()
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

        carImage = convert_image_to_blob(upload_label.image_path)  # Convert image to BLOB

        # Get agencyID from agency name
        conn, cursor = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT agencyID FROM rentalAgency WHERE agencyName = ?', (rentalAgency,))
        agency_data = cursor.fetchone()
        conn.close()

        if agency_data:
            agencyID = agency_data[0]
        else:
            conn = connect_db()
            messagebox.showerror("Error", "Selected agency does not exist.")
            conn.close()
            return

        conn, cursor = connect_db()
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

# Function to handle image upload
def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        try:
            img = Image.open(file_path)
            img = img.resize((250, 300), Image.LANCZOS)
            img_photo = ImageTk.PhotoImage(img)
            upload_label.config(image=img_photo, text="")
            upload_label.image = img_photo
            upload_label.image_path = file_path  # Store the path in the label widget
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload image: {e}")

def convert_data(data):
    global car_img
    img_byte = BytesIO(data)
    img = Image.open(img_byte)
    img = img.resize((280,160), Image.Resampling.LANCZOS)
    car_img = ImageTk.PhotoImage(img)
    return car_img

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
        conn, cursor = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT carImage FROM CarDetails WHERE carID = ?', (carID,))
        car_image_path = cursor.fetchone()
        conn.close()

        if car_image_path and car_image_path[0]:
            try:
                img = convert_data(car_image_path[0])
                upload_label.config(image=img, text="")
                upload_label.image = img  # Keep a reference to avoid garbage collection
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")
        else:
            upload_label.config(image="", text="No Image Uploaded")

# Create main window
root = tk.Tk()
root.title("Car Upload Page")
root.geometry("1280x720")

# Load the background image
bg_image_path = relative_to_assets("Car Lisintg Form.png")
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((1280, 720), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Set the background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Label to display uploaded image with background image
upload_label = tk.Label(root, text="No Image Uploaded", fg="white", bg="#394552", width=25, height=100)
upload_label.place(x=290, y=150, width=280, height=160)

# Button to upload image
upload_button = tk.Button(root, text="Upload an Image", command=upload_image, font="Arial", bg="white", fg="black", bd=0, width=18, height=1)
upload_button.place(x=325, y=330)

# Agency Name
selected_agency = tk.StringVar(value="Select")
agency_options = ["J&C Agency", "Wheels Agency", "Auto Agency"]
agency_menu = ttk.Combobox(root, textvariable=selected_agency, values=agency_options, font=("Arial", 10))
agency_menu.place(x=353, y=418, width=176.0, height= 33.0)  


# Entry for registration number
entry_registration = tk.Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_registration.place(x=353, y=473, width=176.0, height=33.0)


# Entry for model
entry_model = tk.Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_model.place(x=713, y=418, width=176.0, height=33.0)


# Entry for colour
entry_colour = tk.Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_colour.place(x=713, y=473, width=176.0, height=33.0)


# Dropdown for Fuel Type
selected_fuel = tk.StringVar(value="Select")
fuel_options = ["Petrol", "Diesel", "Electric", "Hybrid"]
fuel_menu = ttk.Combobox(root, textvariable=selected_fuel, values=fuel_options, font=("Arial", 10))
fuel_menu.place(x=713, y=526, width=176.0, height= 33.0)  


# Dropdown for selecting seating capacity
selected_seat = tk.StringVar(value="Select")
seat_options = ["2-seater", "4-seater", "6-seater"]
seat_menu = ttk.Combobox(root, textvariable=selected_seat, values=seat_options, font=("Arial", 10))
seat_menu.place(x=1071, y=414, width=176.0, height= 33.0)  


# Dropdown for selecting transmission type
selected_transmission = tk.StringVar(value="Select")
transmission_options = ["Manual", "Automatic"]
transmission_menu = ttk.Combobox(root, textvariable=selected_transmission, values=transmission_options, font=("Arial", 10))
transmission_menu.place(x=1071, y=469, width=176.0, height= 33.0)  


# Entry for price
entry_price = tk.Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_price.place(x=1071, y=522, width=176.0, height=33.0)

# Treeview for displaying saved data
columns = ('id', 'rental_agency', 'registration_number', 'model', 'colour', 'fuel_type', 'seating_capacity', 'transmission_type', 'price_rate')
treeview = ttk.Treeview(root, columns=columns, show='headings', height=9)

# Define the headings
for col in columns:
    treeview.heading(col, text=col.capitalize())
    treeview.column(col, width=71)

treeview.place(x=613, y=119)  # Adjust this position as needed
treeview.bind("<<TreeviewSelect>>", on_treeview_select)

# Button to save
save_button = tk.Button(root, text="SAVE", font= "Arial", bg="#5DC122", fg="black", bd=0, width=10, command= save_data)
save_button.place(x=270, y=645)

# Button to update
update_button = tk.Button(root, text="UPDATE", font= "Arial", bg="#FFB300", fg="black", bd=0, width=10, command= update_data)
update_button.place(x=542, y=645)

# Button to delete
delete_button = tk.Button(root, text="DELETE", font= "Arial", bg="#FF443B", fg="black", bd=0, width=10, command= delete_data)
delete_button.place(x=811, y=645)

# Button to clear
clear_button = tk.Button(root, text="CLEAR", font= "Arial", bg="#D9D9D9", fg="black", bd=0, width=10, command= clear_entries)
clear_button.place(x=1084, y=645)

# Call this function after the mainloop to initialize the display of existing data
refresh_treeview()

# Start the main loop
root.mainloop()



