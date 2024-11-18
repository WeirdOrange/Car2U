import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry

def example1():
    def print_sel():
        print(cal.selection_get())

    top = tk.Toplevel(root)

    cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                   cursor="hand1", year=2018, month=2, day=5)

    cal.pack(fill="both", expand=True)
    ttk.Button(top, text="ok", command=print_sel).pack()


def example2():

    top = tk.Toplevel(root)

    cal = Calendar(top, selectmode='none')
    date = cal.datetime.today() + cal.timedelta(days=2)
    cal.calevent_create(date, 'Hello World', 'message')
    cal.calevent_create(date, 'Reminder 2', 'reminder')
    cal.calevent_create(date + cal.timedelta(days=-2), 'Reminder 1', 'reminder')
    cal.calevent_create(date + cal.timedelta(days=3), 'Message', 'message')

    cal.tag_config('reminder', background='red', foreground='yellow')

    cal.pack(fill="both", expand=True)
    ttk.Label(top, text="Hover over the events.").pack()


def example3():
    global cal, dates_to_highlight
    top = tk.Toplevel(root)

    ttk.Label(top, text='Choose date').pack(padx=10, pady=10)

    cal = DateEntry(top, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=2018)
    cal.pack(padx=10, pady=10)
    cal.bind("<<DateEntrySelected>>", on_date_select)
    
    #style_calendar(cal)
    
def style_calendar(calendar):
    # Adding a custom style for a specific date (e.g., Nov 20, 2024)
    calendar.tag_configure('highlight', background='lightblue', foreground='darkblue')
    calendar.calevent_create('2024-11-20', '', 'highlight')  # Add the date to the 'highlight' tag

def on_date_select(event):
    selected_date = cal.get_date().strftime('%Y-%m-%d')
    if selected_date in dates_to_highlight:
        # Change the foreground color to red to indicate disallowed date
        cal.configure(foreground='red')
    else:
        # Reset color to normal if date is allowed
        cal.configure(foreground='black')

root = tk.Tk()
ttk.Button(root, text='Calendar', command=example1).pack(padx=10, pady=10)
ttk.Button(root, text='Calendar with events', command=example2).pack(padx=10, pady=10)
ttk.Button(root, text='DateEntry', command=example3).pack(padx=10, pady=10)

dates_to_highlight = ["2024-11-15","2024-11-02","2024-11-21","2024-11-01"]
root.mainloop()