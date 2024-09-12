import tkinter as tk

root = tk.Tk()
root.geometry('1280x720')
root.title('pages galore')

def homepage():
    home_frame = tk.Frame(main_frame)
    lb = tk.Label(home_frame, text='Home Page\n\nPage 1',font=('Bold',32))
    lb.pack()
    home_frame.pack(pady=20)

def carpage():
    car_frame = tk.Frame(main_frame)
    lb = tk.Label(car_frame, text='Home Page\n\nPage 1',font=('Bold',32))
    lb.pack()
    car_frame.pack(pady=20)

def aboutpage():
    about_frame = tk.Frame(main_frame)
    lb = tk.Label(about_frame, text='Home Page\n\nPage 1',font=('Bold',32))
    lb.pack()
    about_frame.pack(pady=20)

def pickuppage():
    pickup_frame = tk.Frame(main_frame)
    lb = tk.Label(pickup_frame, text='Home Page\n\nPage 1',font=('Bold',32))
    lb.pack()
    pickup_frame.pack(pady=20)

def hide_indicators():
    home_indicate.config(bg='grey')
    car_indicate.config(bg='grey')
    about_indicate.config(bg='grey')
    pickup_indicate.config(bg='grey')

def indicate(lb,page):
    hide_indicators()
    lb.config(bg='#4B5B6D')
    for frame in main_frame.winfo_children():
        frame.destroy()
    page()

option_frame = tk.Frame(root,bg='grey')

home_btn = tk.Button(option_frame,text='Home',font=('Bold',12),
                     fg='black',bg='grey',
                     command=lambda:indicate(home_indicate,homepage))
home_btn.place(x=10,y=50)
home_indicate = tk.Label(option_frame,text='', bg='grey')
home_indicate.place(x=3,y=45,width=5 ,height=40)

car_btn = tk.Button(option_frame,text='Car for rent',font=('Bold',12),
                     fg='black',bg='grey',
                     command=lambda:indicate(car_indicate,carpage))
car_btn.place(x=10,y=100)
car_indicate = tk.Label(option_frame,text='', bg='grey')
car_indicate.place(x=3,y=95,width=5 ,height=40)

about_btn = tk.Button(option_frame,text='About Us',font=('Bold',12),
                     fg='black',bg='grey',
                     command=lambda:indicate(about_indicate,aboutpage))
about_btn.place(x=10,y=150)
about_indicate = tk.Label(option_frame,text='', bg='grey')
about_indicate.place(x=3,y=145,width=5 ,height=40)

pickup_btn = tk.Button(option_frame,text='P&R',font=('Bold',12),
                     fg='black',bg='grey',
                     command=lambda:indicate(pickup_indicate,pickuppage))
pickup_btn.place(x=10,y=200)
pickup_indicate = tk.Label(option_frame,text='', bg='grey')
pickup_indicate.place(x=3,y=195,width=5 ,height=40)

option_frame.pack(side=tk.LEFT)
option_frame.pack_propagate(False)
option_frame.configure(width=120,height=720)

main_frame = tk.Frame(root,bg='light blue',
                      highlightbackground='black',
                      highlightthickness=1)
main_frame.pack()
main_frame.pack_propagate(False)
main_frame.configure(width=1280,height=720)

root.mainloop()
