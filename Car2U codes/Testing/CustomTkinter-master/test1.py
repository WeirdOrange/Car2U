import customtkinter as CTk
from customtkinter import *
import tkinter as tk
from tkinter import *
from tkinter import ttk
from plistlib import Image, ImageTk

app = CTk()
app.geometry("1280x720")

set_default_color_theme("dark-blue")
"""
CTkButton(master=app, text="Button").pack(pady=20, padx=20)
CTkCheckBox(master=app, text="Check box").pack(pady=20, padx=20)
CTkComboBox(master=app, values=["Option 1", "Option 2", "Option 3"]).pack(pady=20, padx=20)
CTkEntry(master=app, placeholder_text="Start typing...").pack(pady=20, padx=20)
CTkProgressBar(master=app).pack(pady=20, padx=20)
CTkRadioButton(master=app, text="Radio button").pack(pady=20, padx=20)
CTkSlider(master=app).pack(pady=20, padx=20)
CTkSwitch(master=app, text="Option").pack(pady=20, padx=20)

tab_frame = Frame(app,width=1280,height=90)
tab = CTkTabview(app)
tab.place(x=10, y=10)

tab1 = tab.add('Home')  # add tab at the end
tab2 = tab.add('Selections')  
tab3 = tab.add('Contact Us') 
tab4 = tab.add('About Us')

# set currently visible tab
tab1_1 = tab.set('Home')  
tab2_1 = tab.set('Selections')
tab3_1 = tab.set('Contact Us')
tab4_1 = tab.set('About Us')

Homebutton = CTkButton(tab1, text="Click Me!")
Homebutton.place(x=10, y=10)
"""

style = ttk.Style()
style.theme_create( "MyStyle", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {"configure": {"padding": [20, 20] },}})

style.theme_use("MyStyle")
im = Image.open('path/to/image')
ph = ImageTk.PhotoImage(im)

a_notebook = ttk.Notebook(app, width=1280, height=200)
a_tab = ttk.Frame(a_notebook)
a_notebook.add(a_tab, text = 'This is the first tab')
another_tab = ttk.Frame(a_notebook)
a_notebook.add(another_tab, text = 'This is another tab')
a_notebook.pack(expand=True, fill=tk.BOTH, side = RIGHT)


#tk.Button(app, text='Some Text!').pack(fill=tk.X)

app.mainloop()