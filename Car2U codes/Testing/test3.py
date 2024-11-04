from pathlib import Path
from PIL import Image
from tkinter import Toplevel, messagebox, ttk
from tkcalendar import Calendar, DateEntry
import pandas as pd
import customtkinter as ctk 
import pywinstyles
import sqlite3

def Database(): #creating connection to database and creating table
    global conn, cursor
    conn = sqlite3.connect("car2u.db")
    # Enable access to columns by name
    cursor = conn.cursor()

def onRent(carNo,o):
    carNoLabel = ctk.CTkLabel(onRentFrame,text=carNo,font=("Segoe UI", 16))
            
    pickupMainFrame = ctk.CTkFrame(cTaskFrame, width=980, height=72, bg_color="#FFFFFF", fg_color="#FFFFFF") # Act as Main feature
def pickCar(carNo,pickTime,pickLocate,p):
    # To Pick-Up Car
    pickupFrame = ctk.CTkFrame(cTaskFrame, width=980, height=72, bg_color="#FFFFFF", fg_color="#FFFFFF") # To repeat if same time, but different car
    carNoLabel = ctk.CTkLabel(pickupFrame,text=carNo,font=("Segoe UI", 16))
    carTimeLabel = ctk.CTkLabel(pickupFrame,text=pickTime,font=("Segoe UI", 16))
    carLocate = ctk.CTkLabel(pickupFrame,text=pickLocate,font=("Segoe UI", 16))

#To Drop-Off Car
def dropCar(carNo,pickTime,pickLocate,d):
    dropffFrame = ctk.CTkFrame(cTaskFrame, width=980, height=72, bg_color="#FFFFFF", fg_color="#FFFFFF")
    pywinstyles.set_opacity(dropffFrame,color="#FFFFFF")
    carNoLabel = ctk.CTkLabel(dropffFrame,text=carNo,font=("Segoe UI", 16))
    carNoLabel.place(x=44,y=0+d*86)
    carTimeLabel = ctk.CTkLabel(dropffFrame,text=pickTime,font=("Segoe UI", 16))
    carTimeLabel.place(x=173,y=0+d*86)
    carLocateFrame = ctk.CTkFrame(dropffFrame,width=227,height=57)
    carLocateFrame.place(x=15,y=30)
    carLocate = ctk.CTkLabel(carLocateFrame,text=pickLocate,font=("Segoe UI", 16))
    carLocate.place(x=0,y=0)
    
# Function to support tkcalendar view
def refresh_CalendarEvent():
    selected_date = task_calendar.get_date()
    try:
        Database()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""SELECT C.registrationNo, pickupDate,pickupLocation,pickupTime,dropoffDate,dropoffLocation,dropoffTime 
                            FROM BookingDetails B 
                                INNER JOIN CarDetails C ON B.carID = C.carID
                                WHERE agencyID = 1 AND ((pickupDate >= '?' AND pickupDate <= '?') or (dropoffDate >= '?' AND dropoffDate <= '?'))""",(selected_date,selected_date))
        fetchData = cursor.fetchall()

        dateLabel = ctk.CTkLabel(cTaskFrame,text=selected_date,width=260,anchor='center',font=('Segoe UI',16))
        dateLabel.pack(side='top',fill='both',padx=0,pady=8)

        for row in fetchData:
            carNo = row[0]
            start_date = row[1]
            pickLocate = row[2]
            pickTime = row[3]
            end_date = row[4]
            dropLocate = row[5]
            dropTime = row[6]

        # Setting up frames
        # Cars On Rent
        global onRentFrame
        onRentFrame = ctk.CTkFrame(cTaskFrame, width=980, height=72, bg_color="#FFFFFF", fg_color="#FFFFFF")
        pywinstyles.set_opacity(onRentFrame,color="#FFFFFF")
                    
        dropTitle = ctk.CTkLabel(cTaskFrame,text="Drop-Off Car:",font=("Segoe UI", 20))
        dropMainFrame = ctk.CTkFrame(cTaskFrame, width=980, height=72, bg_color="#FFFFFF", fg_color="#FFFFFF") # Act as Main feature
        


        # checking if date selected is within the period
        date_range = pd.date_range(start=start_date, end=end_date)
        for date in date_range:
            if selected_date == date:
                if isinstance(onRentFrame, ctk.CTkFrame):
                    break
                else:
                    onRentTitle = ctk.CTkLabel(cTaskFrame,text="Car On Rent:",font=("Segoe UI",16))
                    onRentTitle.pack()
                    onRentFrame.pack()
                    o += 1

                if selected_date == start_date:
                    print("a")
                    
    except sqlite3.Error as e:
        messagebox.showerror("Error", "Error occurred during registration: {}".format(e))
    finally:
        conn.close()

adminHomeFrame = ctk.CTk()
global task_calendar
task_calendar = Calendar(adminHomeFrame,date_pattern='y-mm-dd',showothermonthdays=False)
task_calendar.pack(fill="both", expand=True)
refresh_CalendarEvent()

cTaskFrame = ctk.CTkFrame(adminHomeFrame, width=260, height=300, fg_color="#FFFFFF", border_width=2, border_color="#000000")
cTaskFrame.place(x=620,y=80)
cTask = ctk.CTkLabel(cTaskFrame, text="No Bookings Today")
cTask.place(x=70,y=70)


adminHomeFrame.mainloop()