
a = [1,2,3,4,5]
b = 6
c = 5

if b not in a:
    print("B is not in a")
if c in a:
    print("C is in a")

"""
import customtkinter as ctk
import sqlite3
import pandas as pd
from pandas import date_range
from tkinter import messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry

def fetch_booking_and_price():
    nexttoday = pickupDate.get_date()+timedelta(1)
    dropoffDate.config(mindate=nexttoday)

def checking():
    selected_Pdate = pickupDate.get_date()
    selected_Ddate = dropoffDate.get_date()

    if selected_Pdate != None and selected_Ddate != None:
        print("HIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII?")
        print("Pickup: ",selected_Pdate,"DropOff: ",selected_Ddate)
        try:
            conn = sqlite3.connect('CAR2U.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Fetch booking data from BookingDetails table
            cursor.execute('''
                SELECT pickupDate, dropoffDate FROM BookingDetails
                WHERE carID = ? and (pickupDate = ? or dropoffDate = ? or pickupDate = ? or dropoffDate = ?)
            ''', (1,selected_Pdate,selected_Pdate,selected_Ddate,selected_Ddate))

            booking_data = cursor.fetchall()
            conn.close()

            for row in booking_data:
                startdate = row[0]
                enddate = row[1]

                dateRange = date_range(start=startdate,end=enddate)
                selecteRange = date_range(start=selected_Pdate,end=selected_Ddate)
                print(dateRange)
                print(selecteRange)
                for i,date in enumerate(selecteRange):
                    for day in dateRange:
                        #print(f"day: {day} Selected date:{date}")
                        if day == date:
                            result = "Rejected"
                            print(f"Date:{day} is taken")
                        if date[i-1] != date[i]:
                            print(f"{date} is free")
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", "Error occurred during registration: {}".format(e))
        finally:
            conn.close()

root = ctk.CTk()
root.geometry("1280x720")
root.title("Embedding in Tk")

today = datetime.today()
pickupDate = DateEntry(root, width=12, background='orange', foreground='white', borderwidth=2, font=("Skranji", 10), mindate=today, date_pattern='yyyy/MM/dd')
pickupDate.bind("<<DateEntrySelected>>", lambda event: fetch_booking_and_price())
pickupDate.pack(pady=5)

global dropoffDate
dropoffDate = DateEntry(root, width=12, background='orange', foreground='white', borderwidth=2, font=("Skranji", 10), mindate=today, date_pattern='yyyy/MM/dd')
dropoffDate.pack(pady=5)

bttn = ctk.CTkButton(root,text="Check", command=lambda:checking())
bttn.pack(pady=10)

root.mainloop()
"""
"""
from datetime import datetime
import customtkinter as ctk

root = ctk.CTk()
root.geometry("1280x720")
root.title("Embedding in Tk")

time = ["10.00am","12.00am","3.00am","5.00am"]
timeVar = [datetime.strptime('10:00:00', "%H:%M:%S"),datetime.strptime('12:00:00', "%H:%M:%S"),datetime.strptime('15:00:00', "%H:%M:%S"),datetime.strptime('17:00:00', "%H:%M:%S")]

# Create a mapping from displayed time to datetime objects
time_mapping = dict(zip(time, timeVar))

selectedTime = ctk.StringVar()
pickupTime = ctk.CTkComboBox(master=root, width=90, state="readonly", values=time, variable=selectedTime, fg_color="#FFFFFF", font=("Skranji", 12))
pickupTime.place(x=0,y=0)
button = ctk.CTkButton(root, text="Press me", command=lambda:printStuff())
button.place(x=10,y=50)
def printStuff():
    print(time_mapping.get(selectedTime.get()).time())
root.mainloop()
"""
"""
import sqlite3
import hashlib

def Database(): #creating connection to database and creating table
    global conn, cursor
    conn = sqlite3.connect("car2u.db")
    cursor = conn.cursor()

password = ["adriana12345","faiz12345","pravin12345","ivan","soong","ivan"]

Database()
for i,row in enumerate(password):
    passwords = hashlib.sha256(str(row).encode()).hexdigest()
    i+=1
    if i >3:
        i+=3
    print("userID: ",i,"password: ",row)
    cursor.execute("UPDATE UserDetails SET password = ? WHERE userID = ?",(passwords,i))
    conn.commit()
"""
"""
import tkinter
import customtkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np
from datetime import datetime


sizes = [35, 25, 20, 15, 5]
labels = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
explode = (0.1, 0, 0, 0, 0)  # Explode the first slice

plt.pie(sizes, labels=labels, explode=explode, autopct='%1.1f%%', shadow=True)
plt.title('Matplotlib Pie Chart with Exploded Slice - how2matplotlib.com')
plt.axis('equal')
plt.show()

root = customtkinter.CTk()
root.geometry("1280x720")
root.title("Embedding in Tk")

canvasFrame = customtkinter.CTkFrame(root, width=200, height=200)
canvasFrame.place(x=10, y=10)

# x-coordinates of left sides of bars 
left = [1, 2, 3, 4, 5]

# heights of bars
height = [10, 24, 36, 40, 5]

# labels for bars
tick_label = ['one', 'two', 'three', 'four', 'five']

# plotting a bar chart
plt

# naming the x-axis
plt.xlabel('x - axis')
# naming the y-axis
plt.ylabel('y - axis')
# plot title
plt.title('My bar chart!')

# Create a figure for the pie chart
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
ax.bar(left, height, tick_label = tick_label, width = 0.8, color = ['red', 'green'])

canvas = FigureCanvasTkAgg(fig, master=canvasFrame)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, canvasFrame)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)


canvas.mpl_connect("key_press_event", on_key_press)

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


button = customtkinter.CTkButton(master=root, text="Quit", command=_quit)
button.pack(side=tkinter.BOTTOM)

current_month = datetime.now().month
print(current_month)

root.mainloop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.
"""
