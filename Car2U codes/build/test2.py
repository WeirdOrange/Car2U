import customtkinter as ctk
import sqlite3

# Initialize the main window
root = ctk.CTk()
root.geometry("400x400")

# Initial carID value (starts from 0)
car_id = 0

# Function to fetch data from the database based on carID
def fetch_data():
    global car_id
    # Connect to the SQLite database
    connection = sqlite3.connect('car2u.db')  # replace with your actual database name
    cursor = connection.cursor()

    # Fetch data with the query
    cursor.execute(f"SELECT * FROM CarDetails WHERE carID > {car_id} LIMIT 6")
    results = cursor.fetchall()

    # Update the car_id for the next batch (assuming 6 as the limit)
    if results:
        car_id += len(results)

    # Clear the existing frames before refreshing
    for widget in master_frame.winfo_children():
        widget.destroy()

    # Populate the new data in the frame
    for idx, row in enumerate(results):
        # Create a new frame for each row
        frame = ctk.CTkFrame(master=master_frame, width=300, height=50, corner_radius=10)
        frame.grid(row=idx, column=0, pady=5, padx=5)

        # Example of placing data in labels (assuming columns: carID, carName, carType)
        label = ctk.CTkLabel(frame, text=f"CarID: {row[0]}, CarName: {row[2]}, CarType: {row[1]}")
        label.pack(pady=10, padx=10)

    # Close the connection
    connection.close()

# Create a master frame where all the fetched data will be placed
master_frame = ctk.CTkFrame(root)
master_frame.pack(pady=20)

# Button to fetch and display new data
fetch_button = ctk.CTkButton(root, text="Fetch Data", command=fetch_data)
fetch_button.pack(pady=10)

# Run the main loop
root.mainloop()
